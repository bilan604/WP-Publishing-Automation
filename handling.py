
import json
import requests
import asyncio
from analyzer import get_statistics_task



async def get_api_result(api_key, serps_to_check, query):
    
    params = {
        'api_key': api_key,
        'page': 1,
        'max_page': 1,
        'num': serps_to_check * 11,
        'q': query
    }

    api_result = requests.get('https://api.valueserp.com/search', params)
    return api_result.json()


def filter_blacklisted(organic_results, blacklisted_urls):

    blacklisted_urls = set(blacklisted_urls)
    return [res for res in organic_results if res["domain"] not in blacklisted_urls]


async def get_keyword_statistics_task(keyword, organic_results, credentials):
    keyword_statistics = []
    for result in organic_results:
        link = result["link"]
        print(f" {link=} ")
        get_statistics = asyncio.create_task(get_statistics_task(keyword, link, credentials))
        statistics = await get_statistics
        keyword_statistics += statistics
    return keyword_statistics


async def get_statistics_by_keywords_task(keywords, num_pages, blacklisted_urls, credentials):
    print(keywords, num_pages, blacklisted_urls, credentials)
    
    statistics_by_keyword = {}
    for keyword in keywords.split(","):
        get_serp_response = asyncio.create_task(get_api_result(credentials["VALUE_SERP_API_KEY"], num_pages, keyword))
        serp_response = await get_serp_response
        organic_results = serp_response["organic_results"]
        # for each keyword
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)
        get_keyword_statistics = asyncio.create_task(get_keyword_statistics_task(keyword, organic_results, credentials))
        statistics_by_keyword[keyword] = await get_keyword_statistics
    return statistics_by_keyword



async def get_handle_statistics(queries, blacklisted_urls, credentials):
    statistics = []
    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        num_pages = queries[rowNo]["SERPNumber"]
        # for each row
        get_statistics_by_keywords = asyncio.create_task(get_statistics_by_keywords_task(keywords, num_pages, blacklisted_urls, credentials))
        statistics_from_keywords = await get_statistics_by_keywords
        statistics += statistics_from_keywords

    return statistics


