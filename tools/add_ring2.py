"""Ring 2 (Toronto, Peel, Halton, Hamilton, York, Durham, Niagara, Dufferin) — researched 2026-10-22.
Edits programs.json and municipalities.json in place. Run from the repository root."""
import json

TODAY = "2026-10-22"
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
        progs.append(rec); by[pid] = rec

def towns(region):
    return ["city:" + m for m, r in mun.items() if r == region]

# ---------------- Toronto ----------------
add("toronto-tax-relief", name="Toronto — Property Tax, Water and Solid Waste Relief (seniors and disability)", level="Municipal",
    regions=["city:Toronto"], categories=["tax","utility"], housing=["owner"],
    amount="Cancellation or deferral of the yearly property tax increase, plus water and garbage bin rebates.",
    requirements="Owner-occupant 1+ year; combined owner income $62,000 or less; 65+, or 60–64 on GIS, or receiving a disability benefit (deferral also open to 50+ with a pension). Cancellation needs assessment under $975,000. Water rebate needs use under 400 m³/yr.",
    action="DEADLINE Nov 2, 2026. Apply online or mail the form to Revenue Services, 5100 Yonge St. Reapply every year.",
    url="https://www.toronto.ca/services-payments/property-taxes-utilities/property-tax/property-tax-water-solid-waste-relief-and-rebate-programs/property-tax-and-utility-relief-program/",
    phone="311", status="Open; 2026 deadline Nov 2.", verified="Official City page checked Oct 22, 2026.",
    value=val(a=300, t="tax", note="Illustrative; depends on tax increase and water use"))
add("toronto-hardship", name="Toronto — Tax Appeal for Sickness or Extreme Poverty", level="Municipal",
    regions=["city:Toronto"], categories=["tax","debt"], housing=["owner"],
    amount="Cancellation, reduction or refund of property taxes for owners unable to pay because of sickness or extreme poverty.",
    requirements="Owner who cannot pay because of sickness or extreme poverty; reviewed case by case.",
    action="Apply through the City's property tax appeal page; check the deadline on the page.",
    url="https://www.toronto.ca/services-payments/property-taxes-utilities/property-tax/property-tax-water-solid-waste-relief-and-rebate-programs/property-tax-appeal-sickness-or-extreme-poverty/",
    phone="311", status="Ongoing.", verified="Listed on official City relief page Oct 22, 2026.",
    value=val(t="tax", note="Amount decided by the City; no illustration set"))
by["import-17"].update(dict(name="Toronto — Basement Flooding Protection Subsidy", level="Municipal", regions=["city:Toronto"], housing=["owner"],
    amount="Up to 80% of costs, up to $6,650 per property: backwater valves up to $1,600 each (max 2), sump pump up to $2,250, battery backup $300, weeping tile severance $400, plumbing assessment $500.",
    requirements="Registered owner of a single-family home to fourplex; downspouts disconnected; City-licensed contractor; no City taxes owing; apply within 2 years of work.",
    action="Get a building permit for backwater valves; apply online with paid invoices.",
    url="https://www.toronto.ca/services-payments/water-environment/basement-flooding-protection-subsidy-program/",
    source="https://www.toronto.ca/services-payments/water-environment/basement-flooding-protection-subsidy-program/",
    phone="416-338-7668", status="Open; expanded May 1, 2026; first come first served.", checked=TODAY,
    verified="Official City page checked Oct 22, 2026.", value=val(o=3000, t="project", note="Illustrative; up to $6,650")))
add("toronto-help", name="Toronto — Home Energy Loan Program (HELP)", level="Municipal",
    regions=["city:Toronto"], categories=["repairs","utility"], housing=["owner"],
    amount="Low-rate loans up to $125,000 for energy upgrades, repaid on the property tax bill (3.95% for 5 years to 5.20% for 20 years).",
    requirements="Owner of a low-rise home in Toronto; all owners and mortgage lender consent; tax and utility accounts in good standing.",
    action="Apply online; book an energy assessment if required.",
    url="https://www.toronto.ca/services-payments/water-environment/net-zero-homes-buildings/homeowner-financing/home-energy-loan-program-help/",
    status="Open; rates fixed to Dec 31, 2026.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=20000, t="financing", note="Illustrative loan; repaid with interest"))
add("toronto-renovates", name="Toronto Renovates — Homeowner Repairs and Accessibility", level="Municipal",
    regions=["city:Toronto"], categories=["repairs","access"], housing=["owner"],
    amount="Funding for essential repairs and accessibility changes for low-income senior and disabled homeowners.",
    requirements="Low-income homeowner; seniors and people with disabilities prioritised; no other property.",
    action="Call 416-392-7620 or email torontorenovates@toronto.ca to confirm intake before applying.",
    url="https://www.toronto.ca/wp-content/uploads/2021/11/98ea-Toronto-Renovates-Assessment-Request-Form.pdf",
    phone="416-392-7620", status="Current intake not confirmed — check before offering.",
    verified="Program form (2021) found; current status not confirmed Oct 22, 2026.",
    value=val(o=10000, t="financing", note="Illustrative; amount not published"))
add("toronto-eef", name="Toronto — Emergency Energy Fund", level="Municipal",
    regions=["city:Toronto"], categories=["utility","community"],
    amount="Help to prevent disconnection, reconnect, or pay hydro, gas or oil arrears.",
    requirements="Low-income Toronto resident not on OW/ODSP (OW/ODSP clients ask their caseworker).",
    action="Call the Neighbourhood Information Post at 647-727-8988, weekdays 9–4:30.",
    url="https://www.toronto.ca/community-people/employment-social-support/support-for-people-in-financial-need/assistance-through-ontario-works/policies-and-procedures/emergency-energy-fund-eef/",
    phone="647-727-8988", status="Open.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=650, t="cash", note="Illustrative; overlaps LEAP — do not add both"))
add("toronto-leap", name="LEAP intake — Toronto agencies", level="Community",
    regions=["city:Toronto"], categories=["utility"],
    amount="Up to $650 toward electricity or gas arrears ($780 for electric heat).",
    requirements="Behind on bills and at risk of disconnection; after-tax income under LEAP limits.",
    action="Book with the nearest agency, e.g. Neighbourhood Information Post 416-924-2543, Housing Help Centre (Scarborough) 416-285-8070, Albion (Etobicoke) 416-252-5990.",
    url="https://www.torontohydro.com/for-home/financial-assistance", phone="416-924-2543",
    status="Open.", verified="Toronto Hydro agency list checked Oct 22, 2026.",
    value=val(o=650, t="cash", note="Same grant as provincial LEAP — do not add both"))
add("toronto-rent-bank", name="Toronto Rent Bank", level="Municipal", regions=["city:Toronto"], categories=["housing","debt"], housing=["renter"],
    amount="Grant up to $5,000 for rent arrears, or $2,000–$3,500 for a rental deposit.",
    requirements="Market-rent tenant; not on OW/ODSP; income up to $46,500 (1 person) to $66,500 (4); rent no more than 85% of income; asset limits.",
    action="Apply online through Neighbourhood Information Post (nipost.org) or a Local Access Centre.",
    url="https://www.toronto.ca/rentbank", phone="311", status="Open.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=2500, t="cash", note="Illustrative; paid to landlord"))
add("toronto-fair-pass", name="TTC Fair Pass — Transit Discount", level="Municipal", regions=["city:Toronto"], categories=["transport"],
    amount="36% off adult TTC fares ($2.10 instead of $3.30), monthly cap $98.70.",
    requirements="Age 20–64, Toronto resident, after-tax family income below 75% of LIM-AT (e.g. $23,488 for 1 person); OW/ODSP qualify.",
    action="Apply online with a PRESTO card number or call 416-338-8888.",
    url="https://www.toronto.ca/community-people/employment-social-support/support-for-people-in-financial-need/assistance-through-ontario-works/fair-pass-transit-discount-program/",
    phone="416-338-8888", status="Open.", verified="Official City page checked Oct 22, 2026.",
    value=val(a=500, t="bill", note="Illustrative yearly fare savings"))

# ---------------- Peel ----------------
add("peel-tax-rebate", name="Peel — Property Tax Rebate for Low-income Seniors and Persons with Disabilities", level="Regional",
    regions=["region:Peel"], categories=["tax"], housing=["owner"],
    amount="Yearly property tax rebate: Brampton $590 (2026); Mississauga $571 (2025, rises yearly).",
    requirements="Owner 65+ receiving GIS, or receiving ODSP; principal residence owned 1+ year; apply every year.",
    action="DEADLINE Dec 31, 2026. Apply to your city (Mississauga, Brampton or Caledon).",
    url="https://peelregion.ca/finance/tax-rebate-seniors-and-disabilities.asp",
    links={"Brampton": "https://brampton.ca/en/residents/Taxes-Assessment/taxation/Pages/tax-adjustments-rebates.aspx"},
    status="Open; deadline Dec 31.", verified="Peel Region and City of Brampton pages and Mississauga 2025 guide checked Oct 22, 2026.",
    value=val(a=590, t="cash", note="2026 Brampton amount"))
add("mississauga-older-adult-subsidies", name="Mississauga — Stormwater Subsidy and Outdoor Maintenance Subsidy", level="Municipal",
    regions=["city:Mississauga"], categories=["utility","access"], housing=["owner"],
    amount="100% of the yearly stormwater charge (automatic with the tax rebate), plus up to $400 a year back for paid yard care and snow removal.",
    requirements="Tax rebate recipient (65+ on GIS or ODSP). Maintenance subsidy: no able-bodied person in the home; proof of payment.",
    action="Stormwater: automatic. Maintenance: apply by Mar 31 of the next year; email tax@mississauga.ca.",
    url="https://www.mississauga.ca/wp-content/uploads/2025/09/25151346/Financial-Assistance-for-Older-Adults-September-2025.pdf",
    status="Open (per Sept 2025 City guide).", verified="City of Mississauga guide (Sept 2025) checked Oct 22, 2026.",
    value=val(a=400, t="cash", note="Published maintenance maximum"))
add("peel-backwater", name="Peel — Backwater Valve Rebate", level="Regional", regions=["region:Peel"], categories=["repairs"], housing=["owner"],
    amount="60% of the invoice, up to $1,500.",
    requirements="Valve on the sanitary line; building permit and passed inspection.",
    action="Apply after installation and inspection; cheque in 4–6 weeks.",
    url="https://peelregion.ca/water/pipes-downspouts/backwater-valve-rebate", source="https://peelregion.ca/wastewater/backwater-valve-rebate.asp",
    status="Open (forms updated Dec 2025).", verified="Peel Region page checked Oct 22, 2026.",
    value=val(o=1500, t="project", note="Published maximum"))
add("peel-water-relief", name="Peel — Water Bill Relief Program", level="Regional", regions=["region:Peel"], categories=["utility"],
    amount="Credit on the water bill: 20% of the rate-change increase for bills Apr 2026–Mar 2027.",
    requirements="Peel water bill in your name and 65+, or low income ($35,000 for 1 to $52,500 for 5), or very low water use.",
    action="Apply online through the Region's resident portal or call 905-791-8711.",
    url="https://peelregion.ca/services/water-bill-relief-program", phone="905-791-8711",
    status="Open; credit shrinks each year.", verified="Official Region page checked Oct 22, 2026.",
    value=val(a=40, t="bill", note="Illustrative"))
add("peel-past-due", name="Peel — Emergency Help with Past-due Rent or Utility Bills", level="Regional",
    regions=["region:Peel"], categories=["housing","utility","debt","community"],
    amount="One-time financial help with overdue utility bills or rent; based on need.",
    requirements="Peel resident behind on utilities or rent; proof of income and expenses.",
    action="Apply online through a Peel Region account.",
    url="https://peelregion.ca/help/past-due-bills/", status="Open.", verified="Official Region page checked Oct 22, 2026.",
    value=val(o=650, t="cash", note="Illustrative; overlaps LEAP — do not add both"))
add("peel-transit", name="Peel — Affordable Transit Program (MiWay, Brampton Transit, Caledon)", level="Regional",
    regions=["region:Peel"], categories=["transport"],
    amount="50% off monthly passes and single fares for 12 months.",
    requirements="Age 20+; net household income up to $30,255 (1 person) to $60,510 (4); PRESTO card.",
    action="Apply online or call 905-793-9200.",
    url="https://peelregion.ca/services/bus-fare-discounts", phone="905-793-9200", status="Open.",
    verified="Official Region page checked Oct 22, 2026.", value=val(a=700, t="bill", note="Illustrative yearly savings"))

# ---------------- Halton ----------------
add("halton-increase-deferral", name="Halton — Property Tax Increase Deferral (seniors and disability)", level="Regional",
    regions=["region:Halton"], categories=["tax"], housing=["owner"],
    amount="Defers the yearly property tax increase until the home is sold.",
    requirements="65+ or receiving disability benefits (ODSP, CPP-D or private); combined income $69,500 or less; principal residence.",
    action="Apply to your town/city within 45 days of the final tax bill (usually early June). Renew yearly.",
    url="https://www.halton.ca/repository/property-tax-increase-deferral-program-application",
    source="https://www.halton.ca/getmedia/9c09f93b-365f-40f2-a8e6-d946618e95ed/fn-by-law-no-21-26-amended-09-25-tax-increase-deferral-program-apr-2026.pdf",
    phone="311", status="Annual; 2026 window has passed.", verified="Halton by-law 21-26 (Apr 2026) checked Oct 22, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred"))
add("halton-older-adult-deferral", name="Halton — Older Adults Full Property Tax Deferral", level="Regional",
    regions=["region:Halton"], categories=["tax"], housing=["owner"],
    amount="Defers ALL yearly property taxes as an interest-free loan, repaid on sale ($200 one-time fee).",
    requirements="65+; principal residence for the last 4 years; combined income under $69,500; one property only.",
    action="2026 intake closed; new applications expected spring 2027. Renewals due Sept 30.",
    url="https://www.halton.ca/the-region/finance-and-transparency/property-taxes/older-adults-property-tax-deferral-program",
    phone="311", status="Closed for 2026 — reopens spring 2027.", verified="Official Region page checked Oct 22, 2026.",
    value=val(a=5000, t="financing", note="Illustrative full tax deferred; repaid on sale"))
add("oakville-seniors-rebate", name="Oakville — Seniors Property Tax Rebate", level="Municipal",
    regions=["city:Oakville"], categories=["tax"], housing=["owner"],
    amount="$500 per year.",
    requirements="Owner 65+ where owner or spouse receives GIS; only owners/spouse live there. Can't combine with the deferral.",
    action="Apply to ServiceOakville; email tax@oakville.ca.",
    url="https://www.oakville.ca/home-environment/property-tax-assessments/tax-rebates-assistance/",
    source="https://www.mississaugahaltonhealthline.ca/printService.aspx?id=111097",
    phone="905-845-6601", status="Open.", verified="Health directory listing (updated May 2026) checked Oct 22, 2026.",
    value=val(a=500, t="cash", note="Published amount"))
add("burlington-tax-reduction", name="Burlington — Property Tax Reduction for Low-income Seniors and Persons with Disabilities", level="Municipal",
    regions=["city:Burlington"], categories=["tax"], housing=["owner"],
    amount="$575 property tax reduction.",
    requirements="Low-income senior or person with a disability (check City criteria). Can't combine with a deferral.",
    action="DEADLINE Dec 31 each year. Contact the City tax office.",
    url="https://www.burlington.ca/en/property-taxes/rebates-and-deferrals.aspx", source="https://halton.cioc.ca/record/BTN4799",
    phone="905-335-7750", status="Open; deadline Dec 31.", verified="Community directory (updated Oct 19, 2026) checked Oct 22, 2026.",
    value=val(a=575, t="cash", note="Published amount"))
add("halton-hsf", name="Halton — Housing Stability Fund", level="Regional", regions=["region:Halton"], categories=["housing","utility","debt"],
    amount="One-time payments for unpaid rent, last month's rent, moving, and hydro/gas arrears (after applying to LEAP).",
    requirements="Halton resident at risk of losing housing; assets under $5,000 (single/couple) or $10,000 (family).",
    action="Apply online through a Halton 311 account or call 311 / 905-825-6000.",
    url="https://halton.ca/For-Residents/Housing-Supports-and-Services/Housing/Housing-Stability-Fund", phone="905-825-6000",
    status="Open.", verified="Official Region page checked Oct 22, 2026.",
    value=val(o=1000, t="cash", note="Illustrative; maximum not published"))
add("halton-backwater", name="Halton — Basement Flooding Prevention Subsidy (backwater valve)", level="Regional",
    regions=["region:Halton"], categories=["repairs"], housing=["owner"],
    amount="50% of cost up to $1,600 for a backwater valve; other subsidies for sump pumps and downspouts.",
    requirements="On municipal sewer; building permit; weeping tile disconnected; apply within 1 year.",
    action="Email basementfloodingsubsidy@halton.ca with invoice and permit sign-off.",
    url="https://www.halton.ca/for-residents/water-and-wastewater-services/basement-flooding/flood-preparedness-and-reducing-your-risk/backwater-valve-installation-subsidy",
    phone="905-825-6000", status="Open (amounts updated Sept 2025).", verified="Official Region page checked Oct 22, 2026.",
    value=val(o=1600, t="project", note="Published maximum"))

# ---------------- Hamilton ----------------
add("hamilton-seniors-rebate", name="Hamilton — Seniors Tax Rebate", level="Municipal", regions=["city:Hamilton"], categories=["tax"], housing=["owner"],
    amount="Yearly credit on the property tax account.",
    requirements="Owner or spouse 65+; household income $44,568 or less; home assessed $505,694 or less; owned 1+ year; prior taxes paid.",
    action="Apply any time up to the last day of February of the following year.",
    url="https://www.hamilton.ca/home-neighbourhood/property-taxes/property-tax-billing/tax-assistance-programs",
    source="https://redbook.hpl.ca/node/11781", phone="905-546-2489", status="Open.",
    verified="Hamilton Public Library directory (updated July 2026) checked Oct 22, 2026.",
    value=val(a=200, t="cash", note="Illustrative; amount not published"))
add("hamilton-tax-deferral", name="Hamilton — Tax Increase Deferral (seniors and disability)", level="Municipal",
    regions=["city:Hamilton"], categories=["tax"], housing=["owner"],
    amount="Defers the yearly tax increase, interest-free while eligible.",
    requirements="65+, or receiving ODSP, GIS disability or CPP disability; income limit applies; owned 1+ year.",
    action="Apply by the last day of February of the following year.",
    url="https://hamilton.ca/sites/default/files/2024-06/taxes-full-deferral-tax-application-jun2024.pdf",
    phone="905-546-2489", status="Open; renew yearly.", verified="City application form (2024) checked Oct 22, 2026; confirm current income limit.",
    value=val(a=300, t="financing", note="Illustrative tax deferred"))
add("hamilton-renovates", name="Hamilton — Ontario Renovates (repairs and accessibility)", level="Municipal",
    regions=["city:Hamilton"], categories=["repairs","access"], housing=["owner"],
    amount="Help with basic repairs (roof, plumbing, electrical, furnace) or accessibility changes; limited funding.",
    requirements="Owner-occupant; household income up to $60,000; home assessed $300,000 or less; mortgage, taxes and insurance current.",
    action="Call 905-546-2424 ext. 2758.",
    url="https://www.hamilton.ca/people-programs/housing-shelter/supported-housing/ontario-renovates-programs",
    source="https://centraleast.rehabcareontario.ca/Services/PrintServiceDetailsNoTracking/180572",
    phone="905-546-2424 ext. 2758", status="Open; limited funding.", verified="Health directory listing (updated June 2026) checked Oct 22, 2026.",
    value=val(o=10000, t="financing", note="Illustrative; amount not published"))
add("hamilton-3p", name="Hamilton — Protective Plumbing Program (3P)", level="Municipal",
    regions=["city:Hamilton"], categories=["repairs"], housing=["owner"],
    amount="Grant up to $2,000 for a backwater valve, sump pump or downspout disconnection, plus a loan for costs above the grant.",
    requirements="Single-family home with a basement on City sewer, built before 2012; no tax arrears.",
    action="Email waterstorefront@hamilton.ca or call 905-546-2489.",
    url="https://hamilton.ca/home-neighbourhood/house-home/basement-flooding/protective-plumbing-program",
    source="https://hellodarwin.com/business-aid/programs/protective-plumbing-program",
    phone="905-546-2489", status="Open, continuous intake.", verified="Program summary (verified July 2026) checked Oct 22, 2026.",
    value=val(o=2000, t="project", note="Published maximum"))
add("hamilton-hef", name="Hamilton — Housing Emergency Fund", level="Municipal", regions=["city:Hamilton"], categories=["housing","utility","debt"],
    amount="Help with rent arrears, utility arrears and last month's rent; capped by household size over 24 months.",
    requirements="Low-income Hamilton resident; housing costs no more than 95% of income; eviction or disconnection notice.",
    action="Low-income/ODSP: apply through the Hamilton Housing Help Centre. Email hef@hamilton.ca.",
    url="https://www.hamilton.ca/people-programs/housing-shelter/housing-supports/housing-emergency-fund",
    source="https://redbook.hpl.ca/node/26161", status="Open.", verified="Library directory (updated Jan 2026) checked Oct 22, 2026.",
    value=val(o=1000, t="cash", note="Illustrative"))

# ---------------- York ----------------
add("york-tax-deferral", name="York Region — Tax Deferral for Seniors and Low-income Persons with Disabilities", level="Regional",
    regions=["region:York"], categories=["tax"], housing=["owner"],
    amount="Defers the yearly tax increase (for low-income 55–64: the part over $300), repaid on sale.",
    requirements="65+; or 55–64 with income up to $23,000 (single) / $40,000 (family); or on ODSP/GAINS-D. Principal residence.",
    action="Apply to your city/town by Sept 30 each year (2026 window passed — plan for 2027).",
    url="https://www.Vaughan.ca/sites/default/files/Property%20Tax%20Deferral%20for%20Seniors%20and%20Disabled%20Persons.pdf",
    links={"King": "https://www.king.ca/sites/default/files/docs/Low%20Income%20Seniors%20Deferral%20application.pdf",
           "Aurora": "https://www.aurora.ca/media/n22nfhli/property-tax-deferral-program-form.pdf"},
    status="Annual; deadline Sept 30.", verified="Vaughan form under York By-law A-0399-2004-026 checked Oct 22, 2026.",
    value=val(a=300, t="financing", note="Illustrative tax deferred"))
add("richmondhill-senior-grant", name="Richmond Hill — Senior Tax Assistance Grant", level="Municipal",
    regions=["city:Richmond Hill"], categories=["tax"], housing=["owner"],
    amount="Yearly grant on the tax bill (amount set in the annual budget).",
    requirements="Owner 65+ receiving GIS; principal residence owned 1+ year; one per household.",
    action="Apply by Sept 30 each year (by Mar 31 to apply to that year's final bill).",
    url="https://richmondhill.ca/en/online-services/Tax-Assistance-Programs.aspx",
    source="https://www.richmondhill.ca/en/shared-content/resources/documents/Senior-Tax-Grant-2026.pdf",
    status="Annual; deadline Sept 30.", verified="Official 2026 grant document checked Oct 22, 2026.",
    value=val(a=300, t="cash", note="Illustrative; amount set yearly"))
add("york-homelessness-prevention", name="York Region — Homelessness Prevention Program (incl. mortgage arrears)", level="Regional",
    regions=["region:York"], categories=["housing","utility","debt","community"],
    amount="Help with rent, utility or MORTGAGE arrears, utility deposits/reconnection, moving costs.",
    requirements="York resident not on OW/ODSP; at risk of losing housing or utilities; household income up to $47,952 (1) to $126,870 (7+).",
    action="Call Access York 1-877-464-9675. OW/ODSP clients: Housing Stability Program 1-888-256-1112.",
    url="https://www.york.ca/node/44101", phone="1-877-464-9675", status="Open.", verified="Official Region page checked Oct 22, 2026.",
    value=val(o=1500, t="cash", note="Illustrative; amount not published"))

# ---------------- Durham ----------------
add("durham-reassessment-deferral", name="Durham — Reassessment Tax Increase Deferral (seniors and ODSP)", level="Regional",
    regions=["region:Durham"], categories=["tax"], housing=["owner"],
    amount="Defers reassessment-related increases over 5% or $100.",
    requirements="65+ on GIS, or ODSP-eligible.",
    action="Currently closed; reopens with the next province-wide MPAC reassessment.",
    url="https://www.durham.ca/regional-government/property-taxes/",
    status="CLOSED until next reassessment.", verified="Durham Region and Whitby pages checked Oct 22, 2026.",
    value=val(t="financing", note="Program closed"))
add("pickering-tax-grant", name="Pickering — Tax Grant for Low-income Seniors and Persons with Disabilities", level="Municipal",
    regions=["city:Pickering"], categories=["tax"], housing=["owner"],
    amount="$620 (2026).",
    requirements="65+ on GIS, or ODSP; owned and occupied 1+ year.",
    action="Apply by Aug 19 each year (2026 window passed — plan for 2027).",
    url="https://pickering.ca/en/city-hall/grants-and-deferrals.aspx", phone="905-420-4614",
    status="Annual; deadline Aug 19.", verified="Official City page checked Oct 22, 2026.", value=val(a=620, t="cash", note="2026 amount"))
add("oshawa-tax-grant", name="Oshawa — Tax Grant for Low-income Seniors and Persons with Disabilities", level="Municipal",
    regions=["city:Oshawa"], categories=["tax"], housing=["owner"],
    amount="Grant applied to the property tax account.",
    requirements="Low-income senior or person with a disability; occupied 1+ year before Dec 31; one per household.",
    action="Apply Jan 1–Apr 30 each year, online or at Service Oshawa.",
    url="https://www.oshawa.ca/en/home-property/tax-rebates-and-reductions.aspx", status="Annual; Jan 1–Apr 30.",
    verified="Official City page checked Oct 22, 2026.", value=val(a=300, t="cash", note="Illustrative; amount not published"))
add("whitby-seniors-rebate", name="Whitby — Low-income Seniors and Disability Tax Rebate", level="Municipal",
    regions=["city:Whitby"], categories=["tax"], housing=["owner"],
    amount="Yearly property tax rebate (one per roll number).",
    requirements="65+ qualifying for GIS (separate program for low-income homeowners with disabilities); principal residence.",
    action="Apply by Dec 31 each year.",
    url="https://www.whitby.ca/services-and-payments/property-taxes/tax-rebate-and-relief-programs/low-income-seniors/",
    links={}, status="Open; deadline Dec 31.", verified="Official Town page checked Oct 22, 2026.",
    value=val(a=300, t="cash", note="Illustrative; amount not published"))
add("durham-hsp", name="Durham — Housing Stability Program", level="Regional", regions=["region:Durham"], categories=["housing","utility","debt"],
    amount="Up to 2 months of rent or utility arrears, deposits, reconnection fees and moving costs.",
    requirements="Low-income Durham resident behind on rent/utilities or homeless.",
    action="Apply online at forms.durham.ca or call 905-666-6239 ext. 1803.",
    url="https://www.durham.ca/living-here/living-with-low-income/housing-outreach-eviction-prevention-and-utility-and-rent-arrears-resources/",
    phone="905-666-6239 ext. 1803", status="Open.", verified="Official Region page checked Oct 22, 2026.",
    value=val(o=1000, t="cash", note="Illustrative"))

# ---------------- Niagara ----------------
by["neef"].update(dict(amount="Pays electricity or gas arrears to stop disconnection: up to $2,000 per utility once every 24 months.",
    requirements="Niagara resident on OW/ODSP or low income; bill and disconnection notice in your name.",
    action="Apply online through the Discretionary Benefits Portal or call 905-641-9960 ext. 6072.",
    phone="905-641-9960 ext. 6072", status="Open.", checked=TODAY, verified="Official Region page checked Oct 22, 2026.",
    value=val(o=700, t="cash", note="Illustrative; up to $2,000; overlaps LEAP")))
by["niagrenov"].update(dict(name="Niagara Renovates — Repairs and Accessibility",
    amount="Forgivable loan for repairs (written off over 10 years); up to $5,000 accessibility grant.",
    requirements="Household income up to $56,000–$83,500 by bedrooms; home below local average price (e.g. St. Catharines $639,258, Niagara Falls $679,086); assets under $40,000.",
    action="Call 905-980-6000 ext. 3954 to check if 2026 intake has reopened.",
    url="https://www.niagararegion.ca/government/incentive-programs/affordable-housing/renovations.aspx",
    source="https://www.niagararegion.ca/government/incentive-programs/affordable-housing/renovations.aspx",
    phone="905-980-6000 ext. 3954", status="2026 reopening was pending budget — confirm before offering.",
    checked=TODAY, verified="Official Region page and directory (June 2025) checked Oct 22, 2026."))
add("niagara-region-deferral", name="Niagara Region — Tax Increase Deferral (seniors and ODSP)", level="Regional",
    regions=["region:Niagara"], categories=["tax"], housing=["owner"],
    amount="Defers part of a yearly tax increase above $200.",
    requirements="65+ on GIS, or ODSP; owner-occupant 1+ year; taxes up to date.",
    action="Apply to your local municipality by Feb 28 of the following year.",
    url="https://niagarafalls.ca/property-home-and-environment/property-tax-and-assessment/water-and-property-tax-relief-programs/",
    status="Open; deadline Feb 28 following year.", verified="City of Niagara Falls page checked Oct 22, 2026.",
    value=val(a=200, t="financing", note="Illustrative"))
add("niagarafalls-deferral", name="Niagara Falls — Senior/ODSP Property Tax Deferral ($500/yr)", level="Municipal",
    regions=["city:Niagara Falls"], categories=["tax"], housing=["owner"],
    amount="Defers $500 a year for up to 10 years (max $5,000); $150 fee at discharge.",
    requirements="65+ on GIS, or ODSP; principal residence 1+ year; pre-authorized payment plan required.",
    action="Apply Aug 1–Oct 31 each year (2026: by Oct 31).",
    url="https://niagarafalls.ca/property-home-and-environment/property-tax-and-assessment/water-and-property-tax-relief-programs/",
    phone="905-356-7521 ext. 4214", status="Open; deadline Oct 31, 2026.", verified="Official City page checked Oct 22, 2026.",
    value=val(a=500, t="financing", note="Published deferral amount"))
add("niagarafalls-tenant-water", name="Niagara Falls — Tenant Water Rebate (GIS/ODSP)", level="Municipal",
    regions=["city:Niagara Falls"], categories=["utility"], housing=["renter"],
    amount="$102 water account credit.", requirements="Tenant with water account, on GIS or ODSP.",
    action="Apply Aug 1–Oct 31, 2026.", url="https://niagarafalls.ca/property-home-and-environment/property-tax-and-assessment/water-and-property-tax-relief-programs/",
    phone="905-356-7521", status="Open; deadline Oct 31, 2026.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=102, t="bill", note="Published credit"))

# ---------------- Dufferin ----------------
add("dufferin-renovates", name="Dufferin County — Ontario Renovates", level="Regional", regions=["region:Dufferin"], categories=["repairs","access"], housing=["owner"],
    amount="Interest-free loan for necessary repairs and accessibility work.",
    requirements="Moderate-income owner; sole residence in Dufferin; taxes, mortgage and insurance current.",
    action="Call 519-941-6991 ext. 2110 to confirm funding before applying.",
    url="https://www.dufferincounty.ca/housing-services/ontario-renovates-program", source="https://dufferincounty.cioc.ca/record/DUF0023?PrintMd=on",
    phone="519-941-6991 ext. 2110", status="Subject to funding — confirm.", verified="Community directory (2024) checked Oct 22, 2026.",
    value=val(o=10000, t="financing", note="Illustrative; amount not published"))
add("dufferin-tax-relief", name="Dufferin County — Tax Relief for Low-income Seniors and Persons with Disabilities", level="Regional",
    regions=["region:Dufferin"], categories=["tax"], housing=["owner"],
    amount="Rebate of the yearly tax increase (less $50).",
    requirements="65+ eligible for GIS, or on ODSP; owned in Dufferin 1+ year.",
    action="Apply to your town with the final tax bill by Nov 30, 2026.",
    url="https://townofgrandvalley.ca/media/1sjkv1k3/tax-relief-application.pdf", status="Open; deadline Nov 30.",
    verified="County by-law application form checked Oct 22, 2026.", value=val(a=100, t="cash", note="Illustrative"))

# ---------------- Lookup ----------------
ALIASES = {"Scarborough":"Toronto","Etobicoke":"Toronto","North York":"Toronto","East York":"Toronto","Port Credit":"Mississauga",
  "Streetsville":"Mississauga","Meadowvale":"Mississauga","Bolton":"Caledon","Woodbridge":"Vaughan","Maple":"Vaughan","Concord":"Vaughan",
  "Kleinburg":"Vaughan","Unionville":"Markham","Stouffville":"Whitchurch-Stouffville","Keswick":"Georgina","Sutton":"Georgina",
  "Bowmanville":"Clarington","Courtice":"Clarington","Newcastle":"Clarington","Port Perry":"Scugog","Beaverton":"Brock","Cannington":"Brock",
  "Ancaster":"Hamilton","Dundas":"Hamilton","Stoney Creek":"Hamilton","Waterdown":"Hamilton","Binbrook":"Hamilton","Flamborough":"Hamilton",
  "Georgetown":"Halton Hills","Acton":"Halton Hills","Ridgeway":"Fort Erie","Crystal Beach":"Fort Erie","Beamsville":"Lincoln","Vineland":"Lincoln",
  "Fonthill":"Pelham","Smithville":"West Lincoln","Virgil":"Niagara-on-the-Lake","Stoney Ridge":"Hamilton"}
ALIASES.pop("Stoney Ridge")
for a, m in ALIASES.items():
    assert m in mun, m
    lookup["aliases"][a] = m
for r in ["Toronto","Peel","Halton","Hamilton","York","Durham","Niagara","Dufferin"]:
    lookup["coverage"][r] = "researched"

# validate
ids = [p["id"] for p in progs]; assert len(ids) == len(set(ids))
regions = set(mun.values()); cities = set(mun)
for p in progs:
    assert p["url"].startswith("https://"), p["id"]
    for t in p["regions"]:
        if t.startswith("city:"): assert t[5:] in cities, (p["id"], t)
        elif t.startswith("region:"): assert t[7:] in regions, (p["id"], t)
        else: assert t in ("Ontario","Canada"), (p["id"], t)
json.dump(progs, open("programs.json","w"), indent=1, ensure_ascii=False)
json.dump(lookup, open("municipalities.json","w"), indent=1, ensure_ascii=False)
print(len(progs), "programs;", sum(1 for p in progs if p.get("checked")), "checked;", len(lookup["aliases"]), "aliases")
