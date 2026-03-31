# ============================================================
# banks_config.py
# Rural Loan Eligibility System
# Static list of banks supporting each scheme
# To add a new bank: just add a new dict to the scheme list
# ============================================================

SCHEME_BANKS = {

    # ── 1. KISAN CREDIT CARD ──────────────────────────────
    'Kisan Credit Card': [
        {
            'name': 'State Bank of India',
            'type': 'Nationalised Bank',
            'toll_free': '1800-11-2211',
            'website': 'https://sbi.co.in'
        },
        {
            'name': 'Punjab National Bank',
            'type': 'Nationalised Bank',
            'toll_free': '1800-180-2222',
            'website': 'https://pnbindia.in'
        },
        {
            'name': 'Karnataka Gramin Bank',
            'type': 'Regional Rural Bank',
            'toll_free': '1800-425-1906',
            'website': 'https://kgb.co.in'
        },
        {
            'name': 'NABARD',
            'type': 'Development Bank',
            'toll_free': '1800-22-0000',
            'website': 'https://nabard.org'
        },
    ],

    # ── 2. PM MUDRA LOAN ──────────────────────────────────
    'PM Mudra Loan': [
        {
            'name': 'State Bank of India',
            'type': 'Nationalised Bank',
            'toll_free': '1800-11-2211',
            'website': 'https://sbi.co.in'
        },
        {
            'name': 'Bank of Baroda',
            'type': 'Nationalised Bank',
            'toll_free': '1800-258-4455',
            'website': 'https://bankofbaroda.in'
        },
        {
            'name': 'Canara Bank',
            'type': 'Nationalised Bank',
            'toll_free': '1800-425-0018',
            'website': 'https://canarabank.com'
        },
        {
            'name': 'Union Bank of India',
            'type': 'Nationalised Bank',
            'toll_free': '1800-22-2244',
            'website': 'https://unionbankofindia.co.in'
        },
    ],

    # ── 3. RURAL HOUSING LOAN (PMAY-G) ───────────────────
    'Rural Housing Loan': [
        {
            'name': 'National Housing Bank',
            'type': 'Housing Finance',
            'toll_free': '1800-11-3377',
            'website': 'https://nhb.org.in'
        },
        {
            'name': 'State Bank of India',
            'type': 'Nationalised Bank',
            'toll_free': '1800-11-2211',
            'website': 'https://sbi.co.in'
        },
        {
            'name': 'LIC Housing Finance',
            'type': 'Housing Finance',
            'toll_free': '1800-258-5678',
            'website': 'https://lichousing.com'
        },
        {
            'name': 'HDFC Bank',
            'type': 'Private Bank',
            'toll_free': '1800-202-6161',
            'website': 'https://hdfc.com'
        },
    ],

    # ── 4. NABARD FARM LOAN ───────────────────────────────
    'NABARD Farm Loan': [
        {
            'name': 'NABARD',
            'type': 'Development Bank',
            'toll_free': '1800-22-0000',
            'website': 'https://nabard.org'
        },
        {
            'name': 'State Bank of India',
            'type': 'Nationalised Bank',
            'toll_free': '1800-11-2211',
            'website': 'https://sbi.co.in'
        },
        {
            'name': 'Karnataka Gramin Bank',
            'type': 'Regional Rural Bank',
            'toll_free': '1800-425-1906',
            'website': 'https://kgb.co.in'
        },
        {
            'name': 'Punjab National Bank',
            'type': 'Nationalised Bank',
            'toll_free': '1800-180-2222',
            'website': 'https://pnbindia.in'
        },
    ],

    # ── 5. PM FASAL BIMA ──────────────────────────────────
    'PM Fasal Bima': [
        {
            'name': 'Agriculture Insurance Company of India',
            'type': 'Government Insurance',
            'toll_free': '1800-116-515',
            'website': 'https://aicofindia.com'
        },
        {
            'name': 'SBI General Insurance',
            'type': 'General Insurance',
            'toll_free': '1800-22-1111',
            'website': 'https://sbigeneral.in'
        },
        {
            'name': 'Bajaj Allianz General Insurance',
            'type': 'General Insurance',
            'toll_free': '1800-209-5858',
            'website': 'https://bajajallianz.com'
        },
        {
            'name': 'HDFC ERGO General Insurance',
            'type': 'General Insurance',
            'toll_free': '1800-266-0700',
            'website': 'https://hdfcergo.com'
        },
    ],

}

# ============================================================
# HOW TO ADD A NEW BANK TO ANY SCHEME:
# Just add a new dict to the scheme list. Example:
#
# SCHEME_BANKS['Kisan Credit Card'].append({
#     'name': 'Your Bank Name',
#     'type': 'Bank Type',
#     'toll_free': '1800-XXX-XXXX',
#     'website': 'https://yourbank.com'
# })
# ============================================================