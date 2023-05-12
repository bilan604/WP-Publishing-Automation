import re
import json
import requests
import asyncio
from bs4 import BeautifulSoup
from analyzer import get_GPT_statistics_task


relevant_sentences_by_keyword = {}
# id: sentence
sentence_ids = {}
# flip
sentences = {}

row_numbers = {}

# keyword: set(relevant_data.id)
relevant_data_by_row = {}

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

async def get_update_by_keywords(keyword, all_text_tags):
    # for a link for a given keyword
    m = 3
    for text_tag in all_text_tags:
        # generate_id
        sentence = re.sub("[^a-zA-Z|0-9|%|.| ]", " ", text_tag.lower())
        # Skip giant text corpuses
        if len(sentence) >= 2500:
            continue
        sentenceLst = re.sub("( )+?", " ", sentence).split(" ")
        for gap_size in range(m, 0, -1):
            for i in range(len(sentenceLst)-gap_size+1):
                token = " ".join(sentenceLst[i:i+gap_size])
                if token in row_numbers:
                    if sentence not in sentence_ids:
                        id = len(sentence_ids)
                        sentence_ids[sentence] = id
                        sentences[id] = sentence
                    
                    sentence_id = sentence_ids[sentence]
                    # csv row for the keyword
                    row_number = row_numbers[token]
                    # Add the sentence id to the row
                    if row_number not in relevant_data_by_row:
                        relevant_data_by_row[row_number] = set({})
                    # Do not store more than 200 sentences per row
                    if len(relevant_data_by_row[row_number]) < 1000:
                        relevant_data_by_row[row_number].add(sentence_id)
                        break
    return

async def get_sentences_task(keyword, link, credentials):
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
        tags = [re.sub("(\n| )+?", " ", tag) for tag in tags]
        tags = [tag for tag in tags if len(tag) > 15]
        all_text_tags += tags
    update_sentences_by_keywords = asyncio.create_task(get_update_by_keywords(keyword, all_text_tags))
    await update_sentences_by_keywords
    return
    

async def get_keyword_sentences_task(keyword, organic_results, credentials):
    # For each keyword
    for result in organic_results:
        link = result["link"]
        print(f" {link=} ")
        get_sentences = asyncio.create_task(get_sentences_task(keyword, link, credentials))
        await get_sentences
    print(f" {relevant_data_by_row=} ")
    return 


async def get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials):
    # For each csv row, containing a list of comma separated keywords
    for keyword in keywords.split(","):
        # Add 'statistics' back to the search query
        if "statistics" not in keyword:
            keyword += " statistics"
        get_serp_response = asyncio.create_task(get_api_result(credentials["VALUE_SERP_API_KEY"], num_pages, keyword))
        serp_response = await get_serp_response
        organic_results = serp_response["organic_results"]
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)
        get_keyword_sentences = asyncio.create_task(get_keyword_sentences_task(keyword, organic_results, credentials))
        await get_keyword_sentences

        # Safety precaution for saving
        try:
            dd = {}
            for k, v in relevant_data_by_row.items():
                dd[k] = list(v)
            if dd:
                with open("relevant_data_by_row.json", "w") as f1:
                    json.dump(dd, f1)
            if len(sentences) > 50:
                with open("sentences.json", "w") as f2:
                    json.dump(sentences, f2)
            if row_numbers:
                with open("row_numbers.json", "w") as f3:
                    json.dump(row_numbers, f3)
        except:
            print("Error on saving data")
            pass
    return


async def get_handle_statistics(queries, blacklisted_urls, credentials):
    for rowNo in queries:
        keywords = queries[rowNo]["Keywords"]
        for keyword in keywords.split(","):
            filtered_keyword = re.sub("( |\n)+?", " ", keyword.strip().lower())
            ################ Remove statistics from keyword
            if "statistics" in keyword:
                filtered_keyword = re.sub("statistics", "", filtered_keyword).strip()
            if filtered_keyword:  # and all([len(word) > 1 or word in ("a", "i") for word in filtered_keyword.split(" ")])

                # keyword: set(sentence_id)
                relevant_sentences_by_keyword[filtered_keyword] = []
                # used to track the row number of the keyword in the original csv sheet
                row_numbers[filtered_keyword] = rowNo

    for rowNo in queries:
        keywords = queries[rowNo]["Keywords"]
        num_pages = queries[rowNo]["SERPNumber"]
        # for each row
        get_relevant_data_by_row = asyncio.create_task(get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials))
        await get_relevant_data_by_row
    
    get_GPT_statistics = asyncio.create_task(get_GPT_statistics_task(credentials))
    await get_GPT_statistics
    return


