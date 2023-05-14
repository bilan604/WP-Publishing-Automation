import os
import re
import json
import openai
import asyncio
from wordpress.send_request import create_post
import time

row_numbers = {}
relevent_data_by_row = {}
sentences = {}


def get_keywords_from_keyword(keyword):
    if not keyword:
        return []
    global row_numbers
    keywords = []
    for __keyword in row_numbers:
        if row_numbers[__keyword] == row_numbers[keyword]:
            keywords.append(__keyword)
    return keywords

def filter_content(keywords, row_sentences):
    # max 300 for 2500 prompt content/context (Not including response and 390 existing prompt)
    row_sentences = [s for s in row_sentences if 10 < len(s) < 300]
    keyword_set = set({})
    for keyword in keywords:
        for word in keyword.lower().split(" "):
            keyword_set.add(word)
    match_counter = {i: sum([1 if word in keyword_set else 0 for word in row_sentences[i].lower().split()]) for i in range(len(row_sentences))}
    # sort the sentences for all keywords queries in the row by how many unique words across all keywords
    # the sentence contains
    match_counter = dict(sorted(match_counter.items(), key=lambda x: x[1], reverse=True))
    # penalty for length?
    row_sentences = [row_sentences[idx] for idx in list(match_counter.keys())]

    total_length = 0
    for j in range(len(row_sentences)):
        total_length += len(row_sentences[j])
        if total_length > 2500:
            row_sentences = row_sentences[:j]
            break

    return row_sentences


async def get_openai_result(prompt):
    #KEY = "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"
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


def parse_response(response):
    if not response:
        return []
    for var in ("response = ", "Response = ", "response=", "Response="):
        if var in response:
            response = response.split(var)[1]
            break
        
    if "[" in response:
        response = response.split("[")[1]
    if "]" in response:
        response = response.split("]")[0]
    
    response = response.split(",")
    response = [r.strip() for r in response]
    return response


def save_response(keyword, response):
    response = parse_response(response)
    with open("responses.txt", "a") as f:
        f.write("KEYWORD:" + keyword + "\n")
        for resp in response:
            f.write(resp + "\n")
    return

def save_page_content(page_data, folder_name="page_contents", file_name= "page_content.json"):
    do = False
    for file in os.listdir():
        if file.find(folder_name) == 0:
            do = True
            break
    
    if not do:
        folder_name = "wordpress/" + folder_name

    with open(folder_name + "/" + file_name, "w") as file:
        json.dump(page_data, file)

    print(f"Page content saved to '{folder_name + file_name}'.")
    return


def get_page_contents_string(lst):
    s = "||||".join(lst)
    s = re.sub("\n", " ", s)
    s = re.sub("( \.( )+?|\. | \.)", ". ", s)
    s = re.sub(" +?", " ", s)
    s = s.split("||||")

    cache = []
    for si in s:

        cache += si.split(".")

    cache = [c.strip() for c in cache]
    s = [ci[0].upper()+ci[1:] for ci in cache if 6 < len(ci.split(" ")) < 500]
    s = ". ".join(s)
    return s


##################################
async def get_content_task(keywords_string, page_contents):
    print("___________________________________\nPrompting")
    
    # For all pages for all keywords for a row
    parsed_responses = []
    total_length = 0
    curr = []
    for i, content in enumerate(page_contents):
        if total_length + len(content) >= 2500:
            print(curr)
            page_contents_string = "\n".join(curr)

            prompt = f"The following text was extracted from a link from a Google search for the keywords \"{keywords_string}\". "
            prompt += f"Please extract and present as much empirical statistical information related to the keywords from the following text as possible:\n"
            prompt += "\"\"\"\n" + page_contents_string + "\n\"\"\"\n"
            prompt += "Format your response as a list of whole sentences separated by commas\n"
            prompt += "i.e.\nresponse = [\"Webinars receive 47% of their views up to ten days after the initial event\", \"The webinar market is projected to reach 800 million by 2023\"]\n"
            print(f" {prompt=} ")

            get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
            response = await get_gpt3_response
            print(f" {response=} ")
            parsed_response = parse_response(response)
            print(parsed_response)
            parsed_responses += parsed_response

            curr = []
            total_length = 0
        else:
            curr.append(content)
            total_length += len(content)
            
    return parsed_responses


async def get_prompt_section_task(keywords, section_type, content):
    print(f" {keywords=} {section_type} {content} ")
    topic = keywords
    if type(topic) != str:
        topic = ", ".join(topic)
    prompt = "Create a " +  section_type + " section for a wordpress blog on " + topic + ".\n"
    prompt += "The content for the site is:\n"
    prompt += "\"\"\"\n" + " ".join(content) + "\n\"\"\"\n"
    print(f" {prompt=} ")
    get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
    response = await get_gpt3_response
    print(f" {response=} ")
    return response


async def generate_page_data(keywords, page_content):
    get_intro_content = asyncio.create_task(get_prompt_section_task(keywords, "intro", page_content))
    intro_content = await get_intro_content

    get_statistics_content = asyncio.create_task(get_prompt_section_task(keywords, "statistics in groups", page_content))
    statistics_content = await get_statistics_content

    get_reference_content = asyncio.create_task(get_prompt_section_task(keywords, "reference info", page_content))
    reference_content = await get_reference_content

    get_conclusion_content = asyncio.create_task(get_prompt_section_task(keywords, "conclusion", page_content))
    conclusion_content = await get_conclusion_content

    get_title_content = asyncio.create_task(get_prompt_section_task(keywords, "title", page_content))
    title_content = await get_title_content

    page_data = {
        "title_content": title_content,
        "intro_content": intro_content,
        "statistics_content": statistics_content,
        "reference_content": reference_content,
        "conclusion_content": conclusion_content
    }

    return page_data


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
    
    for row_number in relevant_data_by_row:
        page_content = []
        keywords = []
        # For each keyword, generate page content and add it to page contents
        for keyword in relevant_data_by_row[row_number]:
            keyword_data = relevant_data_by_row[row_number][keyword]
            keyword_data = list(set(keyword_data))
            sentences_for_keyword = [sentences[str(sentence_id)] for sentence_id in keyword_data]
            
            get_prompt_gpt3 = asyncio.create_task(get_content_task(keyword, sentences_for_keyword))
            filtered_content = await get_prompt_gpt3
            page_content += filtered_content
            
            keywords = get_keywords_from_keyword(keyword)
        

        page_data_task = asyncio.create_task(generate_page_data(keywords, page_content))
        page_data = await page_data_task

        save_page_content(page_data)
        
        keywords_string = ", ".join(keywords)
        
        
# Testing overrides
"""
lst = [
    'when it comes to additional functionalities customers prioritize flexible viewing experiences. webinar marketing statistics further reveal that besides being able to view it at any given time viewers also value receiving slides as a part of a presentation downloading additional resources and the watch later functionality.',
    'research shows that 58% of marketers use webinars as a promotion tool. studies show that between 2% and 5% of webinar attendees eventually make a purchase at the end of the webinar.',
    'industries use webinars for generating leads. so if you have concerns about meeting demand goals just consider these webinar lead generation statistics. a total of 66% of businesses say their sales teams prioritize leads coming from webinars while 72% confirm a direct influence of webinars on pipeline and revenue. a further 78% say they help lower the cost per lead.',
    'surveys show that b2b marketers rely more on webinars and other virtual events of sorts more than their b2c counterparts. 67% of b2b companies have hosted webinars in the past year as opposed to 39% of b2c businesses. b2b webinar statistics further reveal that b2b companies ranked webinars online courses virtual events and blog posts short articles tied at 22% as the best performing content marketing channels.',
    'digital activity peaked after the covid 19 outbreak and remains at all time high levels as professionals embrace a hybrid system of online and in person workflow. marketers have been racing to find the best practices for webinars to cut the noise and stand out among the crowd. webinar statistics demonstrate that most marketers choose to improve audience interaction via polls questions and votes followed by simplicity and ease of use 28% and flexible formats 27% .',
    'the percentage of marketers who run up to 150 webinars per year is satisfactory and amounts to 29%. 80% of organizations hosting training webinars produce as many as 100 webinars per year while a total of 93% of webinars for continuing education are organized 150 times per year according to a webinar benchmarks report.'
]
"""
#asyncio.run(get_GPT_statistics_task())
#asyncio.run(generate_page_data("webinar", lst))