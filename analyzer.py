import re
import json
import openai
import asyncio
from wordpress.send_request import create_post


row_numbers = {}
relevent_data_by_row = {}
sentences = {}


# Unused
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

def save_page_content(page_data, folder_name, file_name):
                import os
                folder_name = "wordpress"
                file_name = "page_content.json"
                folder_path = os.path.join(os.getcwd(), folder_name)
                file_path = os.path.join(folder_path, file_name)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                with open(file_path, "w") as file:
                    json.dump(page_data, file)

                print(f"Page content saved to '{file_path}'.")
                return


import re
def get_page_contents_string(s):

    s = "||||".join(s)
    s = re.sub("\n", " ", s)
    s = re.sub("( \.( )+?|\. | \.)", ". ", s)
    s = re.sub(" +?", " ", s)

    s = s.split("||||")

    cache = []
    for si in s:

        cache += si.split(".")

    cache = [c.strip() for c in cache]
    s = [ci[0].upper()+ci[1:] for ci in cache if 6 < len(ci.split(" ")) < 50]
    s = ". ".join(s)
    return s
        

async def get_prompt_gpt3_task(keywords_string, page_contents):
    print("___________________________________\nPrompting")

    # For all pages for all keywords for a row
    
    page_contents_string = get_page_contents_string(page_contents)
    if len(page_contents_string) < 100:
        return []
    if len(page_contents_string) >= 2500:
        page_contents_string = page_contents_string[:2500]
    
    prompt = f"The following text was extracted from a link from a Google search for the keywords \"" + keywords_string + "\". "
    prompt += f"Please extract and present as much empirical statistical information related to the keywords from the following text as possible:\n"
    prompt += "\"\"\"\n" + page_contents_string+ "\n\"\"\"\n"
    prompt += "Format your response as a list of whole sentences separated by commas\n"
    prompt += "i.e.\nresponse = [\"Webinars receive 47% of their views up to ten days after the initial event\", \"The webinar market is projected to reach 800 million by 2023\"]\n"
    print(f" {prompt=} ")
    print("___________________")

    try:
        get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
        response = await get_gpt3_response
        print(f" {response=} ")
        return response

    except:
        print("Error on OpenAI API call")
        pass

    return ""



async def get_prompt_section_task(keywords, content_type, section_type, content):
    print("___________________________________\nget_prompt_section_task")

    prompt = f"Create a " +  section_type + "for a wordpress blog on " + ", ".join(keywords) + ".\n"
    prompt += "The " + content_type + " for the site is:\n"
    prompt += "\"\"\"\n" + content + "\n\"\"\"\n"
    print(f" {prompt=} ")
    print("___________________")

    get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
    response = await get_gpt3_response
    print(f" {response=} ")
    return response



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
        for keyword in relevant_data_by_row[row_number]:
            keyword_data = relevant_data_by_row[row_number][keyword]
            keyword_data = list(set(keyword_data))
            sentences_for_keyword = [sentences[str(sentence_id)] for sentence_id in keyword_data]

            gpt3_response = ""
            get_prompt_gpt3 = asyncio.create_task(get_prompt_gpt3_task(keyword, sentences_for_keyword))
            gpt3_response = await get_prompt_gpt3
            page_content += gpt3_response
            
            
            keywords = []
            for __keyword in row_numbers:
                if row_numbers[__keyword] == row_numbers[keyword]:
                    keywords.append(__keyword)
        
        intro_content = get_prompt_section_task(keywords, "content", "intro", page_content)
        conclusion_content = get_prompt_section_task(keywords, "content", "conclusion", page_content)
        statistics_content = asyncio.create_task(get_prompt_section_task(keywords, "content", "statistics in groups", page_content))
        reference_content = get_prompt_section_task(keywords, "content", "reference info", page_content)
        title_content = get_prompt_section_task(keywords, "content", "title", page_content)
        
        page_data = {
            "title_content": title_content,
            "intro_content": intro_content,
            "statistics_content": statistics_content,
            "reference_content": reference_content,
            "conclusion_content": conclusion_content
        }
        save_page_content(page_data)
        keywords_string = ", ".join(keywords)
        post_data = {
            "link": "https://wordpress-923757-3513525.cloudwaysapps.com/",
            "keywords": keywords_string,
            "content": page_data

        }
        WP_url = ""
        
        create_post(page_data, WP_url, True, credentials)





asyncio.run(get_GPT_statistics_task())