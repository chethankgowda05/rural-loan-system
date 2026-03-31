# Rural Loan Eligibility Checker

A Firebase-based rural loan screening portal with separate flows for farmers and state agents.

## What It Does

- Farmers can submit loan applications, upload documents, select their state, and track status.
- State agents can log in by state, review only routed applications for that state, verify documents, and update application status.
- Firestore stores applications, document review state, remarks, and eligibility results.

## Project Structure

- `frontend/index.html`
  Landing page for role selection.
- `frontend/farmer.html`
  Farmer application and status tracking page.
- `frontend/dashboard.html`
  State agent login and review dashboard.
- `frontend/style.css`
  Shared UI styling.
- `frontend/app-config.js`
  State list and agent credentials.
- `functions/main.py`
  Firebase HTTP functions for submit, status, dashboard fetch, and updates.
- `functions/validator.py`
  Input validation rules.
- `firebase.json`
  Hosting, Functions, Firestore, and Hosting rewrite configuration.

## Firebase Endpoints

The frontend is configured to work in both environments:

- Local emulator:
  Uses `http://localhost:5001/...`
- Deployed site:
  Uses Hosting rewrites:
  - `/api/submit_loan`
  - `/api/check_status`
  - `/api/get_applications`
  - `/api/update_status`

## Local Development

1. Start the Firebase emulators.
2. Open the frontend through Firebase Hosting emulator.
3. Test farmer submission, status tracking, and agent dashboard review flow.

## Deployment

This project is configured for Firebase project:

- `rural-loan-system`

Recommended deploy command:

```powershell
$env:XDG_CONFIG_HOME='c:\Users\manoj\rural-loan-system\.firebase-config'
cmd /c firebase deploy --project rural-loan-system
```

## Current Deploy Note

Deployment requires Firebase authentication on the machine running the command. If not already logged in, run:

```powershell
$env:XDG_CONFIG_HOME='c:\Users\manoj\rural-loan-system\.firebase-config'
cmd /c firebase login
```

Then deploy again.

## Notes

- Agent credentials are currently stored in frontend config for simplicity.
- For production security, agent authentication should move to the backend.
- Cloudinary is used for document uploads from the frontend.
