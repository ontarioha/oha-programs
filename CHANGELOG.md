# Changelog

## 2026-11-08: Weekly check
- 146 programs reviewed: 144 confirmed against official pages (checked dates set to 2026-11-08), 25 changed, 2 added, 2 couldn't be checked. 148 programs in total.

Changes:
- Durham Housing Stability Program: link moved from durham.ca/en/living-here/housing-supports.aspx → durham.ca/living-here/housing-and-homelessness/housing-supports/
- Whitby ADU Fee Reimbursement: CLOSED to new permits (ended Dec 31, 2025) → OPEN until Dec 31, 2026 (permits issued on/after Apr 1, 2024; permit application complete by Dec 31, 2026)
- Whitby ADU Fee Reimbursement: reimbursed fees now also include the below-grade entrance fee; education development charges only for detached ADUs
- Whitby ADU Fee Reimbursement: link moved to whitby.ca/services-and-payments/building-and-renovating/additional-dwelling-units/
- Brock Low-income Seniors Rebate: requirements → add property owned 1+ year and tax account paid in full for the rebate year (per Township policy)
- Clarington Tax Cancellation: described as hardship relief (sickness/extreme poverty) → official page and Section 357 form list only property-based reasons (renovation 3+ months, fire/demolition, change of use, exemption, assessment error); sickness/extreme poverty not offered
- Clarington Tax Cancellation: phone 905-623-3379 ext. 2650 → 905-623-3379 (ext. 2650 is listed only for bills on properties no longer owned)
- Clarington Tax Cancellation: link moved to clarington.net/homes-and-property/property-taxes-and-assessments/
- Oshawa Section 357 hardship relief: no deadline listed → must be received by Feb 28 of the following year (2026 taxes: Feb 28, 2027); late applications not accepted
- Oshawa Section 357 hardship relief: link moved to oshawa.ca/living-here/property-taxes/tax-rebates-and-reductions/
- Home Renovation Savings: status 'no end date; unconfirmed extension to Nov 2026' → official terms set Nov 30, 2026 (attic completion, follow-up assessment booking) and Dec 31, 2026 (assessment completion, smart thermostat) cut-offs
- HRS insulation rebate: status 'Open' → open but follow-up assessment must be booked by Nov 30, 2026 and completed by Dec 31, 2026
- HRS standalone attic rebate: status 'Open' → work must be completed by Nov 30, 2026
- HRS smart thermostat rebate: status 'Open' → offer ends Dec 31, 2026 (claim within 60 days of purchase)
- HRS air sealing rebate: status 'Open' → open but follow-up assessment must be booked by Nov 30, 2026 and completed by Dec 31, 2026
- HRS heat pump water heater rebate: status 'Open' → open but follow-up assessment must be booked by Nov 30, 2026 and completed by Dec 31, 2026
- HRS energy assessment rebate: status 'Open' → open but follow-up assessment must be booked by Nov 30, 2026 and completed by Dec 31, 2026
- Multigenerational Home Renovation Tax Credit: value note said 'nonrefundable' → CRA says the credit is refundable (note corrected; amounts unchanged)
- Ontario Seniors Care at Home Tax Credit: eligibility minimum age in data was 65 → 70 (matches the official page and the record's own requirements text)
- Wellington Tax Relief: action/status said 'DEADLINE Nov 1, 2026 … call Monday Nov 2' → 2026 deadline passed; next deadline Nov 1, 2027 (late 2026 only if Treasury agrees)
- Dufferin Ontario Renovates: status 'Subject to funding, confirm' → not listed on the County's current Housing Services pages; availability unconfirmed, call before quoting
- Dufferin Ontario Renovates: link moved from old /housing-services/ontario-renovates-program page → County Housing Services page
- Dufferin Ontario Renovates: phone 519-941-6991 ext. 2110 (from 2024 directory) → 519-941-6991 (County Housing Services main line)
- Toronto Property Tax, Water and Solid Waste Relief: Open, deadline Nov 2 → 2026 deadline (Nov 2, 2026) has passed; wait for 2027 intake
- Toronto Renovates: Intake not confirmed → no longer listed by the City (program page redirects to a general homeowner-support page); do not offer
- Peel Backwater Valve Rebate: source link was the old .asp page → current Region page
- Peel Emergency Help with Past-due Bills: link peelregion.ca/help/past-due-bills now redirects → new 'Keep housing and avoid eviction' page
- Cambridge Seniors and Disability Property Tax Deferral: status 'deadline was Nov 1, call Monday Nov 2' → '2026 window closed; next deadline Nov 1, 2027'
- Kitchener Seniors and Disability Property Tax Deferral: deadline Nov 1, 2026 → 2026 window closed; next deadline Nov 1, 2027
- City of Waterloo Seniors and Disability Property Tax Deferral: deadline Nov 1, 2026 (today) → 2026 window closed; next deadline Nov 1, 2027
- Waterloo Region townships Seniors and Disability Property Tax Deferral: deadline Nov 1, 2026 → 2026 window closed; next deadline Nov 1, 2027
- Brampton Garden Suite Fee Grant: Application page live, funding not stated → CLOSED as of July 21, 2025 (per City Garden Suites page)

Added:
- Pickering — Seniors and Persons with Disabilities Snow Clearing
- Mississauga — Basement Flooding Prevention Rebate

Needs a decision: Brampton Garden Suite Grant closed (July 21, 2025) — hide or remove; Toronto Renovates no longer listed by the City — consider removing; Dufferin Ontario Renovates not on County site; Whitby ADU incentive reopened through Dec 31, 2026; Clarington tax record no longer a hardship program — consider removing from hardship searches.
Couldn't check: Hamilton — Ontario Renovates (repairs and accessibility), Salvation Army Fort Erie — Utility Assistance Intake.

## 2026-11-03: Age and income eligibility tags
- Added an `eligibility` field to 85 of 146 programs (age limits, GIS requirement, disability route, household income limits by size). Built by `tools/add_eligibility.py`.
- The search page uses these tags to hide programs a client clearly can't qualify for. Net and after-tax limits are compared with 30% headroom because the form asks for gross income; "low income" programs with no published figure are hidden only at $100,000+.
- Programs without the field are never filtered by age or income.

## 2026-11-01: Durham Region deep-dive (Oshawa and surrounding)
- 14 programs added, 1 updated. 146 programs in total. Durham now has 19 local listings (was 5).

Added:
- Durham Greener Homes Loan: 2% loan up to $125,000 over 15 years for energy/renovation work (all Durham except Pickering)
- Durham Greener Homes: free renovation coach + free Weather-ready Home Assessment (all Durham)
- Durham LEAP intake: Community Development Council Durham, 905-686-2661 (Elexicon and Oshawa Power customers)
- Oshawa Power: Arrears Management, Compassion Fund, Rainy Day Fund
- Durham water bill payment help (60+ due-date extension)
- Durham Region Transit Assistance Program: $53.76/month unlimited for OW/ODSP
- Oshawa Tax Relief for sickness or extreme poverty (Section 357)
- Clarington property tax cancellation/reduction (hardship)
- Brock Low-income Seniors Tax Rebate: $355 (deadline Sept 30)
- Scugog Tax Grant for low-income seniors/ODSP: $375 (deadline Aug 31)
- Oshawa Snow Clearing Help for seniors/disabled (open to Dec 18)
- Whitby free windrow clearing (2026 registration closed Nov 1)
- Clarington snow clearing for seniors/disabled, $107.69 (closed Oct 31)
- Whitby ADU fee reimbursement (closed to new permits Dec 31, 2025)

Updated:
- Durham Housing Stability Program: added arrears caps ($3,000–$4,000), income limits ($50,000 for 1 to $78,000 for 7+), phone 905-668-4113 ext. 3474, area outreach workers

Not found: no Ontario Renovates / home repair program currently offered by Durham Region; no seniors tax rebate published by Ajax or Uxbridge.
Search: added community names Orono, Brooklin, Ashburn, Claremont, Sunderland, Blackstock, Greenbank, Hampton and others.

## 2026-11-01: Weekly check
- 132 programs reviewed: 127 confirmed against official pages (checked dates set to 2026-11-01), 32 changed, 0 added, 5 couldn't be checked. 132 programs in total.

Changes:
- Oakville Seniors Property Tax Rebate: Open (deadline Oct 31) → CLOSED for 2026; watch for 2027 form
- Niagara Falls Senior/ODSP Tax Deferral: Open, deadline Oct 31 → closed for 2026; next intake Aug 1–Oct 31, 2027
- Niagara Falls Tenant Water Rebate: Open, deadline Oct 31 → closed for 2026; watch for 2027 dates
- Fort Erie Seniors Utility Relief Fund: open window → 2026 window closed Oct 31; credit applied in November; next window May 1, 2027
- Cambridge, Kitchener and Waterloo townships tax deferrals: "Open; deadline Nov 1" → 2026 deadline passed Nov 1 (Sunday); call Monday about late applications; next deadline Nov 1, 2027
- City of Waterloo tax deferral: "Open; deadline Nov 1" → deadline today; email revenue@waterloo.ca, otherwise next deadline Nov 1, 2027
- Wellington County Tax Relief: Open, deadline Nov 1 → 2026 deadline passed; next deadline Nov 1, 2027
- Toronto Property Tax/Water/Solid Waste Relief: "Open; deadline Nov 2" → deadline is tomorrow (Mon Nov 2); closed after that
- York Region Tax Deferral: "deadline Sept 30" → 2026 window closed; next Sept 30, 2027; Aurora form link → new address
- Richmond Hill Senior Tax Grant: "deadline Sept 30" → 2026 window closed; reapply 2027
- Pickering Tax Grant: "deadline Aug 19" → 2026 window closed; next Aug 19, 2027; link → new City page
- Oshawa Tax Grant: "Jan 1–Apr 30" → 2026 window closed, reopens Jan 1, 2027; link → new City page; phone (blank) → 905-436-3311
- Guelph Greener Homes: "PAUSED to new registrations" → loans closed (waitlist only), low-income heat pump grants available but limited; 2-person income limit $66,595 → $68,193
- Guelph Affordable Bus Pass: 1-person income limit $26,926 → $27,478
- Wellington-Guelph Housing Stability Programme: phone 519-837-2670 x3712 → 519-837-6274 x3712
- Wellington-Guelph Emergency Energy/LEAP: phone 519-837-2670 x3712 → 519-837-6274 x3712 (County: 519-843-7000); LEAP noted as for Guelph Hydro customers
- Wellington-Guelph Housing Allowance: phone 519-824-7822 x4060 → 519-837-6274 x4060
- Hamilton Housing Emergency Fund: phone (blank) → 905-546-2424 ext. 6555; caps added ($3,000 single to $7,000 for 5+ over 24 months); source library directory → City info sheet
- Hamilton Protective Plumbing (3P): link → corrected City page; source business-aid site → City Jan 2026 form; loan described as up to $2,000 at 4% over 10 years
- Hamilton Ontario Renovates: link → new City page address; source health directory → City application form
- St. Catharines ADU Grant: "$80,000 detached" → "$80,000 exterior" (City wording); phone (blank) → 905-688-5600
- Fort Erie Community Improvement Plan: vague amount → itemized Downtown Core/Brownfield/Gateway incentives; noted as business/redevelopment only, not general homeowner repairs; phone (blank) → 905-871-1332
- Kitchener Stormwater Credit: email stormwater@kitchener.ca → stormwaterutility@kitchener.ca; link → current page address
- Niagara Emergency Energy Fund: link → new Niagara Region page
- OESP: source oeb.ca/node/121 → full OEB OESP page
- LEAP (United Way Simcoe Muskoka): source health directory → United Way LEAP FAQ
- Simcoe towns tax relief: Innisfil and Wasaga Beach links → towns' new web pages
- Barrie Bonus, Barrie 2026 ARU Incentives, Barrie Water/Wastewater Relief: short node links → full City page addresses

Needs a decision: Oakville, Niagara Falls (2) and other closed-for-2026 listings could be hidden until 2027; Guelph Greener Homes grants are open again; Fort Erie CIP is business-only (consider removing "repairs"/owner match); Hamilton duplicate (import-18) still listed; Toronto Renovates still unconfirmed.
Couldn't check: City of Waterloo ARU Grant, Fort Erie Salvation Army utility help (211), Fort Erie Tax Deferral, Toronto Renovates, Dufferin Ontario Renovates.

## 2026-10-25: Weekly check
- 130 programs reviewed: 125 confirmed against official pages (checked dates set to 2026-10-25), 23 changed, 2 added, 5 couldn't be checked. 132 programs in total.

Changes:
- Multigenerational Home Renovation Tax Credit: 15% (up to $7,500) → 14.5% (up to $7,250); source → CRA line 45355 page
- Home Accessibility Tax Credit: link → current CRA page (".../completing-a-tax-return/...")
- Canada Disability Benefit: source news article → official Canada.ca amount page
- Canadian Dental Care Plan: phone (blank) → 1-833-537-4342
- Home and Vehicle Modification Program (March of Dimes): phone (blank) → 1-877-369-4867
- Region of Waterloo Affordable Secondary Suite Funding: amount "set in fact sheet" → up to $25,000 forgivable loan (incl. up to $5,000 accessibility grant), forgiven over 15 years
- GRT Affordable Transit Program: 50% off → 55% off; income limits added (e.g. $31,875 for 1 person); status Open → online application temporarily unavailable, apply by phone 519-883-2100 option 1; link → new GRT page
- Guelph Transit Affordable Bus Pass: phone (blank) → 519-822-1811
- Toronto Basement Flooding Protection Subsidy: link → new City page address
- Toronto HELP: rates 3.95%–5.20% → 3.83%–5.12%; loan capped at 10% of assessed value; link → new City page
- TTC Fair Pass: link → new City page address
- Peel Property Tax Rebate: old .asp link → new Peel Region page
- Oakville Seniors Property Tax Rebate: status Open → deadline Oct 31, 2026 (no late applications); source directory → Town 2026 form
- Burlington Property Tax Reduction: link → official program page; vague requirements → City criteria (65+ on GIS or ODSP, owner-occupant 1+ year, one property, taxes paid)
- Hamilton ADU / Multiplex Incentive (import-18): homepage link and "needs live confirmation" → official program page and details; marked as a duplicate of the Hamilton ADU and Multiplex Housing Incentive Grant listing
- Hamilton Seniors Tax Rebate: "yearly credit" → $241 (2026) plus $175 utility rebate with metered water; source → City 2026 form
- Hamilton Tax Increase Deferral: "income limit applies" → combined income $44,568 or less (2026); link 2024 form → 2026 form
- Richmond Hill Senior Tax Assistance Grant: phone (blank) → 905-771-8949
- Whitby Low-income Seniors Tax Rebate: phone (blank) → 905-430-4300
- Dufferin Tax Relief: phone (blank) → 519-941-2816 ext. 2810
- Fort Erie Affordable Housing ADU, Study and Per Door grants: "amount to confirm" → up to $20,000 per eligible property/project (max $500,000 per project)

Added:
- Barrie Low-Income Household Water/Wastewater Relief (40% of the bill, up to $60 per bill for six bills; owners and renters)
- Niagara Falls Temporary Property Tax Penalty and Interest Credit (50% of 2026–2027 penalty and interest once paid in full; apply by Feb 29, 2028)

Needs a decision: Hamilton duplicate listing (import-18) can be removed; Toronto Renovates may be discontinued (not listed on City pages).
Couldn't check: Toronto Renovates, Hamilton Ontario Renovates, Hamilton Housing Emergency Fund, Dufferin Ontario Renovates, Fort Erie Community Improvement Plan.

## 2026-10-22: Building fee and ARU incentives
- Added 7 programs that cut building permit fees or development charges, or give grants, for adding a unit: Ontario-wide development charge exemption for 2nd/3rd units; Barrie 2026 ARU incentives (permit fees cut 50% then fully rebated); Mississauga permit fee refund; Toronto garden/laneway suite charge deferral; Hamilton ADU grant (up to $40,000/unit); Brampton garden suite fee grant; St. Catharines ADU grant (up to $40,000/$80,000).
- Already in the list: Kitchener ADU grant, City of Waterloo ARU grant, Barrie Bonus, Simcoe and Waterloo secondary suite funding.
- Checked and not added: Guelph multi-unit grant (5+ units, closed July 2026); Peel second unit program (on hold); Burlington affordable ARU grant (closed); Oshawa and Clarington (no incentive found).

## 2026-10-22: Ring 2 added
- Added local programs for Toronto, Peel (Mississauga, Brampton, Caledon), Halton, Hamilton, York Region, Durham, Niagara and Dufferin: 38 new programs, 2 rewritten (Toronto basement flooding, Niagara Renovates), 1 updated (Niagara Emergency Energy Fund).
- 123 programs in total; 113 checked against official or official-directory sources.
- Added 37 community names to the city lookup (e.g. Scarborough → Toronto, Bowmanville → Clarington, Ancaster → Hamilton).
- Links still to confirm: Oakville and Burlington tax pages (taken from community directory listings), Dufferin County Ontario Renovates page.
- Upcoming deadlines: Niagara Falls deferral Oct 31; Toronto tax/water relief Nov 2; Dufferin tax relief Nov 30; Peel and Burlington rebates Dec 31.
- Closed or paused: Durham reassessment deferral (until next MPAC reassessment); Halton older-adult full deferral (reopens spring 2027); Toronto Hydro heat pump program (full, not added).

## 2026-10-21: First version (Ring 1)
- Converted 55 Version 12 records into a single list. Province-wide and federal programs re-checked against official sources.
- Added Ring 1 local programs for Simcoe County (Barrie, Orillia and 16 towns), Waterloo Region (Kitchener, Waterloo, Cambridge and 4 townships) and Guelph and Wellington County.
- Added the Canada Disability Benefit, Disability Tax Credit, Ontario Seniors Dental Care Program, Seniors Care at Home Tax Credit, Assistive Devices Program and Ontario Works Emergency Assistance.
- 85 programs in total; 72 checked on 2026-10-21. The other 13 (Niagara/Fort Erie, Toronto and Hamilton entries) are marked as not re-checked.
- Known gaps: no City of Orillia tax relief program found; no Wellington County home repair program for homeowners found; Guelph Greener Homes paused to new registrations.
