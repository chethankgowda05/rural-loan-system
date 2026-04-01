# ============================================================
# main.py
# Rural Loan Eligibility System
# Firebase Cloud Functions — 4 HTTP endpoints
# submit_loan, get_applications, check_status, update_status
# ============================================================

import os
import json
import uuid
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_functions import https_fn
from flask import Flask, request as flask_request

from eligibility import check_eligibility
from validator import validate_input

# ── Initialize Firebase Admin SDK ────────────────────────
if not firebase_admin._apps:
    firebase_admin.initialize_app()


# ── Collection name — change via environment variable ────
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'applications')

# ── CORS headers added to every response ─────────────────
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}


def cors_response(data, status=200):
    """Helper to return JSON response with CORS headers."""
    response = https_fn.Response(
        json.dumps(data),
        status=status,
        headers={**CORS_HEADERS, 'Content-Type': 'application/json'}
    )
    return response


def handle_preflight():
    """Handle CORS preflight OPTIONS request."""
    return https_fn.Response('', status=204, headers=CORS_HEADERS)


# ════════════════════════════════════════════════════════
# FUNCTION 1 — submit_loan
# Receives form data + document URLs
# Validates → checks eligibility → saves to Firestore
# Returns eligibility result + bank list
# ════════════════════════════════════════════════════════
@https_fn.on_request()
def submit_loan(req: https_fn.Request) -> https_fn.Response:
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return handle_preflight()
    db = firestore.client()
    try:
        # ── Parse request body ────────────────────────
        body = req.get_json(silent=True)
        if not body:
            return cors_response(
                {'error': 'Invalid JSON body'},
                status=400
            )

        loan_scheme = body.get('loan_scheme', '')
        document_urls = body.get('document_urls', {})
        farmer_state = str(body.get('state', '')).strip()

        # ── Validate input ────────────────────────────
        validation = validate_input(body, loan_scheme)
        if not validation['valid']:
            return cors_response(
                {
                    'error': 'Validation failed',
                    'errors': validation['errors']
                },
                status=400
            )
        
        # ── Check for duplicate submission ───────────────────
        existing = db.collection(COLLECTION_NAME)\
                     .where('phone', '==', str(body.get('phone','')))\
                     .where('loan_scheme', '==', loan_scheme)\
                     .stream()
        
        for existing_doc in existing:
            existing_data = existing_doc.to_dict()
            existing_status = existing_data.get('status', '')
            # Block if previous is pending or approved
            if 'Incomplete' not in existing_status and \
                    'Rejected' not in existing_status:
                return cors_response({
                    'error': 'duplicate',
                    'message': (
                        f'You have already submitted an application '
                        f'for {loan_scheme}. '
                        f'Current status: {existing_status}. '
                        f'Check your status below.'
                    )
                }, status=409)

        # ── Check eligibility ─────────────────────────
        eligibility_result = check_eligibility(body, loan_scheme)

        # ── Build application record ──────────────────
        application_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        application = {
            'applicationId':     application_id,
            'applicant_name':    body.get('applicant_name', ''),
            'phone':             str(body.get('phone', '')),
            'state':             farmer_state,
            'loan_scheme':       loan_scheme,
            'input_data':        body,
            'document_urls':     document_urls,
            'eligibility_result': eligibility_result,
            'status':            eligibility_result.get('status', 'Pending'),
            'remarks':           '',
            'submitted_at':      now,
            'updated_at':        now,
        }

        # ── Save to Firestore ─────────────────────────
        db.collection(COLLECTION_NAME).document(application_id).set(application)

        # ── Return result to frontend ─────────────────
        return cors_response({
            'success':           True,
            'applicationId':     application_id,
            'eligible':          eligibility_result.get('eligible'),
            'state':             farmer_state,
            'status':            eligibility_result.get('status'),
            'reason':            eligibility_result.get('reason', ''),
            'interest_rate':     eligibility_result.get('interest_rate'),
            'premium_rate':      eligibility_result.get('premium_rate'),
            'loan_limit':        eligibility_result.get('loan_limit'),
            'banks':             eligibility_result.get('banks', []),
        })

    except Exception as e:
        return cors_response(
            {'error': f'Server error: {str(e)}'},
            status=500
        )


# ════════════════════════════════════════════════════════
# FUNCTION 2 — get_applications
# Fetches all applications from Firestore
# Used by bank official dashboard
# ════════════════════════════════════════════════════════
@https_fn.on_request()
def get_applications(req: https_fn.Request) -> https_fn.Response:
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return handle_preflight()
    db = firestore.client()

    try:
        # ── Fetch all applications ────────────────────
        agent_state = req.args.get('state', '').strip()
        query = db.collection(COLLECTION_NAME)
        if agent_state:
            query = query.where('state', '==', agent_state)

        docs = query.stream()

        applications = []
        for doc in docs:
            data = doc.to_dict()
            applications.append({
                'applicationId':  data.get('applicationId', ''),
                'applicant_name': data.get('applicant_name', ''),
                'phone':          data.get('phone', ''),
                'state':          data.get('state', ''),
                'loan_scheme':    data.get('loan_scheme', ''),
                'status':         data.get('status', ''),
                'remarks':        data.get('remarks', ''),
                'submitted_at':   data.get('submitted_at', ''),
                'updated_at':     data.get('updated_at', ''),
                'document_urls':  data.get('document_urls', {}),
                'eligibility_result': data.get('eligibility_result', {}),
                'input_data':     data.get('input_data', {}),
                'doc_verification': data.get('doc_verification', {}),
                'doc_feedback':   data.get('doc_feedback', {}),
            })

        applications.sort(
            key=lambda app: app.get('submitted_at', ''),
            reverse=True
        )

        return cors_response({
            'success': True,
            'state': agent_state,
            'count': len(applications),
            'applications': applications
        })

    except Exception as e:
        return cors_response(
            {'error': f'Server error: {str(e)}'},
            status=500
        )


# ════════════════════════════════════════════════════════
# FUNCTION 3 — check_status
# Finds all applications by phone number
# Used by farmer to track application status
# ════════════════════════════════════════════════════════
@https_fn.on_request()
def check_status(req: https_fn.Request) -> https_fn.Response:
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return handle_preflight()
    db = firestore.client()

    try:
        # ── Get phone from query params ───────────────
        phone = req.args.get('phone', '').strip()

        if not phone:
            return cors_response(
                {'error': 'Phone number is required'},
                status=400
            )

        # ── Query Firestore by phone ──────────────────
        docs = db.collection(COLLECTION_NAME)\
                 .where('phone', '==', str(phone))\
                 .stream()

        applications = []
        for doc in docs:
            data = doc.to_dict()
            applications.append({
                'applicationId':      data.get('applicationId', ''),
                'loan_scheme':        data.get('loan_scheme', ''),
                'applicant_name':     data.get('applicant_name', ''),
                'phone':              data.get('phone', ''),
                'state':              data.get('state', ''),
                'status':             data.get('status', ''),
                'remarks':            data.get('remarks', ''),
                'submitted_at':       data.get('submitted_at', ''),
                'updated_at':         data.get('updated_at', ''),
                'eligibility_result': data.get('eligibility_result', {}),
                'doc_verification':   data.get('doc_verification', {}),
                'doc_feedback':       data.get('doc_feedback', {}),
            })

        applications.sort(
            key=lambda app: app.get('submitted_at', ''),
            reverse=True
        )

        return cors_response({
            'success': True,
            'phone': phone,
            'count': len(applications),
            'applications': applications
        })

    except Exception as e:
        return cors_response(
            {'error': f'Server error: {str(e)}'},
            status=500
        )


# ════════════════════════════════════════════════════════
# FUNCTION 4 — update_status
# Bank official approves or rejects an application
# Updates status and remarks in Firestore
# ════════════════════════════════════════════════════════
@https_fn.on_request()
def update_status(req: https_fn.Request) -> https_fn.Response:
    if req.method == 'OPTIONS':
        return handle_preflight()
    db = firestore.client()

    try:
        body = req.get_json(silent=True)
        if not body:
            return cors_response(
                {'error': 'Invalid JSON body'}, status=400)

        application_id   = body.get('applicationId', '')
        new_status       = body.get('new_status', '')
        remarks          = body.get('remarks', '')
        doc_verification = body.get('doc_verification', {})
        doc_feedback     = body.get('doc_feedback', {})

        if not application_id:
            return cors_response(
                {'error': 'applicationId is required'}, status=400)

        valid_statuses = ['Approved', 'Rejected', 'Pending',
                          'Documents Incomplete']
        if new_status not in valid_statuses:
            return cors_response(
                {'error': f'new_status must be one of: {valid_statuses}'},
                status=400)

        doc_ref = db.collection(COLLECTION_NAME).document(application_id)
        doc     = doc_ref.get()
        if not doc.exists:
            return cors_response(
                {'error': f'Application {application_id} not found'},
                status=404)

        doc_ref.update({
            'status':           new_status,
            'remarks':          remarks,
            'doc_verification': doc_verification,
            'doc_feedback':     doc_feedback,
            'updated_at':       datetime.now().isoformat(),
        })

        return cors_response({
            'success':       True,
            'applicationId': application_id,
            'new_status':    new_status,
            'message':       f'Application updated to {new_status}'
        })

    except Exception as e:
        return cors_response(
            {'error': f'Server error: {str(e)}'}, status=500)
