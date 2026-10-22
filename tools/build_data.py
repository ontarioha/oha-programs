"""Builds the single program list (programs.json) and the city lookup (municipalities.json).

Starts from the Version 12 records, converts region names to explicit tokens
(city:X / region:X / Ontario / Canada), moves the illustrative values into each
record, applies the October 2026 verification updates, and adds Ring 1 programs.
"""
import json, sys, pathlib

SRC = pathlib.Path(sys.argv[1])          # folder with Version 12 programs.json / municipalities.json
OUT = pathlib.Path(sys.argv[2])          # output folder
HERE = pathlib.Path(__file__).parent
TODAY = "2026-10-21"
ALL = ["owner", "renter", "other"]

old = json.load(open(SRC / "programs.json"))
vals = json.load(open(HERE / "demo_values.json"))

REGION_MAP = {
    "Ontario": "Ontario", "Canada": "Canada",
    "Niagara Region": "region:Niagara", "Fort Erie": "city:Fort Erie",
    "Toronto": "city:Toronto", "Hamilton": "city:Hamilton",
    "Simcoe": "region:Simcoe", "Waterloo": "region:Waterloo",
    "Cambridge": "city:Cambridge", "Kitchener": "city:Kitchener",
}

progs = {}
for p in old:
    p = dict(p)
    p["regions"] = [REGION_MAP[r] for r in p["regions"]]
    v = vals.get(p["id"])
    p["value"] = v or {"monthly": 0, "annual": 0, "once": 0, "type": "project", "note": "Unverified illustration"}
    p.pop("estimated_value", None); p.pop("estimate_type", None)
    p["checked"] = None
    p["source"] = p["url"]
    p.setdefault("phone", "")
    progs[p["id"]] = p

def upd(pid, **kw):
    progs[pid].update(kw)
    progs[pid]["checked"] = TODAY

def val(m=0, a=0, o=0, t="cash", note=""):
    return {"monthly": m, "annual": a, "once": o, "type": t, "note": note}

def add(pid, **kw):
    rec = {"id": pid, "housing": ALL, "phone": "", "checked": TODAY}
    rec.update(kw)
    rec.setdefault("source", rec["url"])
    rec.setdefault("value", val(t="project", note="No illustration set; review program terms"))
    progs[pid] = rec

# ---------- Province-wide and federal: verified Oct 21, 2026 ----------
upd("oesp",
    amount="Monthly electricity bill credit of $35–$75 (up to $52–$113 for electric heat, certain medical devices or Indigenous households).",
    requirements="Electricity account holder. After-tax household income limits by household size, e.g. 1–2 people up to $38,000 for the full $45; up to $71,000 for 5+ people. Must reapply when asked.",
    action="Apply online at ontarioelectricitysupport.ca or through a local intake agency. Have a recent bill, birthdates and SINs for adults.",
    url="https://ontarioelectricitysupport.ca/", source="https://oeb.ca/node/121", phone="1-855-831-8151",
    status="Open, year-round.", verified="Official OEB page checked Oct 21, 2026.")
upd("leap",
    amount="One-time emergency grant toward arrears: up to $650 (electricity or gas), up to $780 for electrically heated homes. Paid to the utility; never more than owed.",
    requirements="Behind on electricity or gas bill. After-tax household income under $38,000 (1 person), $54,000 (2), $65,000 (3–4), $71,000 (5–7). Emergency use only.",
    action="Contact the local LEAP intake agency (see local listing for this area). Bring ID, bills, disconnection notice, proof of income and housing, latest bank statement.",
    url="https://www.oeb.ca/consumer-information-and-protection/bill-assistance-programs/low-income-energy-assistance-program",
    status="Open, year-round, while local funds last.", verified="Official OEB page checked Oct 21, 2026.",
    value=val(o=650, t="cash", note="Published maximum; capped at amount owed. May overlap other local emergency energy funds"))
upd("seniortax",
    amount="Up to $500 per year toward property tax.",
    requirements="Age 64+ by Dec 31 of the prior year, owns and lives in the home, paid Ontario property tax. Full grant if adjusted family net income is $35,000 or less (single) / $45,000 or less (couple); reduced above that; none at $50,000 (single) / $60,000 (couple).",
    action="Claim on the ON-BEN form with the annual tax return (line 61120).",
    url="https://www.ontario.ca/page/senior-homeowners-property-tax-grant", status="Open; claimed yearly with tax return.",
    verified="Official Ontario page checked Oct 21, 2026.")
upd("gis", regions=["Canada"],
    amount="Up to $1,138.90/month for a single senior with income under $23,112 (Oct–Dec 2026 rates).",
    requirements="65+, receives OAS, low income. Amount depends on income and marital status; most people are enrolled automatically.",
    action="Check whether the client already receives GIS. If not, apply through Service Canada.",
    url="https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement.html",
    source="https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement/benefit-amount.html",
    phone="1-800-277-9914", status="Ongoing federal benefit.", verified="Official Canada.ca page checked Oct 21, 2026.")
upd("gains",
    amount="Up to $92/month (July 2026–June 2027 benefit year).",
    requirements="65+, receives OAS and GIS, private income up to $4,416 (single) or $8,832 (couple).",
    action="Paid automatically to GIS recipients who file taxes by April 30. If not receiving GIS, apply for GIS first.",
    url="https://www.ontario.ca/page/guaranteed-annual-income-system-payments-seniors", status="Ongoing provincial benefit.",
    verified="Official Ontario page checked Oct 21, 2026.")
upd("trillium",
    amount="Energy and Property Tax Credit up to $1,488/year for seniors 65+ or $1,307 for ages 18–64 (2026 benefit year), plus the sales tax credit.",
    requirements="Ontario resident who paid rent or property tax; income-tested. Must file a tax return and the ON-BEN form.",
    action="File the annual tax return with ON-BEN by April 30. Free tax clinics can help.",
    url="https://www.ontario.ca/page/ontario-trillium-benefit", status="Ongoing; claimed yearly.",
    verified="Official Ontario page checked Oct 21, 2026.")
upd("access", level="Federal", regions=["Canada"],
    amount="Tax credit of 15% on up to $20,000 of eligible renovation costs per year (up to $3,000).",
    requirements="Homeowner (or supporting relative) aged 65+ or eligible for the Disability Tax Credit. Renovation must improve safety or access.",
    action="Keep receipts; claim on line 31285 of the tax return.", status="Ongoing.",
    verified="Long-standing CRA credit; amounts per CRA line 31285. Re-check yearly.")
upd("eap", name="Energy Affordability Program (Save on Energy)",
    amount="Free in-home energy assessment and upgrades: efficient fridge/freezer, window A/C, dehumidifier, insulation and draft-proofing and heat pumps for electric/oil-heated homes; or a free energy-saving kit by mail.",
    requirements="Utility account holder (owner or renter). Before-tax income under $48,220 (1 person), $68,193 (2), $83,518 (3), $96,439 (4) for full upgrades — or received OESP, LEAP, GIS, OW or ODSP in the past 12 months. Higher limits for kits.",
    action="Apply online or call 1-844-770-3148; a provider calls back within 3 business days.",
    url="https://saveonenergy.ca/For-Your-Home/Energy-Affordability-Program", phone="1-844-770-3148",
    status="Open.", verified="Official Save on Energy page checked Oct 21, 2026.")
for k in ["eap-kit","eap-fridge","eap-freezer","eap-ac","eap-dehumid","eap-insulation","eap-heatpump"]:
    upd(k, url="https://saveonenergy.ca/For-Your-Home/Energy-Affordability-Program", status="Open.",
        verified="Program confirmed Oct 21, 2026; dollar figure is an illustrative installed value.")
upd("cdcp", regions=["Canada"],
    amount="Covers a share of dental care costs (co-pay depends on income).",
    requirements="Adjusted family net income under $90,000, no access to private dental insurance, filed taxes, Canadian resident.",
    action="Apply through Canada.ca; 2026–2027 applications are open.",
    url="https://www.canada.ca/en/services/benefits/dental/dental-care-plan.html",
    source="https://www.canada.ca/en/services/benefits/dental/dental-care-plan/qualify.html",
    status="Open for 2026–2027.", verified="Official Canada.ca pages checked Oct 21, 2026.")
upd("import-5", name="Old Age Security (OAS) pension", level="Federal", regions=["Canada"],
    amount="Up to $762.50/month (ages 65–74) or $838.75/month (75+), Oct–Dec 2026.",
    requirements="65+, residency requirements. Often already received; check before counting it as new money.",
    action="Confirm the client receives OAS; if not, apply through Service Canada.",
    url="https://www.canada.ca/en/services/benefits/publicpensions/old-age-security.html",
    source="https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/payments.html",
    phone="1-800-277-9914", status="Ongoing federal benefit.", verified="Official Canada.ca page checked Oct 21, 2026.")
upd("import-9", name="Home Renovation Savings Program (overview)",
    amount="Rebates: heat pumps up to $12,000, solar + battery up to $10,000, insulation up to $7,700, attic insulation up to $1,250, smart thermostat $125, appliances up to $200 and more.",
    requirements="Rules vary by rebate; some need a pre-upgrade energy assessment. Do not start work before checking the rules.",
    action="Review rebates and register at homerenovationsavings.ca.",
    url="https://www.homerenovationsavings.ca/",
    status="Open. Official site lists no end date; a 2025 report said it was extended through Nov 2026 — confirm before promising.",
    verified="Official site checked Oct 21, 2026.")
upd("import-10", name="Enbridge Gas Home Winterproofing Program (overview)",
    amount="Free home energy assessment, insulation, draft-proofing and a smart thermostat, plus Energy Affordability Program upgrades.",
    requirements="Enbridge Gas account in the applicant's name; gas-heated home; before-tax income under $48,220 (1), $68,193 (2), $83,518 (3), $96,439 (4) — or receives OW, ODSP, GIS or OESP. Renters need landlord permission. Not for apartments/condos.",
    action="Apply online or call 1-844-770-3148 with a recent Enbridge bill and income proof.",
    url="https://www.enbridgegas.com/ontario/rebates-energy-conservation/home-winterproofing-program", phone="1-844-770-3148",
    status="Open.", verified="Official Enbridge page checked Oct 21, 2026.")
for k in ["hwp-insulation","hwp-draft","hwp-thermostat"]:
    upd(k, status="Open.", verified="Program confirmed Oct 21, 2026; dollar figure is an illustrative installed value.")
for k in ["hrs-heatpump","hrs-solar","hrs-insulation","hrs-attic","hrs-thermostat","hrs-appliances","hrs-airseal","hrs-waterheater","hrs-assessment"]:
    upd(k, status="Open; confirm amounts at homerenovationsavings.ca.", verified="Rebate list checked Oct 21, 2026.")
upd("import-12", name="Multigenerational Home Renovation Tax Credit", level="Federal", regions=["Canada"],
    amount="Refundable credit of 15% on up to $50,000 of eligible costs (up to $7,500) to build a secondary unit for a senior (65+) or adult relative with a disability.",
    requirements="Unit must be for an eligible senior or adult with a disability to live with a relative.",
    action="Keep receipts; claim on the tax return for the year the work is completed.",
    url="https://www.canada.ca/cra-mhrtc", status="Ongoing.", verified="CRA program page link updated Oct 21, 2026.")
upd("import-13", name="Home and Vehicle Modification Program (March of Dimes)",
    amount="Funding for home and vehicle modifications for people with mobility disabilities. Households over $38,000 income may need to contribute.",
    requirements="Ontario resident with a disability that substantially limits mobility and daily living; household income within program limits; other funding sources used first.",
    action="Apply through March of Dimes Canada.",
    url="https://www.marchofdimes.ca/en-ca/programs/am/hvmp/Pages/HVMP-How-to-Apply.aspx",
    source="https://www.ontario.ca/page/home-and-vehicle-modification-program",
    status="Open; funding limited.", verified="Official Ontario page checked Oct 21, 2026.")

add("cdb", name="Canada Disability Benefit", level="Federal", regions=["Canada"], categories=["income","access"],
    amount="Up to $204.20/month (July 2026–June 2027).",
    requirements="Age 18–64, approved for the Disability Tax Credit, filed 2025 taxes. Income-tested. Must apply; not automatic.",
    action="If the client has the Disability Tax Credit, apply through Service Canada. If not, start with the Disability Tax Credit.",
    url="https://www.canada.ca/en/services/benefits/disability/canada-disability-benefit.html",
    source="https://www.narcity.com/canada-disability-benefit-payment-date-july-2026-amount-increase",
    status="Open.", verified="Amount from July 2026 news coverage; official page to be confirmed in weekly check.",
    value=val(m=204, t="cash", note="Published maximum; reduced by income"))
add("dtc", name="Disability Tax Credit (DTC)", level="Federal", regions=["Canada"], categories=["income","access","tax"],
    amount="Non-refundable tax credit. Also the gateway to the Canada Disability Benefit, RDSP and many other programs.",
    requirements="Severe and prolonged impairment certified by a medical practitioner (form T2201).",
    action="Have a medical practitioner complete form T2201 and submit to CRA.",
    url="https://www.canada.ca/en/revenue-agency/services/tax/individuals/segments/tax-credits-deductions-persons-disabilities/disability-tax-credit.html",
    status="Ongoing.", verified="Long-standing CRA program; link to be confirmed in weekly check.",
    value=val(t="tax", note="Value depends on tax payable; unlocks other benefits"))
add("osdcp", name="Ontario Seniors Dental Care Program", level="Ontario", regions=["Ontario"], categories=["health"],
    amount="Free routine dental care for eligible seniors.",
    requirements="65+, Ontario resident, net income $25,480 or less (single) or $42,290 or less (couple), no other dental benefits except CDCP.",
    action="Apply online at ontario.ca/SeniorsDental, by mail, or at a public health unit.",
    url="https://www.ontario.ca/SeniorsDental", source="https://www.ontario.ca/files/2026-07/moh-seniors-dental-en-2026-07-29.pdf",
    phone="1-833-207-4435", status="Open.", verified="Official Ontario fact sheet (July 2026) checked Oct 21, 2026.",
    value=val(o=600, t="inkind", note="Illustrative value of covered care; not cash"))
add("oschtc", name="Ontario Seniors Care at Home Tax Credit", level="Ontario", regions=["Ontario"], categories=["tax","health","income"],
    amount="Refundable credit of 25% of up to $6,000 in medical expenses (up to $1,500).",
    requirements="Age 70+ (or spouse 70+). Reduced when family net income is over $35,000; phased out by about $65,000.",
    action="Claim on the annual tax return.",
    url="https://www.ontario.ca/page/ontario-seniors-care-home-tax-credit", status="Ongoing.",
    verified="Official Ontario page checked Oct 21, 2026.",
    value=val(o=1500, t="tax", note="Published maximum; requires eligible medical expenses"))
add("adp", name="Assistive Devices Program (ADP)", level="Ontario", regions=["Ontario"], categories=["access","health"],
    amount="Usually pays 75% of the approved price of equipment such as wheelchairs, walkers and hearing aids (more for OW/ODSP recipients).",
    requirements="Ontario health card; long-term physical disability (6+ months); meets device criteria. Income not considered.",
    action="Start with the client's health care provider or an ADP-registered authorizer.",
    url="https://www.ontario.ca/page/assistive-devices-program", phone="416-327-8804", status="Ongoing.",
    verified="Official Ontario page checked Oct 21, 2026.",
    value=val(o=1000, t="project", note="Illustrative; depends on device"))
add("ow-emergency", name="Ontario Works — Emergency Assistance", level="Ontario", regions=["Ontario"], categories=["housing","community","debt","food"],
    amount="Short-term financial help in a crisis (e.g., at risk of losing housing).",
    requirements="Not already on Ontario Works or ODSP; in a crisis or emergency; financial eligibility applies.",
    action="Apply online or call the local Ontario Works office.",
    url="https://www.ontario.ca/page/apply-emergency-assistance", status="Ongoing.",
    verified="Official page referenced by Region of Waterloo Oct 21, 2026.",
    value=val(t="cash", note="Amount varies; no illustration set"))

# ---------- Waterloo Region ----------
WR_TOWNS = ["city:Woolwich","city:Wilmot","city:Wellesley","city:North Dumfries"]
upd("waterloo-renovates",
    amount="Up to $25,000 forgivable loan for repairs (forgiven over 10 years), or up to $25,000 for accessibility work including up to $5,000 as a grant.",
    requirements="Own and live in the home in Waterloo Region; no other property; home assessed at $600,000 or less; gross household income up to $41,210 (1 person), $51,204 (2), $63,072 (3), $76,577 (4) — or OW/ODSP only. Taxes and mortgage up to date; full home insurance.",
    action="DEADLINE: 2026 fact sheet says apply before Nov 15, 2026 (another line says Dec 1) — submit by Nov 15 to be safe. Email OntarioRenovates@regionofwaterloo.ca.",
    url="https://www.regionofwaterloo.ca/programs-and-services/employment-and-financial-supports/financial-support-for-renters-and-homeowners/funding-for-home-repairs/",
    source="https://www.regionofwaterloo.ca/media/tzsc1ib2/ontario_renovates_fact_sheet_row_4195350_2026.pdf",
    phone="519-575-4400", status="Open for 2026; limited funding; deadline Nov 15, 2026.",
    verified="Official page and 2026 fact sheet checked Oct 21, 2026.")
upd("waterloo-suites",
    amount="Forgivable funding to create an affordable secondary suite (amount set in the Region's fact sheet).",
    requirements="Single-family home assessed at $600,000 or less; self-contained legal unit; rent and tenant income below Region maximums.",
    action="Ongoing intake while funding lasts. Email OntarioRenovates@regionofwaterloo.ca.",
    phone="519-575-4400", status="Open; limited funding.", verified="Official page checked Oct 21, 2026.")
upd("cambridge-tax-deferral",
    amount="Defers part of the yearly property tax increase (minimum $50), interest-free, until the home is sold.",
    requirements="Senior receiving OAS and GIS, or person receiving ODSP. Own and occupy the home for at least 1 year. Taxes must be current.",
    action="Apply each year after final tax bills are issued (deadline Nov 1). Pick up the form at the Tax Office, 50 Dickson St.",
    phone="519-623-1340", status="Open; annual deadline Nov 1.", verified="Official City page and Regional policy checked Oct 21, 2026.")
upd("kitchener-tax-deferral",
    amount="Defers the part of a reassessment tax increase above 3%, interest-free, until the home is sold.",
    requirements="Senior receiving GIS, or person receiving ODSP. Own and occupy the home for at least 1 year. Taxes must be current. Renew yearly.",
    action="DEADLINE Nov 1, 2026. Mail the form to City of Kitchener Revenue, PO Box 1113, or drop at City Hall.",
    phone="519-741-2450", status="Open; annual deadline Nov 1.", verified="Official City page checked Oct 21, 2026.")
add("waterloo-city-tax-deferral", name="City of Waterloo — Seniors and Disability Property Tax Deferral", level="Municipal",
    regions=["city:Waterloo"], categories=["tax"], housing=["owner"],
    amount="Defers the part of a reassessment tax increase above 3%, interest-free, until the home is sold.",
    requirements="Senior receiving GIS, or person receiving ODSP. Own and occupy the home for at least 1 year. Renew yearly.",
    action="DEADLINE Nov 1, 2026. Email the form to revenue@waterloo.ca or drop off at City Hall.",
    url="https://www.waterloo.ca/water-and-tax-billing/tax-billing/check-if-you-qualify-for-a-tax-rebate-or-deferral/", source="https://www.waterloo.ca/media/wr3b1rf0/tax-deferral-policy.pdf",
    phone="519-747-8718", status="Open; annual deadline Nov 1.", verified="Official City page and Regional policy checked Oct 21, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred; repaid on sale"))
add("waterloo-towns-tax-deferral", name="Waterloo Region townships — Seniors and Disability Property Tax Deferral", level="Municipal",
    regions=WR_TOWNS, categories=["tax"], housing=["owner"],
    amount="Defers the part of a reassessment tax increase above 3%, interest-free, until the home is sold.",
    requirements="Senior receiving GIS, or person receiving ODSP. Own and occupy the home for at least 1 year. Renew yearly.",
    action="DEADLINE Nov 1, 2026. Apply to the township office (Woolwich, Wilmot, Wellesley or North Dumfries).",
    url="https://www.wilmot.ca/en/township-office/resources/Documents/Tax---Regional-Policy-on-Tax-Deferral-for-Low-Income-Seniors-or-Disabled-Persons.pdf",
    links={"Wellesley": "https://www.wellesley.ca/media/kqzhqide/regional-tax-relief.pdf"},
    status="Open; annual deadline Nov 1.", verified="Regional policy (By-law 98-048) checked Oct 21, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred; repaid on sale"))
upd("retrofitwr-cambridge", name="RetrofitWR — Low-interest Energy Retrofit Loans and Heat Pump Incentives",
    regions=["city:Cambridge","city:North Dumfries"],
    amount="2.5% loans repaid on the GrandBridge Energy bill, plus $2,500 for a ducted heat pump or $1,000 per mini-split (up to $2,500). Extra support for income-eligible households.",
    requirements="Homeowner and GrandBridge Energy customer in Cambridge or North Dumfries. Work must not start before approval.",
    action="Contact a RetrofitWR Energy Coach at RetrofitWR.ca.",
    status="Active 2026–2030.", verified="Official Region page checked Oct 21, 2026.")
upd("retrofitwr-coach", amount="Free independent Energy Coach to plan upgrades and find rebates.",
    requirements="Homeowner in Waterloo Region.", action="Sign up at RetrofitWR.ca.",
    status="Active 2026–2030.", verified="Official Region page checked Oct 21, 2026.")
upd("waterloo-home-water-review", amount="Free 45–60 minute home water review to cut water bills.",
    requirements="Owner; single, semi, townhouse or duplex with its own meter; uses at least 5.5 m³ per person per month; no previous review.",
    action="Book online through the Region's page.", phone="519-575-4400", status="Open.",
    verified="Official Region page checked Oct 21, 2026.")
add("waterloo-softener-rebate", name="Waterloo Region — Water Softener Plumbing Rebate", level="Regional",
    regions=["region:Waterloo"], categories=["utility"], housing=["owner"],
    amount="$50 one-time rebate for re-plumbing a softener to treat hot water only.",
    requirements="Single, semi or townhouse with a salt-based softener. Plumbing change required, not just a new softener.",
    action="Register, submit a water hardness result, then send receipts.",
    url="https://forms.regionofwaterloo.ca/Transportation/Water/Conservation/Water-Softener-Plumbing-Rebate-Program",
    source="https://www.regionofwaterloo.ca/programs-and-services/water-and-wastewater/conserving-water/residential-water-conservation/",
    phone="519-575-4400", status="Open, continuous intake.", verified="Region page and program details checked Oct 21, 2026.",
    value=val(o=50, t="cash", note="Published rebate"))
add("kitchener-stormwater-credit", name="Kitchener — Residential Stormwater Credit", level="Municipal",
    regions=["city:Kitchener"], categories=["utility"], housing=["owner"],
    amount="Ongoing credit of 20%, 30% or 45% off the monthly stormwater charge.",
    requirements="Home captures stormwater with rain barrels, cisterns, rain gardens or permeable pavers.",
    action="Apply online with a utility bill and measurements, or email stormwater@kitchener.ca.",
    url="https://www.kitchener.ca/en/water-and-environment/stormwater-credits.aspx", status="Open.",
    verified="Official City page checked Oct 21, 2026.",
    value=val(a=60, t="bill", note="Illustrative yearly bill credit"))
add("wreap", name="Waterloo Region Energy Assistance Program (WREAP) and local LEAP intake", level="Regional",
    regions=["region:Waterloo"], categories=["utility","community"],
    amount="One-time grant toward electricity arrears (summary says up to $500 a year). Gas customers use LEAP (up to $650).",
    requirements="Behind on electricity (Enova Power or GrandBridge Energy). Social assistance or after-tax income under LEAP limits. Talk to the utility about a payment plan first.",
    action="Electricity: call 519-883-2100, option 1. Enbridge gas: LEAP line 1-855-487-5327. Kitchener Utilities gas: 519-883-2100.",
    url="https://www.regionofwaterloo.ca/programs-and-services/employment-and-financial-supports/financial-support-for-renters-and-homeowners/utility-bill-help/",
    phone="519-883-2100", status="Open.", verified="Official Region page checked Oct 21, 2026.",
    value=val(o=500, t="cash", note="Published maximum; overlaps LEAP — do not add both"))
upd("import-20", name="City of Waterloo — Additional Residential Unit (ARU) Grant", level="Municipal", regions=["city:Waterloo"],
    housing=["owner"],
    amount="Up to 50% of costs: up to $30,000 for a detached unit or $20,000 for an interior unit.",
    requirements="Construction not started. Rent at or below 80% of CMHC average (2026: 1-bed $1,236, 2-bed $1,466) to an eligible tenant for 5 years.",
    action="Apply online at forms.waterloo.ca before starting; email ARU@waterloo.ca.",
    url="https://www.waterloo.ca/building-and-renovating/additional-residential-units-arus/apply-for-the-aru-grant/",
    status="Open while funds last.", verified="Official City page checked Oct 21, 2026.",
    value=val(o=20000, t="project", note="Published maximum for interior unit; requires construction spending"))
add("kitchener-adu-grant", name="Kitchener — Additional Dwelling Unit (ADU) Grant", level="Municipal",
    regions=["city:Kitchener"], categories=["adu"], housing=["owner"],
    amount="Covers development charges on new ADUs: 100% of education DCs for units 2–3; 50–100% of City, Regional and education DCs for a 4th unit.",
    requirements="Single, semi or street townhouse lot; building permit on or after Jan 5, 2026.",
    action="Email the application to HousingIncentives@kitchener.ca.",
    url="https://www.kitchener.ca/taxes-utilities-and-finance/grants-and-incentives/the-missing-middle-and-affordable-housing-community-improvement-plan/",
    status="Open since Jan 19, 2026, while funds last.", verified="Official City page checked Oct 21, 2026.",
    value=val(o=5000, t="project", note="Illustrative; depends on development charges"))
add("waterloo-atp", name="Grand River Transit — Affordable Transit Program", level="Regional",
    regions=["region:Waterloo"], categories=["transport"],
    amount="50% off GRT fares for the whole household.",
    requirements="Waterloo Region resident with household income below the program limit, or on OW/ODSP.",
    action="Apply online at the Region's ATP portal or call 519-883-2100 ext. 3.",
    url="https://www.grt.ca/en/fares-passes/affordable-transit-program.aspx", source="https://benefitswayfinder.org/ontario/affordable-transit-program",
    phone="519-883-2100", status="Open.", verified="Program details checked Oct 21, 2026.",
    value=val(a=600, t="bill", note="Illustrative yearly fare savings"))

# ---------- Simcoe County, Barrie, Orillia ----------
SIMCOE_TOWNS = ["Adjala-Tosorontio","Bradford West Gwillimbury","Clearview","Collingwood","Essa","Innisfil","Midland",
    "New Tecumseth","Oro-Medonte","Penetanguishene","Ramara","Severn","Springwater","Tay","Tiny","Wasaga Beach"]
add("simcoe-renovates", name="County of Simcoe — Ontario Renovates (Home Repair and Accessibility)", level="Regional",
    regions=["region:Simcoe"], categories=["repairs","access"], housing=["owner"],
    amount="Up to $15,000 forgivable loan (forgiven over 10 years); accessibility work up to $5,000 is a grant.",
    requirements="Low-to-moderate income homeowner; gross household income $91,000 or less; home value $799,000 or less. Urgent repairs: roof, structure, plumbing/septic, electrical, heating, fire safety, mould.",
    action="Download the application package from the County page; email iah@simcoe.ca. Year-round intake; may be waitlisted.",
    url="https://simcoe.ca/residents/housing/affordable-housing-programs/",
    source="https://simcoe.ca/wp-content/uploads/2025/07/SCS-Ontario-Renovates-Fact-Sheet-2025–2026.pdf",
    phone="705-725-7215 ext. 1119", status="Open; limited funding, first come first served.",
    verified="Official County page and 2025–26 fact sheet checked Oct 21, 2026.",
    value=val(o=15000, t="financing", note="Published maximum; forgivable loan, not cash"))
upd("import-19", name="County of Simcoe — Secondary Suites Program", level="Regional", regions=["region:Simcoe"], housing=["owner"],
    amount="Up to $50,000 per unit to create a secondary or garden suite.",
    requirements="Rent and tenant income must stay under the County's 2025–26 maximums.",
    action="Download the application package from the County page; email iah@simcoe.ca.",
    url="https://simcoe.ca/residents/housing/affordable-housing-programs/", phone="705-735-6901 ext. 1360",
    status="Open year-round; limited funding.", verified="Official County page checked Oct 21, 2026.",
    value=val(o=50000, t="project", note="Published maximum; requires construction and affordability terms"))
add("barrie-bonus", name="Barrie Bonus — $15,000 top-up for Affordable ARUs", level="Municipal",
    regions=["city:Barrie"], categories=["adu"], housing=["owner"],
    amount="One-time $15,000 on top of County Secondary Suites funding.",
    requirements="Approved for County of Simcoe Secondary Suites funding; Barrie property on city water and sewer; taxes in good standing.",
    action="Apply to the County program first; County staff pass on the Barrie Bonus form. Questions: HousingCIP@barrie.ca.",
    url="https://www.barrie.ca/node/14737", phone="705-739-4220 ext. 4416", status="Open; limited funding.",
    verified="Official City page checked Oct 21, 2026.",
    value=val(o=15000, t="project", note="Published amount; only with County approval"))
add("simcoe-retention", name="County of Simcoe — Housing Retention Program", level="Regional",
    regions=["region:Simcoe"], categories=["housing","utility","debt","community"],
    amount="Up to $1,500 (singles/couples) or $3,500 (families) over 24 months toward rent or mortgage arrears, utility arrears, or moving costs.",
    requirements="Simcoe County resident. Utility arrears need a disconnection notice and a LEAP application; rent arrears need an N4. Housing costs must be sustainable. Homeowners: mortgage arrears listed — confirm with County.",
    action="Apply by phone: 705-722-3132 ext. 1833.",
    url="https://simcoe.ca/residents/housing/housing-retention-program/", phone="705-722-3132 ext. 1833",
    status="Open.", verified="Official County page checked Oct 21, 2026.",
    value=val(o=1500, t="cash", note="Published maximum for singles/couples; paid to landlord/utility"))
add("simcoe-leap", name="LEAP intake — United Way Simcoe Muskoka", level="Community",
    regions=["region:Simcoe"], categories=["utility"],
    amount="Up to $650 toward gas or electricity arrears; up to $780 for electrically heated homes.",
    requirements="Low income; customer of a partner utility; behind on bills. A disconnection hold can be arranged during assessment.",
    action="Call 1-855-487-5327 (8–10 min pre-screen) or apply online.",
    url="https://www.uwsimcoemuskoka.ca/leap/", source="https://centraleasthealthline.ca/printService.aspx?id=205803",
    phone="1-855-487-5327", status="Open year-round.", verified="Health directory listing (updated Nov 2025) checked Oct 21, 2026.",
    value=val(o=650, t="cash", note="Same grant as provincial LEAP — do not add both"))
add("barrie-tax-deferral", name="Barrie — Property Tax Deferral (Seniors and ODSP)", level="Municipal",
    regions=["city:Barrie"], categories=["tax"], housing=["owner"],
    amount="Freezes property tax at the base-year amount; increases are deferred interest-free until the home is sold.",
    requirements="Owner 65+ and/or receiving ODSP; taxes paid up to date. Renew each year.",
    action="Apply online through Service Barrie by Aug 31 each year (2026 deadline passed — apply for 2027).",
    url="https://www.barrie.ca/services-payments/permits-licences-applications/property-tax-deferral-application",
    phone="705-726-4242", status="Open; annual deadline Aug 31.", verified="Official City page checked Oct 21, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred; repaid on sale"))
add("barrie-toilet-rebate", name="Barrie — Toilet Rebate", level="Municipal", regions=["city:Barrie"], categories=["utility"], housing=["owner"],
    amount="$50 water bill credit (one per home).",
    requirements="Home built before 1996; replace a toilet over 6 L/flush with 6 L or less.",
    action="Submit the City form after replacement.",
    url="https://www.barrie.ca/services-payments/permits-licences-applications/toilet-rebate", phone="705-726-4242",
    status="Open.", verified="Official City page checked Oct 21, 2026.",
    value=val(o=50, t="bill", note="Published credit"))
add("simcoe-towns-tax-relief", name="Simcoe County towns — Tax Relief for Low-income Seniors and Persons with Disabilities", level="Municipal",
    regions=["city:"+t for t in SIMCOE_TOWNS], categories=["tax"], housing=["owner"],
    amount="Up to $250 off an eligible yearly property tax increase.",
    requirements="Owner or spouse 65+ receiving GIS (or OW), or any age receiving ODSP. Principal residence; taxes must have gone up from last year.",
    action="Apply to the town tax office after final bills (e.g., Midland by Dec 31; Wasaga Beach by Dec 15).",
    url="https://simcoe.ca/government/clk/municipal-partners/",
    links={"Midland": "https://www.midland.ca/media-manager/media-pages/forms-applications/tax-relief-application-for-low-income-seniors-persons-with-disabilities/",
           "Innisfil": "https://innisfil.ca/en/living-here/resources/Documents/Property-Tax-Relief-Application_Innisfil.pdf",
           "Wasaga Beach": "https://wasagabeach.com/en/resources/Documents/Treasury/2.%20Information%20about%20Tax%20Relief.pdf"},
    status="Open each year; deadline varies by town.", verified="Midland, Innisfil and Wasaga Beach pages checked Oct 21, 2026; other towns assumed similar under Municipal Act s.319 — confirm with the town.",
    value=val(a=250, t="tax", note="Published maximum"))

# ---------- Guelph and Wellington County ----------
WELL_TOWNS = ["Erin","Centre Wellington","Guelph/Eramosa","Puslinch","Mapleton","Minto","Wellington North"]
add("wellington-tax-relief", name="County of Wellington — Tax Relief for Low-income Seniors and Persons with Disabilities", level="Regional",
    regions=["city:"+t for t in WELL_TOWNS], categories=["tax"], housing=["owner"],
    amount="Property tax increase rebated: $400 minimum, up to $500 per year.",
    requirements="Owner 65+ receiving GIS, or receiving ODSP. Owned in the County at least 1 year; principal residence; current taxes paid.",
    action="DEADLINE Nov 1, 2026. Apply online or drop the form at the local municipal office. Renew yearly.",
    url="https://www.wellington.ca/your-government/budget-finance/tax-rebates",
    phone="519-837-2600 ext. 2340", status="Open; deadline Nov 1, 2026.", verified="Official County page checked Oct 21, 2026.",
    value=val(a=400, t="cash", note="Published minimum rebate"))
add("guelph-tax-deferral", name="Guelph — Property Tax Deferral for Low-income Seniors and Persons with Disabilities", level="Municipal",
    regions=["city:Guelph"], categories=["tax"], housing=["owner"],
    amount="Defers the full yearly increase when it is $200 or more; becomes a lien repaid on sale.",
    requirements="65+ receiving GIS or GAINS, or a low-income person with a disability. Principal residence for at least 1 year; current taxes paid.",
    action="Apply each year with supporting documents to City of Guelph Taxation, 1 Carden St.",
    url="https://guelph.ca/city-government/budget-and-finance/property-taxes/tax-rebates-programs-deferrals/",
    phone="519-822-1260 ext. 5605", status="Open; renew yearly.", verified="Official City page checked Oct 21, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred; repaid on sale"))
add("guelph-hardship", name="Guelph — Tax Cancellation for Sickness or Extreme Poverty (s.357)", level="Municipal",
    regions=["city:Guelph"], categories=["tax","debt"], housing=["owner"],
    amount="Cancellation, reduction or refund of property taxes; no fee for hardship cases.",
    requirements="Unable to pay because of sickness or extreme poverty (also fire, demolition, assessment errors).",
    action="Apply by Feb 28 of the following year to City of Guelph Taxation.",
    url="https://guelph.ca/city-government/budget-and-finance/property-taxes/tax-rebates-programs-deferrals/",
    phone="519-822-1260 ext. 5605", status="Open; deadline Feb 28 following year.", verified="Official City page checked Oct 21, 2026.",
    value=val(t="tax", note="Amount decided by Council; no illustration set"))
add("wellington-hsp", name="Wellington-Guelph Housing Stability Programme", level="Regional",
    regions=["region:Wellington"], categories=["housing","utility","debt","community"],
    amount="Help with rent arrears, utility arrears (with LEAP), first/last month's rent; capped per 24 months. Paid to landlord or utility.",
    requirements="Lives in Guelph or Wellington County; at risk of homelessness; can show future housing costs are affordable.",
    action="Call 519-837-2670 ext. 3712 or apply online at wellington.ca/HSP.",
    url="https://www.wellington.ca/programmes-services/housing-services-supports/eviction-prevention",
    phone="519-837-2670 ext. 3712", status="Open.", verified="Official County page checked Oct 21, 2026.",
    value=val(o=1000, t="cash", note="Illustrative; maximum not published"))
add("wellington-energy", name="Wellington-Guelph Emergency Energy Programme and LEAP intake", level="Regional",
    regions=["region:Wellington"], categories=["utility","community"],
    amount="Emergency help with heat and hydro costs; LEAP grants for low-income customers in arrears (up to $650).",
    requirements="Guelph or Wellington County resident; behind on utility bills or facing disconnection; low income.",
    action="Call 519-837-2670 ext. 3712 (Mon–Fri 8:30–4).",
    url="https://www.wellington.ca/programmes-services/housing-services-supports/eviction-prevention",
    source="https://wwhealthline.ca/printService.aspx?id=214077", phone="519-837-2670 ext. 3712",
    status="Open.", verified="Health directory listing (updated Dec 2025) and County page checked Oct 21, 2026.",
    value=val(o=650, t="cash", note="Same grant as provincial LEAP — do not add both"))
add("wellington-hap", name="Wellington-Guelph Housing Allowance Programme", level="Regional",
    regions=["region:Wellington"], categories=["housing"], housing=["renter"],
    amount="Monthly payment to the landlord to lower rent.",
    requirements="Income under County limits; rent at or below CMHC average market rent; no social housing arrears.",
    action="Call 519-824-7822 ext. 4060 for an application; contacted when funds open.",
    url="https://www.wellington.ca/programmes-services/housing-services-supports/about-wellington-guelph-housing-services/rent-support",
    phone="519-824-7822 ext. 4060", status="Subject to available funds.", verified="Official County page checked Oct 21, 2026.",
    value=val(m=250, t="cash", note="Illustrative; amount set by County"))
add("guelph-greener-homes", name="Guelph Greener Homes — 0% Loans and Low-income Heat Pump Grants", level="Municipal",
    regions=["city:Guelph"], categories=["repairs","utility"], housing=["owner"],
    amount="0% loan up to $50,000 over 10 years on the tax bill; low-income grant up to $15,000 for an air-source heat pump.",
    requirements="Guelph low-rise home over 5 years old, taxes current. Grant: home assessed $350,000 or less and income under City limits (e.g., $66,595 for 2 people).",
    action="Check registration status first — new registrations were paused in June 2025.",
    url="https://guelph.ca/living/environment/energy/guelph-greener-homes/how-the-guelph-greener-homes-program-works/",
    phone="519-822-1260 ext. 3984", status="PAUSED to new registrations since June 23, 2025 — confirm before offering.",
    verified="Official City page checked Oct 21, 2026.",
    value=val(o=15000, t="project", note="Published grant maximum; registration paused"))
add("guelph-royal-flush", name="Guelph — Royal Flush Toilet Rebate", level="Municipal",
    regions=["city:Guelph"], categories=["utility"], housing=["owner"],
    amount="$50 credit per toilet replaced (up to 2 for homeowners).",
    requirements="Home built before 2014 on City water; new toilet WaterSense, 4.8 L/flush or less.",
    action="Apply online with the receipt; credit appears on the water bill.",
    url="https://guelph.ca/living/environment/water/rebates/royal-flush-toilet-rebate/", phone="519-822-1260 ext. 2633",
    status="Open.", verified="Official City page checked Oct 21, 2026.",
    value=val(o=100, t="bill", note="Two toilets at $50"))
add("guelph-lead-pipe", name="Guelph — Lead Pipe Replacement Grant", level="Municipal",
    regions=["city:Guelph"], categories=["repairs"], housing=["owner"],
    amount="Up to $2,000 (about 80% of typical cost) to replace a private lead water service line.",
    requirements="City must confirm a lead service line; building permit required.",
    action="Contact Water Services before starting work.",
    url="https://guelph.ca/living/environment/water/rebates/replacement-program/", phone="519-822-1260 ext. 2263",
    status="Open; confirm funding with Water Services.", verified="Official City page checked Oct 21, 2026.",
    value=val(o=2000, t="project", note="Published maximum"))
add("guelph-bus-pass", name="Guelph Transit — Affordable Bus Pass", level="Municipal",
    regions=["city:Guelph"], categories=["transport"],
    amount="Free transit for the lowest income tiers; reduced fares with a monthly cap for Tier C.",
    requirements="Low-income household based on Statistics Canada LICO (e.g., 1 person up to $26,926).",
    action="Pick up a paper application at ServiceGuelph, Evergreen Seniors Centre or West End Community Centre.",
    url="https://guelph.ca/living/getting-around/bus/fares-and-passes/affordable-bus-pass/", status="Open.",
    verified="Official City page checked Oct 21, 2026.",
    value=val(a=800, t="bill", note="Illustrative yearly fare savings"))

# ---------- Not re-checked in this review ----------
for p in progs.values():
    if p["checked"] is None:
        p["verified"] = (p.get("verified") or "") + " — Not re-checked in Oct 2026 review."

# Normalise and order fields
ORDER = ["id","name","level","regions","categories","housing","amount","requirements","action","url","links","phone","status","value","checked","source","verified"]
out = []
for p in progs.values():
    for f in ("regions","categories","housing"):
        assert isinstance(p[f], list) and p[f], (p["id"], f)
    assert p["url"].startswith("https://"), p["id"]
    out.append({k: p[k] for k in ORDER if k in p and p[k] not in (None,)})
json.dump(out, open(OUT / "programs.json", "w"), indent=1, ensure_ascii=False)

# ---------- City lookup ----------
mun = json.load(open(SRC / "municipalities.json"))
ALIASES = {  # community name -> municipality
    "Elmira":"Woolwich","St. Jacobs":"Woolwich","Breslau":"Woolwich","New Hamburg":"Wilmot","Baden":"Wilmot",
    "St. Clements":"Wellesley","Ayr":"North Dumfries","Preston":"Cambridge","Hespeler":"Cambridge","Galt":"Cambridge",
    "Fergus":"Centre Wellington","Elora":"Centre Wellington","Rockwood":"Guelph/Eramosa","Harriston":"Minto",
    "Palmerston":"Minto","Clifford":"Minto","Mount Forest":"Wellington North","Arthur":"Wellington North",
    "Drayton":"Mapleton","Hillsburgh":"Erin","Aberfoyle":"Puslinch","Alliston":"New Tecumseth","Beeton":"New Tecumseth",
    "Tottenham":"New Tecumseth","Bradford":"Bradford West Gwillimbury","Angus":"Essa","Stayner":"Clearview",
    "Creemore":"Clearview","Elmvale":"Springwater","Midhurst":"Springwater","Alcona":"Innisfil","Cookstown":"Innisfil",
    "Coldwater":"Severn","Washago":"Severn","Victoria Harbour":"Tay","Port McNicoll":"Tay","Lafontaine":"Tiny",
    "Brechin":"Ramara","Orillia":"Orillia","Barrie":"Barrie",
}
for a, m in ALIASES.items():
    assert m in mun, m
lookup = {"municipalities": mun, "aliases": ALIASES,
          "coverage": {"Waterloo": "researched", "Simcoe": "researched", "Wellington": "researched"}}
json.dump(lookup, open(OUT / "municipalities.json", "w"), indent=1, ensure_ascii=False)
print(len(out), "programs;", sum(1 for p in out if p.get("checked")), "checked;", len(mun), "municipalities;", len(ALIASES), "aliases")
