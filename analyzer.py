import os
import re
import time
import json
import openai
import asyncio
from requesting.send_request import post_request
from parsing import *


row_numbers = {}
relevent_data_by_row = {}
sentences = {}


async def get_openai_result(prompt):
    KEY = "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"

    openai.api_key = KEY

    if type(prompt) != str:
        return
    if len(prompt) == 0:
        return "Empty Query Recieved"

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1000)
    return response.choices[0].text


async def get_content_task(keywords_string, page_contents):
    print("REACHED PROMPT")
    
    print("___________________________________\nPrompting")
    
    # For all pages for all keywords for a row
    parsed_responses = []
    total_length = 0
    curr = []
    for content in page_contents:
        if sum(list(map(len, parsed_responses))) > 4000:
            break
        if total_length + len(content) >= 4000:
            page_contents_string = "\n".join(curr)

            prompt = f"The following text was extracted from a link from a Google search for the keywords \"{keywords_string}\". "
            prompt += f"Please extract and present as much empirical statistical information related to the keywords from the following text as possible:\n"
            prompt += "\"\"\"\n" + page_contents_string + "\n\"\"\"\n"
            prompt += "Format your response as a paragraph.\n"

            get_openai_result_task = asyncio.create_task(get_openai_result(prompt))
            response = await get_openai_result_task

            print(f" {response=} ")
            parsed_responses += [response]

            curr = []
            total_length = 0
        else:
            curr.append(content)
            total_length += len(content)
    
    print(f" {parsed_responses=} ")
    return parsed_responses

async def generate_page_data(topic, content):

    use_content = content[:min(2000, len(content))]

    prompt1 = "Please remember the following information about\"" + topic + "\":\n"
    prompt1 += "\"\"\"\n"
    prompt1 += use_content + "\n"
    prompt1 += "\"\"\"\n"

    prompt1 += "From the information about " + topic + " generate the \"title\", \"intro\", and \"conclusion\" sections for a blog about " + topic + ".\n"
    prompt1 += "Return your response as a Python dictionary with the keys \"title\", \"intro\",  and \"conclusion\".\n"
    print(f" {prompt1=} ")

    #task1 = asyncio.create_task(get_openai_result(prompt1))
    #response1 = await task1


    task1 = asyncio.create_task(get_openai_result(prompt1))
    response1 = await task1
    response1 = parse_response2(response1)
    print(f"RESP2:{response1}")

    try:
        page_data = json.loads(response1)
        page_data["statistics_in_groups"] = content
        #page_data["references"] = ""
        return page_data
        
    except:
        print("Crash converting to json object")
        crash_data = {}
        crash_data["title"] = topic
        crash_data["statistics_in_groups"] = content
        return crash_data


# cache the keywords for the row
def parse_saved_data(relevant_data_by_row, row_numbers, sentences):
    # used for abouts now
    row_keywords = {}
    page_data = {}
    for token in row_numbers:
        for aspect in row_numbers[token]:
            row = row_numbers[token][aspect]
            if row not in page_data:
                page_data[row] = []

            if row not in row_keywords:
                row_keywords[row] = aspect

            for id in relevant_data_by_row[row][token]:
                page_data[row] += [sentences[id]]
    return page_data, row_keywords


async def get_GPT_statistics_task(credentials={}):
    
    # for all keywords of all rows which have been loaded to the relevant_data_by_row, row_numbers, and sentences .json files
    with open("data_container/relevant_data_by_row.json", "r") as relevent_data_by_row_file:
        global relevent_data_by_row
        relevant_data_by_row = json.load(relevent_data_by_row_file)
    with open("data_container/sentences.json", "r") as sentences_file:
        global sentences
        sentences = json.load(sentences_file)
    with open("data_container/row_numbers.json", "r") as row_numbers_file:
        global row_numbers
        row_numbers = json.load(row_numbers_file)
    
    page_data, row_keywords = parse_saved_data(relevant_data_by_row, row_numbers, sentences)
    
    for row in page_data:
        
        get_parsed_responses = asyncio.create_task(get_content_task(row_keywords[row], page_data[row]))
        parsed_responses = await get_parsed_responses

        content = get_content(parsed_responses)
        
        topic = row_keywords[row]
        get_page_data = asyncio.create_task(generate_page_data(topic, content))
        page_data = await get_page_data
        
        with open("page_data.txt", "a") as f:
            try:
                data = json.dumps(page_data)            
                f.write(data + "\n")
                post_request_task = asyncio.create_task(post_request(page_data))
                await post_request_task
            except:
                pass
    return

#dd = {"title": "Apple Inc.: The World\u2019s Largest Corporation in 2021", "intro": "Apple Inc. has come a long way since 1995 and is now the world's largest corporation in 2021 with a market capitalization of 2.533 trillion USD. With solid sales fueled by its popular iPhone products, Apple has become the most profitable technology corporation in the world. This article will look into Apple\u2019s achievements over the past few years and how it has been able to maintain its lead over its competitors.", "conclusion": "Apple has clearly demonstrated its leadership in the technology market and will most likely continue to be on the top for the rest of the year. This can easily be seen from their total market capitalization, their market share, and the fact that their income is largely derived from their iPhone sales. It\u2019s impressive performance over the past few years shows that the company is here to stay.", "statistics_in_groups": " As of 2021, Apple Inc. 's market capitalization increased to 2. 533 trillion, more than double what it was in 2018, when Apple became the first company to ever reach a market capitalization of 1 trillion.  With a market capitalization of 2. 23 trillion USD as of April 2021, Apple Inc.  is regarded as the world's largest corporation in 2021.  Apple's spectacular growth in sales, profits and share price are historically driven by solid sales of its iPhone products and the company is now the most profitable technology corporation in the world. . As of 2021, Apple is the first US Company to have a market capitalization of over 2 trillion, significantly more than India's GDP of 3. 03 trillion.  Apple achieved this milestone in August 19, 2020, when its share price briefly topped 467. 77.  Since then, Apple has more than doubled its original market capitalization of 1 trillion, reaching 2. 533 trillion as of 2021.  The annual reports since 1995 can be seen from the website with the greatest change being seen in 2018 when it was first to reach a market capitalization of one trillion US dollars. .  Apple's revenues have been divided between its various products and services over the last few years.  In 2020, iPhone product sales decreased by 3%, iPad product sales increased by 11%, Mac product sales increased by 11%, Services sales increased by 16%, and Other products increased by 25%.  Apple's iPhone revenue alone contributes to over 60% of their income.  Looking at the market shares, Apple holds a worldwide market share for iPhones, while the Apple Watch has a market share compared to the competition, and MacOS has a version market share worldwide from 2018 to 2023.  In the US, their market share for SVOD services during Q4 2020 was recorded as well.  Finally, since 2010, Apple has maintained a global iOS market share. .  The following statistical information is related to the keywords \"Apple\": In the US, Apple is by far the strongest player in market share among smartphone brands, with a market share of 57. 62% in the first quarter of 2020.  Additionally, Apple had the highest share of the worldwide smartwatch shipment market in the first quarter of 2020 at 47. 9%, followed by Samsung at 13. 4%.  Further, various iterations of the iPhone 12 alone represent a 15% market share of global smartphones.  In 2019, Apple had a 47% market share in the premium smartphone segment, which dropped by 8% compared to the first quarter of 2018.  In 2020, Apple sold 20 million Mac and MacBook Units and had a 7. 6% market share following market leaders Lenovo (24%) and HP Inc.  (22. 4%).  In terms of mobile operating systems, Apple's iOS had a market share of 61. 47% worldwide as of May 2021.  Additionally, Apple's iOS market share went from 20. 3% in January 2018 to an estimated 38. 8% in January 2023.  Furthermore, Apple was the winner in the smartwatch category with a global market share of 52. 5% in Q2 of 2021. .  In Q4 of 2022, Apple holds 34. 1% of the global smartwatch market share and 15. 6% of the global iPhone market share.  In Q2 of 2022, Samsung recorded 21. 8% market share, leading Apple among major competitors.  During the last month of 2018, Android had 42. 75% market share in the US.  In the first quarter of this year, Apple's market share in China dropped to 13%.  Apple has 65% market share among smartphone vendors in the United States.  Wordpress also boasts a 30. 1% market share among website CMS engines in 2020.  As of Q4 of 2020, Apple holds 21. 8% of the global smartwatch operating system market share.  Lastly, Apple shipped 194 million iPads and Macs in 2020, which is around 11. 9% of the tablet and PC market share. .  In 2019, Apple held the largest market share for products in the world, and recorded more net sales than the iPad.  According to data released by Counterpoint Research, Apple held a 41. 5% market share of smartphones in the United States.  Additionally, international business machines corporation and Walmart Inc.  hold respective market shares of x. x%.  Apple's market share of global smart speaker shipments fluctuated between 3rd quarter 2016 and 1st quarter 2022, while the market share of SVOD services during Q4 2020 was x. x% in the US.  Apple also held the majority market share for True Wireless Earphones in Q2 of 2020, and a whopping 67% market share for navigation applications, compared to 12% for Waze, 11% for Apple Maps, and 8% for MapQuest.  Apple Watch continues to hold the largest market share and is the most popular smartwatch in the world.  Mac and Macbook units sold by Apple in 2020 amounted to 20 million, giving them a market share of 7. 6%, following market leaders Lenovo (24%), HP Inc. (22. 4%), and Dell (16. 6%). "}
#print(list(dd.keys()))
#asyncio.run(get_GPT_statistics_task())
