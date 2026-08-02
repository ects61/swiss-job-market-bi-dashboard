import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv


def fetch_jobs(app_id, app_key, max_pages=10, results_per_page=50, what_or=None):
    """Fetch Swiss job postings from the Adzuna API with pagination and retry logic."""
    all_dfs = []
    for page in range(1, max_pages + 1):
        for attempt in range(3):
            try:
                params = {
                    "app_id": app_id,
                    "app_key": app_key,
                    "results_per_page": results_per_page,
                }
                if what_or:
                    params["what_or"] = what_or

                response = requests.get(
                    f"https://api.adzuna.com/v1/api/jobs/ch/search/{page}",
                    params=params,
                    timeout=10
                )
            except requests.exceptions.RequestException as e:
                print(f"Page {page}, attempt {attempt+1}: network error ({e})")
                time.sleep(5)
                continue

            if response.status_code == 200:
                break
            elif response.status_code == 429:
                time.sleep(30)
            else:
                time.sleep(5)
        else:
            break

        data = response.json()
        page_df = pd.DataFrame(data["results"])
        if page_df.empty:
            break
        all_dfs.append(page_df)
        time.sleep(1)

    return pd.concat(all_dfs, ignore_index=True)


def load_credentials():
    """Load Adzuna API credentials from .env."""
    load_dotenv()
    return os.getenv("ADZUNA_APP_ID"), os.getenv("ADZUNA_APP_KEY")