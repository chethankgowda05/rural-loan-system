# ============================================================
# eligibility.py
# Rural Loan Eligibility System
# Core eligibility checking logic
# Reads all rules from scheme_config.py — never hardcoded
# To change a rule: edit scheme_config.py only
# ============================================================

from scheme_config import SCHEME_RULES
from banks_config import SCHEME_BANKS


def check_eligibility(data, loan_scheme):
    """
    Checks eligibility for the given loan scheme.
    Returns: {
        eligible: bool,
        status: str,
        reason: str,
        interest_rate or premium_rate: float,
        loan_limit: str (Mudra only),
        banks: list
    }
    """

    # ── Default rejected result ───────────────────────────
    result = {
        'eligible': False,
        'status': 'Rejected',
        'reason': '',
        'interest_rate': None,
        'premium_rate': None,
        'loan_limit': None,
        'banks': SCHEME_BANKS.get(loan_scheme, [])
    }

    # ── Get scheme rules ──────────────────────────────────
    scheme = SCHEME_RULES.get(loan_scheme)
    if not scheme:
        result['reason'] = f'Invalid loan scheme: {loan_scheme}'
        return result

    rules = scheme['eligibility_rules']

    # ══════════════════════════════════════════════════════
    # 1. KISAN CREDIT CARD
    # ══════════════════════════════════════════════════════
    if loan_scheme == 'Kisan Credit Card':

        # Check farmer type
        farmer_type = data.get('farmer_type', '')
        if farmer_type not in rules['farmer_types_allowed']:
            result['reason'] = 'Must be a farmer, tenant farmer, or sharecropper to apply for KCC'
            return result

        # Check age
        try:
            age = int(data.get('age', 0))
            if age < rules['age_min'] or age > rules['age_max']:
                result['reason'] = f'Age must be between {rules["age_min"]} and {rules["age_max"]} years for KCC'
                return result
        except (ValueError, TypeError):
            result['reason'] = 'Invalid age provided'
            return result

        # Check previous default
        if data.get('previous_default') is True:
            result['reason'] = 'Previous loan default disqualifies KCC application'
            return result

        # ── Approved ──────────────────────────────────────
        result['eligible'] = True
        result['status'] = 'Submitted - Verification Pending'
        result['interest_rate'] = scheme['interest_rate']
        return result

    # ══════════════════════════════════════════════════════
    # 2. PM MUDRA LOAN
    # ══════════════════════════════════════════════════════
    elif loan_scheme == 'PM Mudra Loan':

        # Check business type
        business_type = data.get('business_type', '')
        if business_type not in rules['business_type_allowed']:
            result['reason'] = 'PM Mudra Loan is only for non-farm micro and small businesses'
            return result

        # Check mudra stage
        mudra_stage = data.get('mudra_stage', '')
        if mudra_stage not in rules['mudra_stages_allowed']:
            result['reason'] = 'Invalid Mudra stage. Must be Shishu, Kishore, or Tarun'
            return result

        # Check previous default
        if data.get('previous_default') is True:
            result['reason'] = 'Previous loan default disqualifies Mudra Loan application'
            return result

        # ── Approved ──────────────────────────────────────
        stage_info = rules['loan_limits'][mudra_stage]
        result['eligible'] = True
        result['status'] =  'Submitted - Verification Pending'
        result['interest_rate'] = stage_info['rate']
        result['loan_limit'] = f"Up to Rs.{stage_info['limit']}"
        return result

    # ══════════════════════════════════════════════════════
    # 3. RURAL HOUSING LOAN (PMAY-G)
    # ══════════════════════════════════════════════════════
    elif loan_scheme == 'Rural Housing Loan':

        # Check SECC 2011 listing
        if data.get('secc_listed') is not True:
            result['reason'] = 'Must be listed in SECC 2011 beneficiary list to apply for PMAY-G'
            return result

        # Check previous PMAY
        if data.get('previous_pmay') is True:
            result['reason'] = 'Already a PMAY beneficiary — cannot apply again'
            return result

        # Check house condition
        house_condition = data.get('house_condition', '')
        if house_condition not in rules['house_conditions_allowed']:
            result['reason'] = 'Already owns a pucca house — not eligible for Rural Housing Loan'
            return result

        # Check previous default
        if data.get('previous_default') is True:
            result['reason'] = 'Previous loan default disqualifies Rural Housing Loan application'
            return result

        # ── Approved ──────────────────────────────────────
        result['eligible'] = True
        result['status'] =  'Submitted - Verification Pending'
        result['interest_rate'] = scheme['interest_rate']
        return result

    # ══════════════════════════════════════════════════════
    # 4. NABARD FARM LOAN
    # ══════════════════════════════════════════════════════
    elif loan_scheme == 'NABARD Farm Loan':

        # Check farmer type
        farmer_type = data.get('farmer_type', '')
        if farmer_type not in rules['farmer_types_allowed']:
            result['reason'] = 'Must be a farmer, tenant, or sharecropper to apply for NABARD Farm Loan'
            return result

        # Check land acres
        try:
            land_acres = float(data.get('land_acres', 0))
            if land_acres < rules['min_land_acres']:
                result['reason'] = 'Must have land or valid tenancy agreement for NABARD Farm Loan'
                return result
        except (ValueError, TypeError):
            result['reason'] = 'Invalid land size provided'
            return result

        # Check crop name
        crop_name = data.get('crop_name', '').strip()
        if not crop_name:
            result['reason'] = 'Must declare crop being cultivated for NABARD Farm Loan'
            return result

        # Check RRB bank account
        if data.get('bank_account_rrb') is not True:
            result['reason'] = 'Must have an account with RRB or cooperative bank for NABARD Farm Loan'
            return result

        # Check previous default
        if data.get('previous_default') is True:
            result['reason'] = 'Previous loan default disqualifies NABARD Farm Loan application'
            return result

        # ── Approved ──────────────────────────────────────
        result['eligible'] = True
        result['status'] =  'Submitted - Verification Pending'
        result['interest_rate'] = scheme['interest_rate']
        return result

    # ══════════════════════════════════════════════════════
    # 5. PM FASAL BIMA (CROP INSURANCE)
    # ══════════════════════════════════════════════════════
    elif loan_scheme == 'PM Fasal Bima':

        # Check farmer type
        farmer_type = data.get('farmer_type', '')
        if farmer_type not in rules['farmer_types_allowed']:
            result['reason'] = 'Must be a farmer, tenant, or sharecropper to apply for PM Fasal Bima'
            return result

        # Check land acres
        try:
            land_acres = float(data.get('land_acres', 0))
            if land_acres < rules['min_land_acres']:
                result['reason'] = 'Must have land or valid tenancy agreement for PM Fasal Bima'
                return result
        except (ValueError, TypeError):
            result['reason'] = 'Invalid land size provided'
            return result

        # Check crop name
        crop_name = data.get('crop_name', '').strip()
        if not crop_name:
            result['reason'] = 'Must declare crop for insurance coverage'
            return result

        # Check crop season
        crop_season = data.get('crop_season', '')
        if crop_season not in rules['crop_seasons_allowed']:
            result['reason'] = 'Invalid crop season. Must be Kharif, Rabi, or Zaid'
            return result

        # Check enrollment before cutoff
        if data.get('enrolled_before_cutoff') is not True:
            result['reason'] = 'Enrollment deadline for this season has passed'
            return result

        # ── Approved ──────────────────────────────────────
        premium_rates = scheme['premium_rate']
        result['eligible'] = True
        result['status'] =  'Submitted - Verification Pending'
        result['premium_rate'] = premium_rates.get(crop_season)
        return result

    # ── Unknown scheme ────────────────────────────────────
    else:
        result['reason'] = 'Invalid loan scheme selected'
        return result


# ── Quick local test ──────────────────────────────────────
if __name__ == '__main__':

    print('\n--- Test 1: KCC Approved ---')
    print(check_eligibility({
        'age': 35,
        'farmer_type': 'owner',
        'previous_default': False
    }, 'Kisan Credit Card'))

    print('\n--- Test 2: KCC Rejected (too young) ---')
    print(check_eligibility({
        'age': 17,
        'farmer_type': 'owner',
        'previous_default': False
    }, 'Kisan Credit Card'))

    print('\n--- Test 3: Mudra Approved (Shishu) ---')
    print(check_eligibility({
        'business_type': 'non-farm',
        'mudra_stage': 'Shishu',
        'previous_default': False
    }, 'PM Mudra Loan'))

    print('\n--- Test 4: NABARD Approved ---')
    print(check_eligibility({
        'farmer_type': 'owner',
        'land_acres': 2.5,
        'crop_name': 'Rice',
        'bank_account_rrb': True,
        'previous_default': False
    }, 'NABARD Farm Loan'))

    print('\n--- Test 5: Fasal Bima Approved ---')
    print(check_eligibility({
        'farmer_type': 'tenant',
        'land_acres': 1.0,
        'crop_name': 'Wheat',
        'crop_season': 'Rabi',
        'enrolled_before_cutoff': True
    }, 'PM Fasal Bima'))

    print('\n--- Test 6: PMAY-G Rejected (pucca house) ---')
    print(check_eligibility({
        'secc_listed': True,
        'previous_pmay': False,
        'house_condition': 'pucca',
        'previous_default': False
    }, 'Rural Housing Loan'))