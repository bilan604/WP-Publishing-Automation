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


# sentence: sentence_id
sentences = {}

row_numbers = {}

# rowNo: Keyword: Set(str) 
relevant_data_by_row = {}
SIZE_LIMIT =  500



async def get_api_result(api_key, serps_to_check, query):
    
    params = {
        'api_key': api_key,
        'page': 1,
        'max_page': 1,
        'num': min(99, serps_to_check * 11),
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


async def get_update_by_keywords_task(keyword, all_text_tags, credentials):
    print("Searching for keywords from link given search query", keyword)

    # Get sentences from the text tags and filter them
    __sentences = []
    for i, text_tag in enumerate(all_text_tags):
        if len(text_tag) > 60:
            for item in text_tag.lower().split("."):
                sentence = re.sub("[^a-zA-Z|0-9|%|.|'| ]", " ", item)
                __sentences.append(sentence)
            continue
        
        sentence = re.sub("[^a-zA-Z|0-9|%|.|'| ]", " ", text_tag.lower())
        __sentences.append(sentence)
    
    # a list of sentences
    __sentences = [filter_spacing(sentence) for sentence in __sentences]
    # Var for when data is stored already and the python file is run again
    # Prevents rewrites, but quite unlikely
    existing_sentences = 0

    m = 3
    aspect = credentials["aspect"]
    for sentence in __sentences:
        # List of letters in the sentence
        sentenceLst = sentence.split(" ")
        for gap_size in range(m, 0, -1):
            for i in range(len(sentenceLst)-gap_size+1):
                token = " ".join(sentenceLst[i:i+gap_size])
                
                # Exists as a keyword
                if token in row_numbers:
                    if aspect not in row_numbers[token]:
                        continue
                    
                    print("sentence found via token", token)
                    # only store sentences with a matching token
                    id = len(sentences) + existing_sentences
                    if sentence not in sentences:
                        sentences[id] = sentence
                    
                    # Add the sentence id to the row's keyword
                    relevant_data_by_row[row_numbers[token][aspect]][token].add(id)
                    
    return

async def get_data_task(keyword, link, credentials):
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
        tags = [filter_spacing(tag) for tag in tags]
        tags = [tag for tag in tags if len(tag) > 15]
        all_text_tags += tags
    update_sentences_by_keywords = asyncio.create_task(get_update_by_keywords_task(keyword, all_text_tags, credentials))
    await update_sentences_by_keywords
    return
    

async def get_keyword_sentences_task(keyword, organic_results, credentials):

    for result in organic_results:
        
        link = result["link"]
        print(f"Accessing {link=}")
        get_data = asyncio.create_task(get_data_task(keyword, link, credentials))
        await get_data
        print("\n\nkeyword", keyword)
        print("\n\nsentences", sentences)
        print(f" {relevant_data_by_row=} ")
        ###################################### view
        for row in relevant_data_by_row:
            for keyword in relevant_data_by_row[row]:
                sentence_count = len(relevant_data_by_row[row][keyword])
                if sentence_count > 0:
                    print(f" {keyword}: {sentence_count} sentences")
        """
        dd = listify(relevant_data_by_row)
        print("len(dd)", len(dd))
        if dd:
            with open("data_container/relevant_data_by_row.json", "w") as f1:
                json.dump(dd, f1)
            with open("data_container/sentences.json", "w") as f2:
                json.dump(sentences, f2)        
            with open("data_container/row_numbers.json", "w") as f3:
                json.dump(row_numbers, f3)
        """
    return 


async def get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials):
    # track the amount of sentences gained
    prev = 0
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
            print("\nVALUE SERP API REQUEST NOT SUCESSFUL\n")
            return
        ##########
        
        organic_results = serp_response["organic_results"]
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)

        get_keyword_sentences = asyncio.create_task(get_keyword_sentences_task(keyword, organic_results, credentials))
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

    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        row = str(rowNo)
        aspect, filtered_keywords = get_filtered_keywords(keywords)
        credentials["aspect"] = aspect
        print(f" {filtered_keywords=} ")
        for filtered_keyword in filtered_keywords:
            
            if not filtered_keyword:
                continue
            if filtered_keyword not in row_numbers:
                row_numbers[filtered_keyword] = {}
                row_numbers[filtered_keyword][aspect] = row
                # keyword: aspect: set(sentence_id)
                # i.e. safety policy: alphabet: set({1,2,50,7})
            if row not in relevant_data_by_row:
                relevant_data_by_row[row] = {}
            if filtered_keyword not in relevant_data_by_row[row]:
                relevant_data_by_row[row][filtered_keyword] = set({})

    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        num_pages = queries[rowNo]["results to check"]
        # for each row
        get_relevant_data_by_row = asyncio.create_task(get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials))
        await get_relevant_data_by_row
    
    # Prompting
    get_GPT_statistics = asyncio.create_task(get_GPT_statistics_task(credentials))
    await get_GPT_statistics

    # Wordpress
    pages_contents = load_data()
    for page_contents in pages_contents:
        create_post_task = asyncio.create_task(get_api_result(page_contents, "", True, credentials))
        await create_post_task
      
    return
      


