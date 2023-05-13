



import requests
import json
import random
from requests.auth import HTTPBasicAuth


def create_post(prompt_data, wpBaseURL, postStatus, credentials):
    #prompt_data: {"keywords": str, "rowNo": str, "content": [{"content_type": str, "link": str}]}
    
    # with open
    prompt_data = json.loads(prompt_data)

    WP_url = wpBaseURL + "/wp-json/wp/v2/posts"

    auth = HTTPBasicAuth(credentials["WORDPRESS_USER"], credentials["WORDPRESS_PASS"])

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = { 
        "status":postStatus,
        "title": prompt_data["content"]["title"],
        "intro": prompt_data["content"]["intro"],
        "statistics_in_groups": prompt_data["content"]["statistics_in_groups"],
        "reference_info": prompt_data["content"]["reference_info"],
        "conclusion": prompt_data["content"]["conclusion"],
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


post_creator("https://jsonplaceholder.typicode.com/posts/5", "<BASE_URL>", "la", "en", "publish")