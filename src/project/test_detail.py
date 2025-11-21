from project.utils.http_client import fetch_html
from project.etl.extract_detail import parse_detail_page

url = "https://medicinraadet.dk/anbefalinger-og-vejledninger/laegemidler-og-indikationsudvidelser/r/ribociclib-kisqali-tidlig-hrplusher-brystkraeft"

html = fetch_html(url)

result = parse_detail_page(html)

for key, value in result.items():
    print(f"{key}: {value}")
