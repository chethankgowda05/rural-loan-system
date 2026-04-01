import json
import os
import uuid
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request

from eligibility import check_eligibility
from validator import validate_input


COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "applications")
FIREBASE_SERVICE_ACCOUNT_JSON = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()


def initialize_firebase():
    if firebase_admin._apps:
        return

    if FIREBASE_SERVICE_ACCOUNT_JSON:
        cred_info = json.loads(FIREBASE_SERVICE_ACCOUNT_JSON)
        firebase_admin.initialize_app(credentials.Certificate(cred_info))
    else:
        firebase_admin.initialize_app()


initialize_firebase()

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"success": True, "message": "Render backend is running"})


@app.route("/submit_loan", methods=["POST", "OPTIONS"])
def submit_loan():
    if request.method == "OPTIONS":
        return ("", 204)

    db = firestore.client()

    try:
        body = request.get_json(silent=True)
        if not body:
            return jsonify({"error": "Invalid JSON body"}), 400

        loan_scheme = body.get("loan_scheme", "")
        document_urls = body.get("document_urls", {})
        farmer_state = str(body.get("state", "")).strip()

        validation = validate_input(body, loan_scheme)
        if not validation["valid"]:
            return jsonify({
                "error": "Validation failed",
                "errors": validation["errors"]
            }), 400

        existing = (
            db.collection(COLLECTION_NAME)
            .where("phone", "==", str(body.get("phone", "")))
            .where("loan_scheme", "==", loan_scheme)
            .stream()
        )

        for existing_doc in existing:
            existing_data = existing_doc.to_dict()
            existing_status = existing_data.get("status", "")
            if "Incomplete" not in existing_status and "Rejected" not in existing_status:
                return jsonify({
                    "error": "duplicate",
                    "message": (
                        f"You have already submitted an application for {loan_scheme}. "
                        f"Current status: {existing_status}. Check your status below."
                    )
                }), 409

        eligibility_result = check_eligibility(body, loan_scheme)
        application_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        application = {
            "applicationId": application_id,
            "applicant_name": body.get("applicant_name", ""),
            "phone": str(body.get("phone", "")),
            "state": farmer_state,
            "loan_scheme": loan_scheme,
            "input_data": body,
            "document_urls": document_urls,
            "eligibility_result": eligibility_result,
            "status": eligibility_result.get("status", "Pending"),
            "remarks": "",
            "submitted_at": now,
            "updated_at": now,
        }

        db.collection(COLLECTION_NAME).document(application_id).set(application)

        return jsonify({
            "success": True,
            "applicationId": application_id,
            "eligible": eligibility_result.get("eligible"),
            "state": farmer_state,
            "status": eligibility_result.get("status"),
            "reason": eligibility_result.get("reason", ""),
            "interest_rate": eligibility_result.get("interest_rate"),
            "premium_rate": eligibility_result.get("premium_rate"),
            "loan_limit": eligibility_result.get("loan_limit"),
            "banks": eligibility_result.get("banks", []),
        })
    except Exception as exc:
        return jsonify({"error": f"Server error: {str(exc)}"}), 500


@app.route("/get_applications", methods=["GET", "OPTIONS"])
def get_applications():
    if request.method == "OPTIONS":
        return ("", 204)

    db = firestore.client()

    try:
        agent_state = request.args.get("state", "").strip()
        query = db.collection(COLLECTION_NAME)
        if agent_state:
            query = query.where("state", "==", agent_state)

        docs = query.stream()
        applications = []

        for doc in docs:
            data = doc.to_dict()
            applications.append({
                "applicationId": data.get("applicationId", ""),
                "applicant_name": data.get("applicant_name", ""),
                "phone": data.get("phone", ""),
                "state": data.get("state", ""),
                "loan_scheme": data.get("loan_scheme", ""),
                "status": data.get("status", ""),
                "remarks": data.get("remarks", ""),
                "submitted_at": data.get("submitted_at", ""),
                "updated_at": data.get("updated_at", ""),
                "document_urls": data.get("document_urls", {}),
                "eligibility_result": data.get("eligibility_result", {}),
                "input_data": data.get("input_data", {}),
                "doc_verification": data.get("doc_verification", {}),
                "doc_feedback": data.get("doc_feedback", {}),
            })

        applications.sort(key=lambda item: item.get("submitted_at", ""), reverse=True)

        return jsonify({
            "success": True,
            "state": agent_state,
            "count": len(applications),
            "applications": applications,
        })
    except Exception as exc:
        return jsonify({"error": f"Server error: {str(exc)}"}), 500


@app.route("/check_status", methods=["GET", "OPTIONS"])
def check_status():
    if request.method == "OPTIONS":
        return ("", 204)

    db = firestore.client()

    try:
        phone = request.args.get("phone", "").strip()
        if not phone:
            return jsonify({"error": "Phone number is required"}), 400

        docs = (
            db.collection(COLLECTION_NAME)
            .where("phone", "==", str(phone))
            .order_by("submitted_at", direction=firestore.Query.DESCENDING)
            .stream()
        )

        applications = []
        for doc in docs:
            data = doc.to_dict()
            applications.append({
                "applicationId": data.get("applicationId", ""),
                "loan_scheme": data.get("loan_scheme", ""),
                "applicant_name": data.get("applicant_name", ""),
                "phone": data.get("phone", ""),
                "state": data.get("state", ""),
                "status": data.get("status", ""),
                "remarks": data.get("remarks", ""),
                "submitted_at": data.get("submitted_at", ""),
                "updated_at": data.get("updated_at", ""),
                "eligibility_result": data.get("eligibility_result", {}),
                "doc_verification": data.get("doc_verification", {}),
                "doc_feedback": data.get("doc_feedback", {}),
            })

        return jsonify({
            "success": True,
            "phone": phone,
            "count": len(applications),
            "applications": applications,
        })
    except Exception as exc:
        return jsonify({"error": f"Server error: {str(exc)}"}), 500


@app.route("/update_status", methods=["POST", "OPTIONS"])
def update_status():
    if request.method == "OPTIONS":
        return ("", 204)

    db = firestore.client()

    try:
        body = request.get_json(silent=True)
        if not body:
            return jsonify({"error": "Invalid JSON body"}), 400

        application_id = body.get("applicationId", "")
        new_status = body.get("new_status", "")
        remarks = body.get("remarks", "")
        doc_verification = body.get("doc_verification", {})
        doc_feedback = body.get("doc_feedback", {})

        if not application_id:
            return jsonify({"error": "applicationId is required"}), 400

        valid_statuses = ["Approved", "Rejected", "Pending", "Documents Incomplete"]
        if new_status not in valid_statuses:
            return jsonify({
                "error": f"new_status must be one of: {valid_statuses}"
            }), 400

        doc_ref = db.collection(COLLECTION_NAME).document(application_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({"error": f"Application {application_id} not found"}), 404

        doc_ref.update({
            "status": new_status,
            "remarks": remarks,
            "doc_verification": doc_verification,
            "doc_feedback": doc_feedback,
            "updated_at": datetime.now().isoformat(),
        })

        return jsonify({
            "success": True,
            "applicationId": application_id,
            "new_status": new_status,
            "message": f"Application updated to {new_status}",
        })
    except Exception as exc:
        return jsonify({"error": f"Server error: {str(exc)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
