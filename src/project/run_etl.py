# import sys
# import os
# from bs4 import BeautifulSoup
# from project.etl.extract_decision import get_decision_entries
# from project.utils.http_client import fetch_html
# from project.etl.extract_detail import parse_detail_page
# from project.config.constants import BASE_URL, LISTING_URL_TEMPLATE



# def run():

#     all_entries = []
#     page = 1

#     while True:

#         url = LISTING_URL_TEMPLATE.format(page=page)
#         print(f"[Page {page}] Fetching: {url}")

#         html = fetch_html(url)
#         if not html:
#             print("No more pages")
#             break

#         #if no raw files it means we're at the end of all pages
#         soup = BeautifulSoup(html, "lxml")
#         raw_items = soup.select("div.database-item")

#         print(f"Page {page} raw items in listing: {len(raw_items)}")

#         if len(raw_items) == 0:
#             print("\n No more pages\n")
#             break

#         # early filtering
#         page_entries = get_decision_entries(html)
#         print(f"Page {page} - positive entries found: {len(page_entries)}\n")

#         all_entries.extend(page_entries)
#         page += 1

# if __name__ == "__main__":
#     run()
import sys
from bs4 import BeautifulSoup

from project.utils.http_client import fetch_html
from project.etl.extract_decision import get_decision_entries
from project.etl.extract_detail import parse_detail_page
from project.config.constants import LISTING_URL_TEMPLATE


# ============================================================
# Stage 2.5 — Pagination + Early Filtering
# ============================================================
def fetch_all_listing_pages():
    print("\nPagination + Early Filtering \n")

    all_listing_entries = []
    page = 1

    while True:
        url = LISTING_URL_TEMPLATE.format(page=page)
        print(f"{page} Fetching: {url}")

        html = fetch_html(url)
        if not html:
            print("Failed to fetch HTML. Stopping pagination.")
            break

        soup = BeautifulSoup(html, "lxml")
        raw_items = soup.select("div.database-item")

        print(f"[Page {page}] Raw items: {len(raw_items)}")

        if len(raw_items) == 0:
            print("\nNo more items\n")
            break

        filtered_entries = get_decision_entries(html)
        print(f"Page {page} Approved entries: {len(filtered_entries)}\n")

        all_listing_entries.extend(filtered_entries)
        page += 1

    print(f"Total filtered listing entries: {len(all_listing_entries)}\n")
    return all_listing_entries


# ============================================================
# Stage 3 — Detail Page Extraction
# ============================================================
def fetch_all_detail_pages(listing_entries):
    print("\n Detail Extraction \n")

    final_records = []

    for idx, entry in enumerate(listing_entries, start=1):

        print(f"[{idx}/{len(listing_entries)}] Fetching detail page:")
        print(f"→ {entry['url']}")

        detail_html = fetch_html(entry["url"])
        if not detail_html:
            print("Failed to fetch detail page. Skipping.\n")
            continue

        detail_data = parse_detail_page(detail_html)

        combined = {
            **entry,
            **detail_data
        }

        final_records.append(combined)
        print("Detail extracted.\n")

    print(f"\n Stage 3 Complete — {len(final_records)} records \n")
    return final_records


# ============================================================
# Preview Helper
# ============================================================
def preview(results, n=3):
    print("=== Showing Preview ===\n")
    for r in results[:n]:
        print(r)
        print("-----\n")


# ============================================================
# Main Runner
# ============================================================
def run():
    listing_entries = fetch_all_listing_pages()
    final_records = fetch_all_detail_pages(listing_entries)
    preview(final_records)
    return final_records


if __name__ == "__main__":
    run()