



import requests
import json
import random
from requests.auth import HTTPBasicAuth


async def create_post(page_data, wpBaseURL, postStatus, credentials):
    #prompt_data: {"keywords": str, "rowNo": str, "content": [{"content_type": str, "link": str}]}
    # with open
    #page_data = json.loads(...)

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

    response = requests.request(
        "POST",
        WP_url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(response)
    return

