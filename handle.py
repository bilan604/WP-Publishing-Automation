from GoogleSearch.SearchAPI import *
import requests
from bs4 import BeautifulSoup


def analyze(link):
    resp = requests.get(link)
    src = resp.text
    soup = BeautifulSoup(src, 'html.parser')
    



def is_blacklisted(link, urls):
    for url in urls:
        if url in link:
            return True
    return False


def handle(queries, blacklisted_urls):
    
    
    
    for query_no in queries:
        query = queries[query_no]["query"]
        pages = queries[query_no]["SERPNumber"]
        links = search(query, pages)
        links = [link for link in links if not is_blacklisted(link, blacklisted_urls)]

        for link in links:
            analysis = analyze(link)
            # 
    search_results = None
    return None
