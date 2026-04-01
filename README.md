# Rural Loan Eligibility Checker

Rural loan application portal with:

- Firebase Hosting for frontend
- Firestore for database
- Render for Python backend
- Cloudinary for document storage

## Current Architecture

- `frontend/index.html`
  Role-based landing page
- `frontend/farmer.html`
  Farmer application and status tracking
- `frontend/dashboard.html`
  State agent review dashboard
- `frontend/app-config.js`
  State list, agent credentials, and deployed backend base URL
- `functions/app.py`
  Render-ready Flask backend
- `functions/main.py`
  Previous Firebase Functions version kept in repo for reference
- `firebase.json`
  Firebase Hosting + Firestore deployment config
- `render.yaml`
  Render service definition

## Backend Routes

The Render backend exposes:

- `/submit_loan`
- `/check_status`
- `/get_applications`
- `/update_status`

## Local Development

Local frontend pages still use the Firebase emulator-style localhost API URLs.

## Render Deployment

Create a new Render Web Service from this repo.

Recommended settings:

- Runtime: `Python`
- Root directory: `functions`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

You can also use the included [render.yaml](c:/Users/manoj/rural-loan-system/render.yaml).

### Render Environment Variables

Add these in Render:

- `COLLECTION_NAME=applications`
- `FIREBASE_SERVICE_ACCOUNT_JSON=<your Firebase service account JSON as one line>`

The backend uses `FIREBASE_SERVICE_ACCOUNT_JSON` to connect securely to Firestore from Render.

## Firebase Hosting Deployment

This repo is now configured so Firebase deploys only:

- Hosting
- Firestore rules
- Firestore indexes

Deploy command:

```powershell
cd c:\Users\manoj\rural-loan-system
$env:XDG_CONFIG_HOME='c:\Users\manoj\rural-loan-system\.firebase-config'
cmd /c firebase deploy --project rural-loan-system
```

## Frontend Configuration After Render Deploy

After Render gives you the live backend URL, update this line in [app-config.js](c:/Users/manoj/rural-loan-system/frontend/app-config.js):

```javascript
window.APP_API_BASE_URL = 'https://your-render-service.onrender.com';
```

Replace it with your actual Render backend URL, for example:

```javascript
window.APP_API_BASE_URL = 'https://rural-loan-system-api.onrender.com';
```

Then redeploy Firebase Hosting.

## Cloudinary

Cloudinary upload remains in the frontend and does not need architectural changes for this setup.

## Important Note

Agent credentials are still stored in frontend config for simplicity. For stronger production security, agent authentication should eventually move to the backend.
