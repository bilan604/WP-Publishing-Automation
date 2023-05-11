import re
import openai
import asyncio
import requests
from bs4 import BeautifulSoup


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


async def prompt_gpt3(keyword, page_contents):
    
    page_content = "\n".join(page_contents)
    if len(page_content) < 300:
        return []
    if len(page_content) >= 2200:
        page_content = filter_content(keyword, page_content)
        
    prompt = f"The following text is from a link from the a Google search for \"" + keyword + "\". "
    prompt += f"Please find extract all factual \"" + keyword + "\" related statistics information from the following page text:\n"
    prompt += "\"\"\"\n" + page_content+ "\n\"\"\"\n"
    prompt += "Format your response as a list of complete sentences separated by commas.\n"
    prompt += "i.e.\nresponse = [\"52% of brands share webinar leads with their sales teams\", \"Over half consider the quality of leads from webinars to be 'above average'\"]\n"
    print(f" {len(prompt)=} ")
    
    get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
    response = await get_gpt3_response

    print(f" {response=} ")

    try:
        response = response.json()
        return list(response.values())
    except:
        try:
            return response.split(",")
        except:
            pass
        return []

def filter_content(keyword, page_content):
    keyword_words = set(keyword.lower().split(" "))
    lines = page_content.split("\n")
    contents = {}
    for line in lines:
        words = re.sub("[^a-zA-Z|0-9|%| ]", " ", line.lower())
        words = re.sub("( )+?", " ", words).split(" ")
        terms_matched = sum([1 if word in keyword_words else 0 for word in words])
        if terms_matched not in contents:
            contents[terms_matched] = []
        contents[terms_matched] += [line]

    relevant_content = ""
    contents = {terms_matched: contents[terms_matched] for terms_matched in sorted(list(contents.keys()), reverse=True)}
    
    for match_count in contents:
        if type(match_count) == int and match_count < 1:
            continue
        for sentence in contents[match_count]:
            if len(relevant_content) + len(sentence) >= 2200:
                return relevant_content
            relevant_content += sentence
    return relevant_content

async def get_resp_text_task(link):
    asyncio.sleep(1)
    resp = requests.get(link, verify=False)
    asyncio.sleep(2)
    return resp.text

async def get_statistics_task(keyword, link):
    # for all keywords
    # get {keyword: relevant_statistics}
    get_resp_text = asyncio.create_task(get_resp_text_task(link))
    src = await get_resp_text
    soup = BeautifulSoup(src, 'html.parser')


    ########################
    skip_html = True
    ###########
    if skip_html:
        text_tags = ["p", "b", "h3", "h4", "h5", "li", "text"]
        texts = []
        for text_tag in text_tags:
            tags = soup.find_all(text_tag)
            tags = list(map(str, tags))
            tags = [re.sub("<(.)+?>", " ", tag) for tag in tags]
            tags = [re.sub("(\n| )+?", " ", tag) for tag in tags]
            tags = [tag for tag in tags if len(tag) > 15]
            texts += tags

    # for all keywords:
    # prompt_gpt3(keyword, relevant information)
    
    get_gpt3_analysis = asyncio.create_task(prompt_gpt3(keyword, texts))
    gpt3_analysis = await get_gpt3_analysis
    return gpt3_analysis



    