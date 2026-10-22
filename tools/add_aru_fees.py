"""ARU / secondary-suite building fee and development-charge incentives — researched 2026-10-22. Run from repo root."""
import json
TODAY = "2026-10-22"
progs = json.load(open("programs.json")); by = {p["id"]: p for p in progs}

def val(m=0, a=0, o=0, t="project", note=""):
    return {"monthly": m, "annual": a, "once": o, "type": t, "note": note}
def add(pid, **kw):
    rec = {"id": pid, "categories": ["adu"], "housing": ["owner"], "phone": "", "checked": TODAY}
    rec.update(kw); rec.setdefault("source", rec["url"])
    if pid in by: by[pid].update(rec)
    else: progs.append(rec); by[pid] = rec

add("ontario-aru-dc-exemption", name="Ontario — Development Charge and Parkland Exemption for 2nd and 3rd Units", level="Ontario",
    regions=["Ontario"],
    amount="No municipal or regional development charges and no parkland fee on a 2nd or 3rd unit added to a house (school board charges may still apply in some cities).",
    requirements="Second or third unit in or on the lot of a detached, semi or townhouse. A 4th unit usually pays charges unless a local program waives them.",
    action="Confirm with the city's building department when applying for the permit; check local programs for the 4th unit.",
    url="https://www.mississauga.ca/wp-content/uploads/2026/04/08084145/Gentle-Density-Table-of-Incentives.pdf",
    status="In effect (Development Charges Act and Planning Act, since 2022).",
    verified="Exemption confirmed in City of Mississauga incentives table (Apr 2026) checked Oct 22, 2026.",
    value=val(o=15000, t="project", note="Illustrative charges avoided; varies widely by city"))
add("barrie-aru-fees", name="Barrie — 2026 ARU Incentives (permit fees cut 50%, then fully rebated)", level="Municipal",
    regions=["city:Barrie"],
    amount="50% off building permit, zoning and water fees for a new ARU; the other 50% is rebated if the unit reaches occupancy within 12 months of the permit.",
    requirements="New 2nd, 3rd or 4th unit on a detached, semi or street townhouse lot. Permit applied for and issued in 2026; completed by Dec 31, 2027. Development charges and principal-unit fees not covered.",
    action="Submit the 2026 ARU incentive form with the permit application in APLI; email HousingCIP@barrie.ca after final inspection.",
    url="https://www.barrie.ca/node/15283", phone="705-739-4220 ext. 4416",
    status="Open for 2026 permits while funding lasts.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=3000, note="Illustrative permit fees saved"))
add("mississauga-aru-fee-refund", name="Mississauga — ARU Building Permit Fee Refund", level="Municipal",
    regions=["city:Mississauga"],
    amount="Building permit fees refunded in full when building or legalizing an ARU; 2nd and 3rd units also exempt from most municipal charges.",
    requirements="ARU built or legalized with a permit; all inspections complete. 4th unit charges may be waived through the Affordable Rental CIP (extra terms).",
    action="Nothing to apply for — refund cheque is mailed automatically after final inspection. Questions: 311.",
    url="https://www.mississauga.ca/services-and-programs/building-and-renovating/building-more-units-on-your-property/additional-residential-units/",
    phone="905-615-4311", status="Open.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=2500, note="Illustrative permit fees refunded"))
add("toronto-suite-dc-deferral", name="Toronto — Laneway and Garden Suite Development Charge Deferral", level="Municipal",
    regions=["city:Toronto"],
    amount="Development charges on a laneway or garden suite deferred for 20 years (repayable only if the lot is severed or the deferral isn't assumed on sale).",
    requirements="Suite permitted under the laneway/garden suite by-laws; building permit applied for; sign a DC Deferral Agreement and register it on title.",
    action="Apply to the Housing Secretariat when applying for the permit — do not pay the charges first.",
    url="https://www.toronto.ca/services-payments/grants-incentives-rebates/laneway-garden-suite-development-charges-deferral-program/",
    phone="311", status="Open (page updated Aug 2026).", verified="Official City page checked Oct 22, 2026.",
    value=val(o=20000, t="financing", note="Illustrative charges deferred"))
add("hamilton-adu-grant", name="Hamilton — ADU and Multiplex Housing Incentive Grant", level="Municipal",
    regions=["city:Hamilton"],
    amount="Grant of 70% of eligible costs, up to $40,000 per new unit (max $240,000 per property).",
    requirements="Registered owner; property in the Housing for Hamilton CIP area (not Roxborough); permit issued on/after Oct 9, 2025; occupancy within 18 months of approval or by Aug 4, 2027.",
    action="Apply to the Housing Secretariat (Healthy and Safe Communities Department) before work; funding is discretionary.",
    url="https://www.hamilton.ca/sites/default/files/2026-03/housing-secretariat-ADU-Multiplex-Housing-Incentive-Program-feb2026.pdf",
    status="Open while funds last; occupancy deadline Aug 4, 2027.", verified="City program guidelines (Feb 2026) checked Oct 22, 2026.",
    value=val(o=40000, note="Published per-unit maximum; requires construction spending"))
add("brampton-garden-suite-grant", name="Brampton — Garden Suite Fee Grant", level="Municipal",
    regions=["city:Brampton"],
    amount="Reimburses the registration fee, building permit fee, custom home review fee and education development charges for a garden suite.",
    requirements="Completed garden suite (rear or side yard) registered with the City's Building Division.",
    action="Apply online after the suite is registered; questions to 311.",
    url="https://brampton.ca/EN/Business/planning-development/housing-brampton/Pages/Garden-Suite-Grant-Application.aspx",
    phone="905-874-2000", status="Application page live; 2026 funding not stated — confirm.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=4000, note="Illustrative fees reimbursed"))
add("stcatharines-adu-grant", name="St. Catharines — ADU Grant and Accessible Unit Permit Fee Reimbursement", level="Municipal",
    regions=["city:St. Catharines"],
    amount="Grant up to $40,000 for an interior ADU or $80,000 for a detached ADU; building permit fees reimbursed for units built to accessible standards.",
    requirements="Apply within 90 days of building permit issuance; more than one ADU per property allowed. Accessible reimbursement: unit exceeds Building Code accessibility minimums.",
    action="Apply through the City's Community Improvement Plan (ADU Program) page.",
    url="https://www.stcatharines.ca/building-and-renovating/housing-accelerator-funding/",
    status="Open since Apr 1, 2026 until funding runs out.", verified="Official City page checked Oct 22, 2026.",
    value=val(o=40000, note="Published maximum for interior ADU"))

ids = [p["id"] for p in progs]; assert len(ids) == len(set(ids))
json.dump(progs, open("programs.json", "w"), indent=1, ensure_ascii=False)
print(len(progs), "programs")
