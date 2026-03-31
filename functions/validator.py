# ============================================================
# validator.py
# Rural Loan Eligibility System
# Validates all form inputs before eligibility check
# Returns list of errors if any field is invalid
# ============================================================

import re
from scheme_config import SCHEME_RULES


def validate_input(data, loan_scheme):
    """
    Validates form input data for the given loan scheme.
    Returns: {valid: bool, errors: list of error strings}
    """
    errors = []

    # ── Get scheme rules ─────────────────────────────────
    scheme = SCHEME_RULES.get(loan_scheme)
    if not scheme:
        return {
            'valid': False,
            'errors': [f'Invalid loan scheme: {loan_scheme}']
        }

    # ── 1. Validate Applicant Name ───────────────────────
    name = data.get('applicant_name', '').strip()
    if not name:
        errors.append('Applicant name is required')
    elif len(name) < 3:
        errors.append('Applicant name must be at least 3 characters')
    elif not re.match(r'^[a-zA-Z\s]+$', name):
        errors.append('Applicant name must contain only letters and spaces')

    # ── 2. Validate Phone Number ─────────────────────────
    phone = str(data.get('phone', '')).strip()
    if not phone:
        errors.append('Phone number is required')
    elif not re.match(r'^[6-9][0-9]{9}$', phone):
        errors.append('Phone must be a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9')

    farmer_state = str(data.get('state', '')).strip()
    if not farmer_state:
        errors.append('State selection is required')

    # ── 3. Scheme Specific Validations ───────────────────

    # Kisan Credit Card validations
    if loan_scheme == 'Kisan Credit Card':
        age = data.get('age')
        if age is None or age == '':
            errors.append('Age is required for Kisan Credit Card')
        else:
            try:
                age = int(age)
                if age < 1 or age > 120:
                    errors.append('Age must be between 1 and 120')
            except (ValueError, TypeError):
                errors.append('Age must be a valid number')

        farmer_type = data.get('farmer_type', '')
        if not farmer_type:
            errors.append('Farmer type is required')
        elif farmer_type not in ['owner', 'tenant', 'sharecropper']:
            errors.append('Farmer type must be owner, tenant, or sharecropper')

        if data.get('previous_default') is None:
            errors.append('Please indicate if you have any previous loan default')

    # PM Mudra Loan validations
    elif loan_scheme == 'PM Mudra Loan':
        business_type = data.get('business_type', '')
        if not business_type:
            errors.append('Business type is required')
        elif business_type != 'non-farm':
            errors.append('PM Mudra Loan is only for non-farm businesses')

        mudra_stage = data.get('mudra_stage', '')
        if not mudra_stage:
            errors.append('Mudra stage is required')
        elif mudra_stage not in ['Shishu', 'Kishore', 'Tarun']:
            errors.append('Mudra stage must be Shishu, Kishore, or Tarun')

        if data.get('previous_default') is None:
            errors.append('Please indicate if you have any previous loan default')

    # Rural Housing Loan validations
    elif loan_scheme == 'Rural Housing Loan':
        if data.get('secc_listed') is None:
            errors.append('Please indicate if you are listed in SECC 2011')

        if data.get('previous_pmay') is None:
            errors.append('Please indicate if you are a previous PMAY beneficiary')

        house_condition = data.get('house_condition', '')
        if not house_condition:
            errors.append('Current house condition is required')
        elif house_condition not in ['none', 'kutcha', 'pucca']:
            errors.append('House condition must be none, kutcha, or pucca')

        if data.get('previous_default') is None:
            errors.append('Please indicate if you have any previous loan default')

    # NABARD Farm Loan validations
    elif loan_scheme == 'NABARD Farm Loan':
        farmer_type = data.get('farmer_type', '')
        if not farmer_type:
            errors.append('Farmer type is required')
        elif farmer_type not in ['owner', 'tenant', 'sharecropper']:
            errors.append('Farmer type must be owner, tenant, or sharecropper')

        land_acres = data.get('land_acres')
        if land_acres is None or land_acres == '':
            errors.append('Land size in acres is required')
        else:
            try:
                land_acres = float(land_acres)
                if land_acres <= 0:
                    errors.append('Land size must be greater than 0')
            except (ValueError, TypeError):
                errors.append('Land size must be a valid number')

        crop_name = data.get('crop_name', '').strip()
        if not crop_name:
            errors.append('Crop name is required')
        elif len(crop_name) < 2:
            errors.append('Please enter a valid crop name')

        if data.get('bank_account_rrb') is None:
            errors.append('Please indicate if you have an RRB or cooperative bank account')

        if data.get('previous_default') is None:
            errors.append('Please indicate if you have any previous loan default')

    # PM Fasal Bima validations
    elif loan_scheme == 'PM Fasal Bima':
        farmer_type = data.get('farmer_type', '')
        if not farmer_type:
            errors.append('Farmer type is required')
        elif farmer_type not in ['owner', 'tenant', 'sharecropper']:
            errors.append('Farmer type must be owner, tenant, or sharecropper')

        land_acres = data.get('land_acres')
        if land_acres is None or land_acres == '':
            errors.append('Land size in acres is required')
        else:
            try:
                land_acres = float(land_acres)
                if land_acres <= 0:
                    errors.append('Land size must be greater than 0')
            except (ValueError, TypeError):
                errors.append('Land size must be a valid number')

        crop_name = data.get('crop_name', '').strip()
        if not crop_name:
            errors.append('Crop name is required')
        elif len(crop_name) < 2:
            errors.append('Please enter a valid crop name')

        crop_season = data.get('crop_season', '')
        if not crop_season:
            errors.append('Crop season is required')
        elif crop_season not in ['Kharif', 'Rabi', 'Zaid']:
            errors.append('Crop season must be Kharif, Rabi, or Zaid')

        if data.get('enrolled_before_cutoff') is None:
            errors.append('Please indicate if you enrolled before the season cutoff date')

    # ── Return Result ─────────────────────────────────────
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


# ── Quick local test ──────────────────────────────────────
if __name__ == '__main__':
    # Test 1 — Valid KCC application
    test1 = validate_input({
        'applicant_name': 'Ramu Kumar',
        'phone': '9876543210',
        'age': 35,
        'farmer_type': 'owner',
        'previous_default': False
    }, 'Kisan Credit Card')
    print('Test 1 (Valid KCC):', test1)

    # Test 2 — Invalid phone number
    test2 = validate_input({
        'applicant_name': 'Ramu Kumar',
        'phone': '1234567890',
        'age': 35,
        'farmer_type': 'owner',
        'previous_default': False
    }, 'Kisan Credit Card')
    print('Test 2 (Invalid phone):', test2)

    # Test 3 — Valid Mudra application
    test3 = validate_input({
        'applicant_name': 'Sita Devi',
        'phone': '8765432109',
        'business_type': 'non-farm',
        'mudra_stage': 'Shishu',
        'previous_default': False
    }, 'PM Mudra Loan')
    print('Test 3 (Valid Mudra):', test3)
