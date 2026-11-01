"""Durham Region deep-dive (Oshawa and surrounding) — researched 2026-11-01.
Edits programs.json and municipalities.json in place. Run from the repository root."""
import json

TODAY = "2026-11-01"
ALL = ["owner", "renter", "other"]
progs = json.load(open("programs.json"))
by = {p["id"]: p for p in progs}
lookup = json.load(open("municipalities.json"))
mun = lookup["municipalities"]


def val(m=0, a=0, o=0, t="cash", note=""):
    return {"monthly": m, "annual": a, "once": o, "type": t, "note": note}


def add(pid, **kw):
    rec = {"id": pid, "housing": ALL, "phone": "", "checked": TODAY}
    rec.update(kw)
    rec.setdefault("source", rec["url"])
    rec.setdefault("value", val(t="project", note="No illustration set; review program terms"))
    if pid in by:
        by[pid].update(rec)
    else:
        progs.append(rec)
        by[pid] = rec


durham_towns = ["city:" + m for m, r in mun.items() if r == "Durham"]
not_pickering = [t for t in durham_towns if t != "city:Pickering"]

# ---------------- Renovation / energy ----------------
add("durham-greener-homes-loan",
    name="Durham Greener Homes Loan — 2% renovation loan up to $125,000",
    level="Regional", regions=not_pickering, categories=["repairs", "utility"], housing=["owner"],
    amount="Loan up to $125,000 at 2% fixed over 15 years, repaid through the property tax bill "
           "(e.g., $50,000 = about $322/month). At least 80% must go to energy upgrades (insulation, windows/doors, "
           "air sealing, heat pumps, water heaters, solar, ventilation); up to 20% to flood, heat and wind protection, "
           "water efficiency, electrical upgrades and permits.",
    requirements="Durham Region homeowner — NOT available for homes in the City of Pickering. Must enrol before "
                 "starting work; pre- and post-retrofit EnerGuide evaluations; agree to share energy data for 24 months. "
                 "Appliances, cosmetic work and completed projects not eligible.",
    action="Register at durhamgreenerhomes.ca and book a free Greener Homes Coach call; coach checks eligibility and "
           "walks through the loan application. Do NOT start work before approval. Can be combined with Home Renovation Savings rebates.",
    url="https://durhamgreenerhomes.ca/financial/loans/durham-region/",
    status="Open (except Pickering).",
    verified="Official Durham Greener Homes loan page checked Nov 1, 2026: up to $125,000, 2%, 15-year term, 80/20 split, Pickering excluded.",
    value=val(o=20000, t="financing", note="Illustrative low-interest renovation financing; not cash"))

add("durham-greener-homes-coaching",
    name="Durham Greener Homes — Free Renovation Coach and Weather-ready Home Assessment",
    level="Regional", regions=["region:Durham"], categories=["repairs", "utility", "community"], housing=["owner"],
    amount="Free: up to 4 phone/video sessions with a renovation coach, plus a free on-site Weather-ready Home Assessment "
           "(flooding, extreme heat/cold, wind) with a personalized action plan. Coach identifies every rebate and loan the home qualifies for.",
    requirements="Durham Region resident (all 8 municipalities, including Pickering).",
    action="Register at durhamgreenerhomes.ca/get-started, then book through the portal. Good first step for any renovation client in Durham.",
    url="https://durhamgreenerhomes.ca/get-started/",
    status="Open; no cost.",
    verified="Official Durham Greener Homes 'Get Started' page checked Nov 1, 2026.",
    value=val(o=500, t="project", note="Illustrative value of free assessment and coaching; noncash"))

add("whitby-adu-incentive",
    name="Whitby — Additional Dwelling Unit Fee Reimbursement",
    level="Municipal", regions=["city:Whitby"], categories=["adu"], housing=["owner"],
    amount="Town repays select fees for a new basement/garden suite: ADU building permit fee, registration inspection fee, curb cut fee, education development charges.",
    requirements="Whitby owner who got the ADU building permit during the program period; unit registered with By-law Services by Mar 31, 2027.",
    action="Program ended for new permits Dec 31, 2025. Clients who already have a permit: email HAF-ADU@whitby.ca and register the unit by Mar 31, 2027.",
    url="https://www.whitby.ca/en/town-hall/additional-dwelling-units.aspx", phone="905-430-4300",
    status="CLOSED to new permits (ended Dec 31, 2025); registration deadline Mar 31, 2027 for existing permits.",
    verified="Official Town ADU page checked Nov 1, 2026: HAF-funded until Dec 31, 2025; register by Mar 31, 2027, no extensions.",
    value=val(t="project", note="Program closed to new applicants"))

# ---------------- Property tax ----------------
add("brock-seniors-rebate",
    name="Brock — Low-income Seniors Property Tax Rebate",
    level="Municipal", regions=["city:Brock"], categories=["tax"], housing=["owner"],
    amount="$355 per year off property taxes.",
    requirements="Homeowner 65+ receiving GIS; principal residence. GIS renewal award letter must be attached.",
    action="Apply by Sept 30 each year at the Municipal Office or online (2026 window passed — plan for 2027).",
    url="https://www.townshipofbrock.ca/news/posts/low-income-seniors-property-tax-rebate", phone="705-432-2355",
    status="Annual; 2026 deadline Sept 30 passed; next Sept 30, 2027.",
    verified="Official Township of Brock notice checked Nov 1, 2026: $355; 65+ on GIS; deadline Sept 30.",
    value=val(a=355, t="cash", note="Published amount"))

add("scugog-tax-grant",
    name="Scugog — Property Tax Grant for Low-income Seniors and Persons with Disabilities",
    level="Municipal", regions=["city:Scugog"], categories=["tax"], housing=["owner"],
    amount="$375 per year property tax assistance grant.",
    requirements="Owner-occupant (principal residence) receiving GIS (seniors) or ODSP (persons with a disability).",
    action="Submit 'Application A' to the Finance Department by Aug 31 each year (2026 window passed — plan for 2027). Email tax@scugog.ca.",
    url="https://www.scugog.ca/home-property-roads/property-taxes/tax-incentive-and-rebate-programs/",
    phone="905-985-7346 ext. 102 or 106",
    status="Annual; 2026 deadline Aug 31 passed; next Aug 31, 2027.",
    verified="Official Township of Scugog tax incentive page checked Nov 1, 2026: $375; GIS or ODSP; deadline Aug 31.",
    value=val(a=375, t="cash", note="Published amount"))

add("clarington-tax-relief",
    name="Clarington — Property Tax Cancellation or Reduction (hardship)",
    level="Municipal", regions=["city:Clarington"], categories=["tax", "debt"], housing=["owner"],
    amount="Cancellation or reduction of property taxes in certain circumstances (e.g., sickness or extreme poverty), decided case by case.",
    requirements="Clarington property owner; reviewed by Taxation Services.",
    action="Call Taxation Services 905-623-3379 ext. 2650. Apply by the last day of February of the year after the tax year (2026 taxes: by Feb 28, 2027).",
    url="https://www.clarington.net/en/town-hall/Property-Taxes-and-Assessments.aspx", phone="905-623-3379 ext. 2650",
    status="Open; 2026 taxes deadline Feb 28, 2027.",
    verified="Official Municipality of Clarington property tax page checked Nov 1, 2026; no separate seniors rebate listed.",
    value=val(a=200, t="tax", note="Illustrative; case by case"))

add("oshawa-hardship-relief",
    name="Oshawa — Tax Relief for Sickness or Extreme Poverty (Section 357)",
    level="Municipal", regions=["city:Oshawa"], categories=["tax", "debt"], housing=["owner"],
    amount="Relief of the previous year's property taxes for owners facing sickness or extreme poverty.",
    requirements="Oshawa property owner; select the sickness/extreme poverty reason on the Section 357 form.",
    action="Send the completed Section 357 form to Taxation Services; staff follow up. Service Oshawa 905-436-3311.",
    url="https://www.oshawa.ca/en/home-property/tax-rebates-and-reductions.aspx", phone="905-436-3311",
    status="Open.",
    verified="Official Oshawa Tax Rebates and Reductions page checked Nov 1, 2026.",
    value=val(a=200, t="tax", note="Illustrative; case by case"))

# ---------------- Utilities ----------------
add("durham-leap-intake",
    name="Durham — LEAP Emergency Energy Grant intake (Community Development Council Durham)",
    level="Regional", regions=["region:Durham"], categories=["utility", "community"],
    amount="Local intake for the provincial LEAP grant: up to $650 toward an overdue electricity or gas bill ($780 if electrically heated).",
    requirements="Elexicon Energy or Oshawa Power customer behind on the bill or facing disconnection; income under LEAP limits. "
                 "Hydro One customers (parts of Clarington, Scugog, Brock) and Enbridge Gas customers: confirm the agency with the OEB LEAP agency list.",
    action="Call Community Development Council Durham, 905-686-2661, 458 Fairall St, Unit 4, Ajax. Bring ID, bills, disconnection notice, proof of income.",
    url="https://oeb.ca/consumer-information-and-protection/bill-assistance-programs/low-income-energy-assistance-program/leap-agencies",
    phone="905-686-2661",
    status="Open, year-round, while funds last.",
    verified="OEB LEAP agency list (Elexicon Whitby zone and Oshawa PUC entries) and Town of Ajax seniors page checked Nov 1, 2026.",
    value=val(t="cash", note="Same grant as the Ontario LEAP listing — do not count twice"))

add("oshawa-power-assistance",
    name="Oshawa Power — Arrears Management, Compassion Fund and Rainy Day Fund",
    level="Municipal", regions=["city:Oshawa"], categories=["utility", "debt"],
    amount="Arrears Management Program for customers behind on bills; Compassion Fund; Rainy Day Fund (with Shine Through the Rain Foundation) for customers with a life-threatening illness.",
    requirements="Oshawa Power customer who has fallen behind.",
    action="See oshawapower.ca/assistance or call Oshawa Power customer service. For a LEAP grant, call CDC Durham 905-686-2661.",
    url="https://www.durham.ca/living-here/living-with-low-income/housing-outreach-eviction-prevention-and-utility-and-rent-arrears-resources/",
    status="Open.",
    verified="Durham Region utility arrears resources page checked Nov 1, 2026 (describes Oshawa Power programs); amounts not published.",
    value=val(o=300, t="bill", note="Illustrative; amount not published"))

add("durham-water-bill-help",
    name="Durham Region — Water Bill Payment Help (60+ due-date extension)",
    level="Regional", regions=["region:Durham"], categories=["utility"],
    amount="Payment arrangements for customers struggling with water bills; due-date extension available for customers 60+.",
    requirements="Durham Region water customer.",
    action="Call 311 (or 905-668-7711) and ask Water Billing for a payment arrangement or a seniors' due-date extension.",
    url="https://ajax.ca/life-in-ajax/town-services/aging-well-in-ajax/senior-financial-assistance-benefits/", phone="311 / 905-668-7711",
    status="Open.",
    verified="Town of Ajax Senior Financial Assistance page checked Nov 1, 2026 (describes the Region's water bill assistance).",
    value=val(t="bill", note="Payment timing help; no dollar value"))

# ---------------- Aging in place / transport ----------------
add("oshawa-snow-help",
    name="Oshawa — Snow Clearing Help for Seniors and Persons with Disabilities",
    level="Municipal", regions=["city:Oshawa"], categories=["access", "community"],
    amount="City clears and salts the sidewalk and clears the driveway windrow (plow pile 20 cm+) all winter.",
    requirements="65+ or have a disability; single-family home on a City street; no one under 65 without a disability in the home. Proof required (doctor's note, Accessible Parking Permit, CPP-D card or ODSP receipt).",
    action="Apply online or at Service Oshawa, Oct 1 to Dec 18, 2026 (late applications reviewed case by case). Renew yearly.",
    url="https://www.oshawa.ca/getting-around/snow-clearing/snow-clearing-help/", phone="905-436-3311",
    status="OPEN NOW — 2026 window Oct 1 to Dec 18.",
    verified="Official City of Oshawa Snow Clearing Help page checked Nov 1, 2026.",
    value=val(a=300, t="project", note="Illustrative value of a free winter service; noncash"))

add("whitby-windrow",
    name="Whitby — Free Windrow Snow Clearing for Seniors and Persons with Disabilities",
    level="Municipal", regions=["city:Whitby"], categories=["access", "community"],
    amount="Free clearing of the driveway windrow left by the plow.",
    requirements="Whitby resident 65+, or a doctor certifies you cannot clear snow; no one under 65 in the home who can help.",
    action="Register at whitby.ca/WindrowApp. 2026 registration ran Sept 14 to Nov 1, 2026 — call 905-668-3437 to ask about late or waitlist spots.",
    url="https://www.whitby.ca/payments-and-services/parking-roads-and-transportation/snow-and-windrow-clearing-services",
    phone="905-668-3437",
    status="2026 registration closed Nov 1; next season opens mid-September 2027.",
    verified="Official Town of Whitby snow and windrow page checked Nov 1, 2026: free; registration Sept 14 – Nov 1, 2026.",
    value=val(a=300, t="project", note="Illustrative value of a free winter service; noncash"))

add("clarington-snow",
    name="Clarington — Snow Clearing Program for Seniors and Persons with Disabilities",
    level="Municipal", regions=["city:Clarington"], categories=["access", "community"],
    amount="Clears the municipal sidewalk and up to 3 ft of driveway apron (windrow) all winter, for $107.69 (2026–27, HST included).",
    requirements="65+ or doctor-certified physical disability; no able-bodied person under 65 at home; single-family urban home on a municipal street.",
    action="2026–27 registration ran Sept 21 to Oct 31, 2026. Call Community Services 905-623-3379 to ask about late spots.",
    url="https://www.clarington.net/community-and-people/roads-and-transportation/sidewalk-snow-removal/snow-clearing-program-for-seniors-and-persons-with-disabilities/",
    phone="905-623-3379",
    status="2026–27 registration closed Oct 31; next season opens September 2027.",
    verified="Official Municipality of Clarington page checked Nov 1, 2026: $107.69; registration Sept 21 – Oct 31, 2026.",
    value=val(a=200, t="project", note="Illustrative value of a subsidized winter service; noncash"))

add("durham-tap",
    name="Durham Region Transit — Transit Assistance Program (OW/ODSP)",
    level="Regional", regions=["region:Durham"], categories=["transport"],
    amount="Unlimited monthly DRT travel for $53.76 (TAP PRESTO monthly pass or E-Purse), from July 1, 2026.",
    requirements="Durham resident receiving Ontario Works or ODSP. (Seniors 65+ get senior fares, e.g. $55.30 monthly pass.)",
    action="Ask the OW/ODSP caseworker or DRT about a TAP PRESTO card; see durhamregiontransit.com.",
    url="https://www.durham.ca/media/0oaf3swl/2026-transit-fees-charges-updated-july-1.pdf",
    status="Open.",
    verified="Official Durham 2026 transit fees schedule (updated July 1, 2026) checked Nov 1, 2026.",
    value=val(a=600, t="bill", note="Illustrative yearly fare savings"))

# ---------------- Updates to existing Durham records ----------------
h = by["durham-hsp"]
h.update(
    amount="Up to 2 months of rent or utility arrears (rent caps $3,000 1-bed to $4,000 4+-bed), last month's rent deposit, utility deposits/reconnection.",
    requirements="Durham resident on OW/ODSP, or net household income under $50,000 (1 person), $58,000 (2), $65,000 (3), $68,000 (4), "
                 "$72,000 (5), $75,000 (6), $78,000 (7+). Once per 3 years per benefit type; subject to funding. Mainly for renters — homeowners ask about utility arrears.",
    action="Apply online on the Region's HSP form or call 905-668-4113 ext. 3474 (also listed: 905-666-6239 ext. 1803). Outreach workers: Ajax-Pickering CDC Durham 905-686-2661; "
           "Oshawa-Whitby John Howard Society 905-579-8482; Clarington 905-623-6814; Scugog/Uxbridge/Brock Community Living Durham North 905-852-5919.",
    url="https://www.durham.ca/en/living-here/housing-supports.aspx", phone="905-668-4113 ext. 3474",
    checked=TODAY, source="https://www.durham.ca/en/living-here/housing-supports.aspx",
    verified="Official Durham Housing Supports page checked Nov 1, 2026: arrears caps, income limits, once per 3 years, phone 905-668-4113 ext. 3474.")

# ---------------- Community names reps may type ----------------
lookup["aliases"].update({
    "Orono": "Clarington", "Brooklin": "Whitby", "Ashburn": "Whitby", "Port Whitby": "Whitby",
    "Claremont": "Pickering", "Pickering Village": "Ajax", "Sunderland": "Brock",
    "Blackstock": "Scugog", "Greenbank": "Scugog", "Port Bolster": "Brock", "Hampton": "Clarington",
    "Enniskillen": "Clarington", "Newtonville": "Clarington", "Port Darlington": "Clarington",
})

json.dump(progs, open("programs.json", "w"), indent=1, ensure_ascii=False)
json.dump(lookup, open("municipalities.json", "w"), indent=1, ensure_ascii=False)
print(len(progs), "programs")
