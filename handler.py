import re
import json
import requests
import asyncio
from bs4 import BeautifulSoup
from parsing import *
from analyzer import get_GPT_statistics_task
import time
from test import *

from data_helper import *
#from wordpress.send_request import *

# Map<str, str>
# sentence_id: sentence
sentences = {}

# Map<str, Map<str, str>>
# filtered_keyword: {aspect: row}
row_numbers = {}

# Map<str, Map<str, set<str>>>
# filtered_keyword: {aspect, set(sentence_id)}
relevant_data_by_row = {}
SIZE_LIMIT =  500



async def get_api_result(api_key, serps_to_check, query):
    
    params = {
        'api_key': api_key,
        'page': 1,
        'max_page': 1,
        'num': min(99, serps_to_check * 10),
        'q': query
    }

    api_result = requests.get('https://api.valueserp.com/search', params)
    return api_result.json()

def filter_blacklisted(organic_results, blacklisted_urls):
    blacklisted_urls = set(blacklisted_urls)
    return [res for res in organic_results if res["domain"] not in blacklisted_urls]

async def get_resp_text_task(link):
    resp = requests.get(link)
    return resp.text


async def get_update_by_keywords_task(keyword, all_text_tags, row, credentials):
    # keyword: unfiltered keyword
    # all_text_tags: data to be stored

    def __get_sentences(all_text_tags):
        # Get sentences from the text tags and filter them
        lst = [re.sub("[^a-zA-Z|0-9|%|.|'| ]", " ", item.lower()) for item in all_text_tags]
        lst = [filter_spacing(li) for li in lst if 6 < len(li.split(" ")) < 65]
        return lst
    
    
    m = 3
    aspect = credentials["aspect"][row]
    for sentence in __get_sentences(all_text_tags):
        # List of letters in the sentence
        sentenceLst = sentence.split(" ")
        # set to range(m, 0, -1) for unigrams
        for gap_size in range(m, 1, -1):
            for i in range(len(sentenceLst)-gap_size+1):
                token = " ".join(sentenceLst[i:i+gap_size])

                # if the token made from above exists as a filtered keyword (keyword without aspect)
                if token in row_numbers and aspect in row_numbers[token]:
                    # get an id
                    id = str(len(sentences))
                    
                    # store the sentence
                    sentences[id] = sentence

                    # find the row number
                    row_key = row_numbers[token][aspect]
                    
                    # token == filtered_keyword
                    relevant_data_by_row[row_key][token].add(id)
    return


async def get_data_task(keyword, link, row, credentials):
    try:
        get_resp_text = asyncio.create_task(get_resp_text_task(link))
        src = await get_resp_text
        soup = BeautifulSoup(src, 'html.parser')
    except:
        print("Crash On Request:", link)
        return

    text_tags = ["p", "b", "h3", "h4", "h5", "li", "text"]
    all_text_tags = []
    for text_tag in text_tags:
        tags = soup.find_all(text_tag)
        tags = list(map(str, tags))
        tags = [re.sub("<(.)+?>", " ", tag) for tag in tags]
        tags = [tag for tag in tags if len(tag) > 15]
        all_text_tags += tags
    
    update_sentences_by_keywords = asyncio.create_task(get_update_by_keywords_task(keyword, all_text_tags, row, credentials))
    await update_sentences_by_keywords
    return
    

async def get_keyword_sentences_task(keyword, organic_results, row, credentials):

    for result in organic_results:
        link = result["link"]
        print(f"Accessing {link=}")
        try:
            await asyncio.wait_for(get_data_task(keyword, link, row, credentials), timeout=10)
            #get_data = asyncio.create_task(get_data_task(keyword, link, row, credentials))
            #await get_data
        except asyncio.TimeoutError:
            print("get_data_task() timed out after 10 seconds")
    
    
    return 


async def get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, row, credentials):
    # For each csv row, containing a list of comma separated keywords
    keywords = re.sub("/",",",keywords)
    for keyword in keywords.split(","):
        # Add 'statistics' back to the search query
        query = keyword
        if "statistics" not in keyword:
            query += " statistics"
        
        get_serp_response = asyncio.create_task(get_api_result(credentials["VALUE_SERP_API_KEY"], num_pages, query))
        serp_response = await get_serp_response

        if not serp_response or serp_response['request_info']['success'] == False:
            print("VALUE SERP API REQUEST NOT SUCESSFUL")
            return
        
        organic_results = serp_response["organic_results"]
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)

        get_keyword_sentences = asyncio.create_task(get_keyword_sentences_task(keyword, organic_results, row, credentials))
        await get_keyword_sentences

        # Safety precaution for saving
        dd = listify(relevant_data_by_row)
        save_relevant_data(dd)
        save_sentences(sentences)
        save_row_numbers(row_numbers)

    return


# main function for handle
async def get_handle_statistics(queries, blacklisted_urls, credentials):
    """
    global sentences, sentence_ids, relevant_data_by_row
    data_container = {"relevant_data_by_row":sentences, "sentence_ids": sentence_ids, "sentence": relevant_data_by_row}
    for file in data_container:
        path = "data_container/" + file + ".json"
        with open(path, "r") as f:
            existing_data = json.loads(f)
            data_container[file] = existing_data
            print("TEST1", existing_data)
    """

    def initialize(queries, credentials):
        credentials["aspect"] = {}
        for rowNo in queries:
            keywords = queries[rowNo]["keywords"]
            row = str(rowNo)
            aspect, filtered_keywords = get_filtered_keywords(keywords)
            aspect = filter_spacing(aspect)
            credentials["aspect"][row] = aspect
                        
            for filtered_keyword in filtered_keywords:
                if not filtered_keyword or not aspect:
                    continue

                if filtered_keyword not in row_numbers:
                    row_numbers[filtered_keyword] = {}
                if aspect not in row_numbers[filtered_keyword]:
                    row_numbers[filtered_keyword][aspect] = row

                # Initialize data storing
                if row not in relevant_data_by_row:
                    relevant_data_by_row[row] = {}
                if filtered_keyword not in relevant_data_by_row[row]:
                    relevant_data_by_row[row][filtered_keyword] = set({})
                
        return credentials
    
    credentials = initialize(queries, credentials)

    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        num_pages = queries[rowNo]["results to check"]
        row = str(rowNo)
        get_relevant_data_by_row = asyncio.create_task(get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, row, credentials))
        await get_relevant_data_by_row
    
    # Prompting
    get_GPT_statistics = asyncio.create_task(get_GPT_statistics_task(credentials))
    await get_GPT_statistics

    """
    # Wordpress
    pages_contents = load_data()
    for page_contents in pages_contents:
        create_post_task = asyncio.create_task(get_api_result(page_contents, "", True, credentials))
        await create_post_task
    """
    return
      


