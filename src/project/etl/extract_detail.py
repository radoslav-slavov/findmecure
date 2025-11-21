import re
from bs4 import BeautifulSoup


def parse_detail_page(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    #from title - active ingredient + brand name
    title_tag = soup.select_one("h1.ui.header")
    full_title = title_tag.get_text(strip=True) if title_tag else None

    active_ingredient = None
    trade_name = None

    if full_title:
        match = re.search(r"^(.+?)\s*\((.*?)\)", full_title)
        if match:
            active_ingredient = match.group(1).strip()
            trade_name = match.group(2).strip()

    #helper to extract values from <div class="product-detail">
    def get_detail_value(label_text: str):
        tag = soup.find("div", string=lambda t: t and t.strip() == label_text)
        if not tag:
            return None
        info = tag.find_next("div", class_="product-detail-info")
        if not info:
            return None
        return info.get_text(" ", strip=True)

    # Required fields
    atc_code        = get_detail_value("ATC-kode")
    indication      = get_detail_value("Anvendelse")
    last_updated    = get_detail_value("Sidst opdateret")
    disease_area    = get_detail_value("Sygdomsområde")
    specific_disease = get_detail_value("Specifik sygdom")

    # ----------------------------------------------------
    # 2. Extract recommendation status
    # ----------------------------------------------------
    status_tag = soup.select_one("div.product-process")
    recommendation_status = status_tag.get_text(strip=True) if status_tag else None

    # ----------------------------------------------------
    # 3. Extract recommendation text (if exists on page)
    # ----------------------------------------------------
    rec_tag = soup.select_one("p.attention-text")
    recommendation_text = rec_tag.get_text(" ", strip=True) if rec_tag else None

    # ----------------------------------------------------
    # 4. Extract decision date text ("Godkendt den X")
    # ----------------------------------------------------
    decision_date = None
    date_tag = soup.find(string=lambda t: t and "Godkendt den" in t)
    if date_tag:
        decision_date = date_tag.replace("Godkendt den", "").strip()

    return {
        "full_title": full_title,
        "active_ingredient": active_ingredient,
        "trade_name": trade_name,
        "recommendation_status": recommendation_status,
        "atc_code": atc_code,
        "indication": indication,
        "last_updated": last_updated,
        "decision_date": decision_date,
        "disease_area": disease_area,
        "specific_disease": specific_disease,
        "recommendation_text": recommendation_text,
    }
