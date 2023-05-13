import re
import json
import openai
import asyncio
import string


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
                                        max_tokens=1500)
    return response.choices[0].text


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


def parse_response(response):
    if not response:
        return []
        
    if "response = " in response:
        response = response.split("response = ")[1]

    add = False
    currString = ''
    statistics = []
    for letter in response:
        if letter == '\"':
            if not add:
                add = True
            else:
                add = False
                statistics += [re.sub("\n", " ", currString)]
                currString = ''
        else:
            if add:
                currString += letter

    return statistics


def save_response(keyword, response):
    response = parse_response(response)
    with open("responses.txt", "w") as f:
        f.write("KEYWORD:" + keyword + "\n")
        for resp in response:
            f.write(resp + "\n")
        


        

async def get_prompt_gpt3_task(keywords, page_contents):
    print("___________________________________\nPrompting")
    print(f" {keywords=} ")
    print(f" {page_contents} ")

    # For all pages for all keywords for a row
    page_contents_string = "\n".join(page_contents)


    if len(page_contents_string) < 100:
        return []
    if len(page_contents_string) >= 2200:
        page_contents_string[:2200]
    
    keywords_string = ",".join(keywords)
    prompt = f"The following text was extracted from a link from a Google search for the keywords \"" + keywords_string + "\". "
    prompt += f"Please extract and present as much empirical statistical information related to the keywords from the following text as possible:\n"
    prompt += "\"\"\"\n" + page_contents_string+ "\n\"\"\"\n"
    prompt += "Format your response as a list of whole sentences separated by commas\n"
    prompt += "i.e.\nresponse = [\"52% of brands share webinar leads with their sales teams\", \"Over half consider the quality of leads from webinars to be 'above average'\"]\n"
    print(f" {prompt=} ")

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
        for keyword in relevant_data_by_row[row_number]:
            keyword_data = relevant_data_by_row[row_number][keyword]
            keyword_data = list(set(keyword_data))
            sentences_for_keyword = [sentences[str(sentence_id)] for sentence_id in keyword_data]
            
            print(sentences_for_keyword)
            get_prompt_gpt3 = asyncio.create_task(get_prompt_gpt3_task(keyword, sentences_for_keyword))
            try:
                gpt3_response = await get_prompt_gpt3
                save_response(keyword, gpt3_response)
                print(f" {gpt3_response=} ")
            except:
                print("Error on GPT3 prompting")


    return




asyncio.run(get_GPT_statistics_task())