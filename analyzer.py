import re
import json
import openai
import asyncio


responses = {}
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


async def get_prompt_gpt3_task(keywords, page_contents):
    # For all pages for all keywords for a row
    page_contents_string = "\n".join(page_contents)
    if len(page_contents_string) < 250:
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



async def get_GPT_statistics_task():
    
    # for all keywords of all rows which have been loaded to the relevant_data_by_row, row_numbers, and sentences .json files
    with open("row_numbers.json", "r") as row_numbers_file:
        global row_numbers
        row_numbers = json.load(row_numbers_file)
    with open("relevant_data_by_row.json", "r") as relevent_data_by_row_file:
        global relevent_data_by_row
        relevent_data_by_row = json.load(relevent_data_by_row_file)
    with open("sentences.json", "r") as sentences_file:
        global sentences
        sentences = json.load(sentences_file)
    print(row_numbers)
    print(relevent_data_by_row)
    print(type(sentences))
    
    rows = {}
    for keyword in row_numbers:
        row_number = row_numbers[keyword]
        if row_number not in rows:
            rows[row_number] = []
        rows[row_number] += [keyword]
    
    for row_number in rows:
        sentence_ids = relevent_data_by_row[str(row_number)]
        # A list of sentences related to row_number
        row_sentences = [sentences[str(id)] for id in sentence_ids]
        row_sentences = filter_content(rows[row_number], row_sentences)
        print(row_number, row_sentences)

        
        try:
            get_prompt_gpt3 = asyncio.create_task(get_prompt_gpt3_task(rows[row_number], row_sentences))
            prompt_gpt3_response = await get_prompt_gpt3
            print(f" {prompt_gpt3_response=} ")

            with open("responses.txt", "w") as f:
                f.write(str(row_number) + "\n")
                f.write(prompt_gpt3_response)
        except:
            try:
                with open("responses.txt", "w") as f:
                    f.write(prompt_gpt3_response)
            except:
                print("Invalid response format")
                pass

    return prompt_gpt3_response


asyncio.run(get_GPT_statistics_task())
    