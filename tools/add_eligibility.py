"""Add structured age/income eligibility to programs.json (Nov 3, 2026).

Each tagged program gets an "eligibility" object read by the search page:
  minAge / maxAge     age limits for the main (age-based) route
  needsGIS            the age route requires the Guaranteed Income Supplement
  altDisability       ODSP / disability qualifies at any age
  requiresDisability  only people with a disability qualify
  maxIncome           household income limit: a number, or a list by
                      household size [1, 2, 3, 4, 5+] (null = no limit known)
  incomeBasis         "gross" (default), "net" or "after-tax"
  lowIncome           program is for low-income households but publishes
                      no figure; the page hides it only at $100,000+

The page only hides a program when the client's age or income band falls
clearly outside these limits. Net and after-tax limits are compared with
headroom, because the form asks for gross household income.
Programs not listed here are never filtered by age or income.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "programs.json"

LEAP = {"maxIncome": [38000, 54000, 65000, 65000, 71000], "incomeBasis": "after-tax"}
EAP = {"maxIncome": [48220, 68193, 83518, 96439, None], "incomeBasis": "gross"}
GIS_INC = {"maxIncome": [23000, 53500, 53500, 53500, 53500], "incomeBasis": "net"}
LOW = {"lowIncome": True}
SENIOR_GIS = {"minAge": 65, "needsGIS": True}
SENIOR_GIS_OR_DIS = {"minAge": 65, "needsGIS": True, "altDisability": True}
SENIOR_OR_DIS = {"minAge": 65, "altDisability": True}
DIS = {"requiresDisability": True}

E = {
    "oesp": {"maxIncome": 71000, "incomeBasis": "after-tax"},
    "leap": LEAP,
    "neef": LOW,
    "seniortax": {"minAge": 64, "maxIncome": [50000, 60000, 60000, 60000, 60000], "incomeBasis": "net"},
    "gis": {"minAge": 65, **GIS_INC},
    "gains": {**SENIOR_GIS, **GIS_INC},
    "niagrenov": {"maxIncome": 83500},
    "access": SENIOR_OR_DIS,
    "eap": EAP,
    "cdcp": {"maxIncome": 90000, "incomeBasis": "net"},
    "import-5": {"minAge": 65},
    "import-10": EAP,
    "import-13": DIS,
    "fort211salvation": LOW,
    "fort211food": LOW,
    "fort211saeo": LOW,
    "fortwaterrelief": SENIOR_GIS,
    "forttaxdeferral": SENIOR_GIS_OR_DIS,
    **{k: EAP for k in ["eap-fridge", "eap-freezer", "eap-ac", "eap-dehumid", "eap-insulation",
                        "eap-heatpump", "hwp-insulation", "hwp-draft", "hwp-thermostat"]},
    "waterloo-renovates": {"maxIncome": [41210, 51204, 63072, 76577, None]},
    "cambridge-tax-deferral": SENIOR_GIS_OR_DIS,
    "kitchener-tax-deferral": SENIOR_GIS_OR_DIS,
    "cdb": {"minAge": 18, "maxAge": 64, "requiresDisability": True},
    "dtc": DIS,
    "osdcp": {"minAge": 65, "maxIncome": [25480, 42290, 42290, 42290, 42290], "incomeBasis": "net"},
    "oschtc": {"minAge": 65, "maxIncome": 65000, "incomeBasis": "net"},
    "adp": DIS,
    "ow-emergency": LOW,
    "waterloo-city-tax-deferral": SENIOR_GIS_OR_DIS,
    "waterloo-towns-tax-deferral": SENIOR_GIS_OR_DIS,
    "wreap": LEAP,
    "waterloo-atp": {"minAge": 18, "maxIncome": [31875, 45078, None, 63749, None], "incomeBasis": "net"},
    "simcoe-renovates": {"maxIncome": 91000},
    "simcoe-leap": LEAP,
    "barrie-tax-deferral": SENIOR_OR_DIS,
    "simcoe-towns-tax-relief": SENIOR_GIS_OR_DIS,
    "wellington-tax-relief": SENIOR_GIS_OR_DIS,
    "guelph-tax-deferral": SENIOR_GIS_OR_DIS,
    "wellington-energy": LEAP,
    "guelph-bus-pass": {"maxIncome": [27478, None, None, None, None], "incomeBasis": "after-tax"},
    "toronto-tax-relief": {"minAge": 60, "altDisability": True, "maxIncome": 62000},
    "toronto-renovates": LOW,
    "toronto-eef": LOW,
    "toronto-leap": LEAP,
    "toronto-rent-bank": {"maxIncome": [46500, None, None, 66500, None]},
    "toronto-fair-pass": {"minAge": 20, "maxAge": 64, "maxIncome": [23488, None, None, None, None], "incomeBasis": "after-tax"},
    "peel-tax-rebate": SENIOR_GIS_OR_DIS,
    "mississauga-older-adult-subsidies": SENIOR_GIS_OR_DIS,
    "peel-past-due": LOW,
    "peel-transit": {"minAge": 20, "maxIncome": [30255, None, None, 60510, None], "incomeBasis": "net"},
    "halton-increase-deferral": {**SENIOR_OR_DIS, "maxIncome": 69500},
    "halton-older-adult-deferral": {"minAge": 65, "maxIncome": 69500},
    "oakville-seniors-rebate": SENIOR_GIS,
    "burlington-tax-reduction": SENIOR_GIS_OR_DIS,
    "hamilton-seniors-rebate": {"minAge": 65, "maxIncome": 44568},
    "hamilton-tax-deferral": {**SENIOR_OR_DIS, "maxIncome": 44568},
    "hamilton-renovates": {"maxIncome": 60000},
    "hamilton-hef": LOW,
    "york-tax-deferral": {"minAge": 55, "altDisability": True},
    "richmondhill-senior-grant": SENIOR_GIS,
    "york-homelessness-prevention": {"maxIncome": [47952, None, None, None, 126870]},
    "durham-reassessment-deferral": SENIOR_GIS_OR_DIS,
    "pickering-tax-grant": SENIOR_GIS_OR_DIS,
    "oshawa-tax-grant": {**SENIOR_OR_DIS, **LOW},
    "whitby-seniors-rebate": SENIOR_GIS_OR_DIS,
    "durham-hsp": {"maxIncome": [50000, 58000, 65000, 68000, 78000], "incomeBasis": "net"},
    "niagara-region-deferral": SENIOR_GIS_OR_DIS,
    "niagarafalls-deferral": SENIOR_GIS_OR_DIS,
    "niagarafalls-tenant-water": SENIOR_GIS_OR_DIS,
    "dufferin-tax-relief": SENIOR_GIS_OR_DIS,
    "brock-seniors-rebate": SENIOR_GIS,
    "scugog-tax-grant": SENIOR_GIS_OR_DIS,
    "durham-leap-intake": LEAP,
    "oshawa-snow-help": SENIOR_OR_DIS,
    "whitby-windrow": SENIOR_OR_DIS,
    "clarington-snow": SENIOR_OR_DIS,
    "durham-tap": LOW,
}

programs = json.loads(P.read_text())
ids = {p["id"] for p in programs}
missing = set(E) - ids
assert not missing, f"unknown ids: {missing}"
for p in programs:
    if p["id"] in E:
        p["eligibility"] = dict(E[p["id"]])
    else:
        p.pop("eligibility", None)
P.write_text(json.dumps(programs, ensure_ascii=False, indent=1) + "\n")
print(f"tagged {len(E)} of {len(programs)} programs")
