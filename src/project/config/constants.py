BASE_URL = "https://medicinraadet.dk"

POSITIVE_STATUSES = {    "Anbefalet",# recommended
    "Delvist anbefalet", # partially recommended
    "Direkte indplacering", # direct placement
    "Indplaceres direkte i behandlingsvejledning" #placed directly in treatment guideline
}

LISTING_URL_TEMPLATE = (
    "https://medicinraadet.dk/anbefalinger-og-vejledninger"
    "?page={page}"
    "&order=updated%20desc"
    "&take="
    "&currentpageid=1095"
    "&database=1095"
    "&secondary=1096"
    "&category="
    "&archived=0"
    "&highlight="
    "&q="
    "&period=0"
)
