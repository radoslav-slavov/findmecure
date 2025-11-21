from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.constants import BASE_URL, POSITIVE_STATUSES


def get_decision_entries(html: str):
    """parses a group of decisions/items and filters based on the set of statuses"""

    soup = BeautifulSoup(html, "lxml")
    results = []

    items = soup.select("div.database-item")

    for item in items:
        a_tag = item.find("a",href=True)
        if not a_tag:
            continue

        relative_url = a_tag["href"]
        detail_url = urljoin(BASE_URL,relative_url)

        title_tag = item.select_one("h3.database-item-title")
        title = title_tag.get_text(strip=True) if title_tag else None

        status_tag = item.select_one(".database-item-status")
        listing_status = status_tag.get_text(strip=True) if status_tag else None

        if listing_status is not None:
            if listing_status not in POSITIVE_STATUSES:
                continue
        
        results.append({
            "url": detail_url,
            "title": title,
            "listing_status": listing_status,
        })

    return results
