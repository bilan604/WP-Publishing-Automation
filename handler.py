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


# id: sentence
sentence_ids = {}
# flip
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

async def get_update_by_keywords_task(keyword, all_text_tags):
    print("Searching for keywords from link given search query", keyword)
    # for a link for a given keyword
    m = 3

    for text_tag in all_text_tags:
        # generate_id
        sentence = re.sub("[^a-zA-Z|0-9|%|.|'| ]", " ", text_tag.lower())
        sentence = filter_spacing(sentence)

        # Skip giant text corpuses
        if len(sentence) >= 500:
            continue
        sentenceLst = sentence.split(" ")
        for gap_size in range(m, 0, -1):
            for i in range(len(sentenceLst)-gap_size+1):
                token = " ".join(sentenceLst[i:i+gap_size])
                if token in row_numbers:
                    # only store sentences with a matching token
                    if sentence not in sentence_ids:
                        id = len(sentence_ids)
                        sentence_ids[sentence] = id
                        sentences[id] = sentence
                    
                    sentence_id = sentence_ids[sentence]
                    # csv row for the keyword
                    row_number = row_numbers[token]
                    # Add the sentence id to the row's keyword
                    ########################################
                    # Store at most 1000 sentences per keyword
                    relevant_data_by_row[row_number][token].add(sentence_id)
                    
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
    update_sentences_by_keywords = asyncio.create_task(get_update_by_keywords_task(keyword, all_text_tags))
    await update_sentences_by_keywords
    return
    

async def get_keyword_sentences_task(keyword, organic_results, credentials):
    # For each keyword
    key = to_key(keyword)
    for result in organic_results:
        row_number = row_numbers[key]
        if len(relevant_data_by_row[row_number][key]) >= SIZE_LIMIT:
            return

        link = result["link"]
        print(f"Accessing {link=}")
        get_data = asyncio.create_task(get_data_task(keyword, link, credentials))
        await get_data

        ###################################### view
        for row in relevant_data_by_row:
            for keyword in relevant_data_by_row[row]:
                sentence_count = len(relevant_data_by_row[row][keyword])
                if sentence_count > 0:
                    print(f" {keyword}: {sentence_count} sentences")
          
            print(relevant_data_by_row)
        dd = listify(relevant_data_by_row)
        if dd:
            with open("data_container/relevant_data_by_row.json", "w") as f1:
                json.dump(dd, f1)
            with open("data_container/sentences.json", "w") as f2:
                json.dump(sentences, f2)        
            with open("data_container/row_numbers.json", "w") as f3:
                json.dump(row_numbers, f3)
    return 


async def get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials):
    # track the amount of sentences gained
    prev = 0
    # For each csv row, containing a list of comma separated keywords
    for keyword in keywords.split(","):
        # Add 'statistics' back to the search query
        query = keyword
        if "statistics" not in keyword:
            query += " statistics"
        
        get_serp_response = asyncio.create_task(get_api_result(credentials["VALUE_SERP_API_KEY"], num_pages, query))
        serp_response = await get_serp_response
        print(f" \n{keyword=}\n")
        if not serp_response or serp_response['request_info']['success'] == False:
            print("\nVALUE SERP API REQUEST NOT SUCESSFUL\n")
            return
        ##########
        
        organic_results = serp_response["organic_results"]
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)
        get_keyword_sentences = asyncio.create_task(get_keyword_sentences_task(keyword, organic_results, credentials))
        await get_keyword_sentences

        print("\n\n___________________________relevant_data_by_row\n", relevant_data_by_row)
        ##########
        time.sleep(5)
        total = 0
        for row in relevant_data_by_row:
            for keyword in relevant_data_by_row[row]:
                sentence_count = len(relevant_data_by_row[row][row])
                print(keyword, sentence_count)
                total += len(relevant_data_by_row[row][row])
        print(f" GAIN: {total-prev=} ")

        # Safety precaution for saving
        dd = listify(relevant_data_by_row)
        save_relevant_data(dd, "data_container/relevant_data_by_row.json")

        save_sentences(sentences, "data_container/relevant_data_by_row.json")
        save_row_numbers(row_numbers, "data_container/relevant_data_by_row.json")

            
    return


# main function for handle
async def get_handle_statistics(queries, blacklisted_urls, credentials):
    # initialize the maps
    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        rowNo = str(rowNo)
        for keyword in keywords.split(","):
            if keyword != "statistics":
                filtered_keyword = to_key(keyword)
            
            if filtered_keyword:
                # track the row number of the keyword in the original csv sheet
                row_numbers[filtered_keyword] = rowNo
                # keyword: set(sentence_id)
            if rowNo not in relevant_data_by_row:
                relevant_data_by_row[rowNo] = {}
            if filtered_keyword not in relevant_data_by_row[rowNo]:
              relevant_data_by_row[rowNo][filtered_keyword] = set({})

    for rowNo in queries:
        keywords = queries[rowNo]["keywords"]
        num_pages = queries[rowNo]["results to check"]
        # for each row
        get_relevant_data_by_row = asyncio.create_task(get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials))
        await get_relevant_data_by_row

        print("PAUSE")

        time.sleep(15000)
    
    # Prompting
    get_GPT_statistics = asyncio.create_task(get_GPT_statistics_task(credentials))
    await get_GPT_statistics

    pages_contents = load_data()
    for page_contents in pages_contents:
        baseUrl = None
        create_post_task = asyncio.create_task(create_post(page_contents, baseUrl, True, credentials))
        await create_post_task
      


