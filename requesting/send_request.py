



import requests
import json
import asyncio
from requests.auth import HTTPBasicAuth


async def create_post(page_data, wpBaseURL, postStatus, credentials):
    #prompt_data: {"keywords": str, "rowNo": str, "content": [{"content_type": str, "link": str}]}
    
    ########## Override
    wpBaseURL = "https://wordpress-923757-3513525.cloudwaysapps.com/"

    WP_url = wpBaseURL + "/wp-json/wp/v2/posts"

    auth = HTTPBasicAuth(credentials["WORDPRESS_USER"], credentials["WORDPRESS_PASS"])

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = { 
        "status":postStatus,
        "title": page_data["content"]["title"],
        "intro": page_data["content"]["intro"],
        "statistics_in_groups": page_data["content"]["statistics_in_groups"],
        "reference_info": page_data["content"]["reference_info"],
        "conclusion": page_data["content"]["conclusion"],
    }

    print(payload)
    print("STOPPING\n\n---------------------------")
    import time
    time.sleep(15000)
    response = requests.request(
        "POST",
        WP_url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(response)
    return

async def fetch_data(link, params):
    response = requests.get(link, params)
    return response

async def get_api_result(api_key, num_pages, query):
    params = {
        'api_key': api_key,
        'q': query,
        "page": 1,
        "max_page": 1,
        "num": num_pages,
        
    }
    get_response = asyncio.create_task(fetch_data("https://api.valueserp.com/search", params))
    response = await get_response
    return response