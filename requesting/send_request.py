



import requests
import json
import asyncio
from requests.auth import HTTPBasicAuth
import requests
import json
import base64
import requests

import tracemalloc
tracemalloc.start()



async def post_request(page_data):
    if not url:
        url = "https://wordpress-923757-3513525.cloudwaysapps.com"

    if "/wp-json/wp/v2/posts" not in url:
        url += "/wp-json/wp/v2/posts"

    # set authentication
    username = ""
    password = ""
    auth = (username, password)    

    # make post request
    response = requests.post(url, data=page_data, auth=auth)

    return response.status_code

#asyncio.run(create_post({}, ""))


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