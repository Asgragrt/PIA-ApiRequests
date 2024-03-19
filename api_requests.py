import requests
import manga_data
import time

base_url = "https://api.mangadex.org"

last_request = 0
# 5 requests per second
request_rate = 1 / 5

def verify_limit():
    global last_request
    if (dt := (time.time() - last_request)) <= request_rate:
        time.sleep(dt)
    last_request = time.time()

def api_search(title):
    try:
        verify_limit()
        r = requests.get(
            f"{base_url}/manga",
            params={
                "title": title,
                "order[followedCount]": "desc" 
                }
        )

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        
    return r.json().get("data", None)

def api_stats(manga_dict):
    try:
        manga_id = manga_data.get_id(manga_dict)
        verify_limit()
        r = requests.get(
            f"{base_url}/statistics/manga/{manga_id}"
            )
        #return r.json(), manga_id
        return r.json()

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)