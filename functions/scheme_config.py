# ============================================================
# scheme_config.py
# Rural Loan Eligibility System
# All scheme rules + required documents in one config file
# To add a new scheme: just add a new key to SCHEME_RULES
# ============================================================

SCHEME_RULES = {

    # ── 1. KISAN CREDIT CARD ──────────────────────────────
    'Kisan Credit Card': {
        'required_fields': [
            'applicant_name',
            'phone',
            'age',
            'farmer_type',
            'previous_default'
        ],
        'eligibility_rules': {
            'age_min': 18,
            'age_max': 75,
            'farmer_types_allowed': ['owner', 'tenant', 'sharecropper'],
            'allow_default': False,
        },
        'required_documents': [
            {
                'field_id': 'aadhaar',
                'label': 'Aadhaar Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'land_records',
                'label': 'Land Records (Patta/Khata/7-12 Extract)',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['owner']
            },
            {
                'field_id': 'tenancy_agreement',
                'label': 'Tenancy Agreement / Lease Deed',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['tenant', 'sharecropper']
            },
        ],
        'interest_rate': 4.0,
        'scheme_type': 'loan',
    },

    # ── 2. PM MUDRA LOAN ──────────────────────────────────
    'PM Mudra Loan': {
        'required_fields': [
            'applicant_name',
            'phone',
            'business_type',
            'mudra_stage',
            'previous_default'
        ],
        'eligibility_rules': {
            'business_type_allowed': ['non-farm'],
            'mudra_stages_allowed': ['Shishu', 'Kishore', 'Tarun'],
            'allow_default': False,
            'loan_limits': {
                'Shishu':  {'limit': '50,000',     'rate': 8.5},
                'Kishore': {'limit': '5,00,000',   'rate': 9.0},
                'Tarun':   {'limit': '10,00,000',  'rate': 9.5},
            }
        },
        'required_documents': [
            {
                'field_id': 'aadhaar',
                'label': 'Aadhaar Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'pan_card',
                'label': 'PAN Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'business_proof',
                'label': 'Business Proof (Udyam/Shop License/GST)',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'address_proof',
                'label': 'Business Address Proof (Utility Bill/Rent Agreement)',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
        ],
        'interest_rate': 8.5,
        'scheme_type': 'loan',
    },

    # ── 3. RURAL HOUSING LOAN (PMAY-G) ───────────────────
    'Rural Housing Loan': {
        'required_fields': [
            'applicant_name',
            'phone',
            'secc_listed',
            'previous_pmay',
            'house_condition',
            'previous_default'
        ],
        'eligibility_rules': {
            'secc_listed': True,
            'previous_pmay': False,
            'house_conditions_allowed': ['none', 'kutcha'],
            'allow_default': False,
        },
        'required_documents': [
            {
                'field_id': 'aadhaar',
                'label': 'Aadhaar Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'secc_letter',
                'label': 'SECC 2011 Acknowledgement Letter',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'house_photo',
                'label': 'Current House Photo (showing condition)',
                'accepted_types': ['image'],
                'mandatory': True
            },
            {
                'field_id': 'ration_card',
                'label': 'Ration Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
        ],
        'interest_rate': 6.5,
        'scheme_type': 'loan',
    },

    # ── 4. NABARD FARM LOAN ───────────────────────────────
    'NABARD Farm Loan': {
        'required_fields': [
            'applicant_name',
            'phone',
            'farmer_type',
            'land_acres',
            'crop_name',
            'bank_account_rrb',
            'previous_default'
        ],
        'eligibility_rules': {
            'farmer_types_allowed': ['owner', 'tenant', 'sharecropper'],
            'min_land_acres': 0.1,
            'require_crop': True,
            'require_rrb_account': True,
            'allow_default': False,
        },
        'required_documents': [
            {
                'field_id': 'aadhaar',
                'label': 'Aadhaar Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'land_records',
                'label': 'Land Records (Patta/Khata)',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['owner']
            },
            {
                'field_id': 'tenancy_agreement',
                'label': 'Tenancy Agreement',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['tenant', 'sharecropper']
            },
            {
                'field_id': 'crop_certificate',
                'label': 'Crop Sowing Certificate (from Patwari/VLO)',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'bank_passbook',
                'label': 'Bank Passbook (RRB or Cooperative Bank)',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
        ],
        'interest_rate': 5.5,
        'scheme_type': 'loan',
    },

    # ── 5. PM FASAL BIMA (CROP INSURANCE) ────────────────
    'PM Fasal Bima': {
        'required_fields': [
            'applicant_name',
            'phone',
            'farmer_type',
            'land_acres',
            'crop_name',
            'crop_season',
            'enrolled_before_cutoff'
        ],
        'eligibility_rules': {
            'farmer_types_allowed': ['owner', 'tenant', 'sharecropper'],
            'min_land_acres': 0.1,
            'require_crop': True,
            'crop_seasons_allowed': ['Kharif', 'Rabi', 'Zaid'],
            'require_enrollment': True,
        },
        'required_documents': [
            {
                'field_id': 'aadhaar',
                'label': 'Aadhaar Card',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
            {
                'field_id': 'land_records',
                'label': 'Land Records (Patta/Khata)',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['owner']
            },
            {
                'field_id': 'tenancy_agreement',
                'label': 'Tenancy Agreement',
                'accepted_types': ['pdf', 'image'],
                'mandatory_for': ['tenant', 'sharecropper']
            },
            {
                'field_id': 'crop_certificate',
                'label': 'Crop Sowing Certificate',
                'accepted_types': ['pdf', 'image'],
                'mandatory': True
            },
        ],
        'premium_rate': {
            'Kharif': 2.0,
            'Rabi': 1.5,
            'Zaid': 2.0,
        },
        'scheme_type': 'insurance',
    },

}

# ============================================================
# HOW TO ADD A NEW SCHEME:
# Just copy any scheme block above and add a new key below.
# Example:
#
# SCHEME_RULES['PM Kisan FPO Loan'] = {
#     'required_fields': [...],
#     'eligibility_rules': {...},
#     'required_documents': [...],
#     'interest_rate': 7.0,
#     'scheme_type': 'loan',
# }
# ============================================================