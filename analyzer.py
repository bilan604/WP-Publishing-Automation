import re
import openai
import asyncio
import requests
from bs4 import BeautifulSoup


async def get_openai_result(prompt):
    if type(prompt) != str:
        return
    if len(prompt) == 0:
        return "Empty Query Recieved"

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1400)
    return response.choices[0].text


async def prompt_gpt3(keyword, page_content):
    if len(page_content) > 3000:
        page_content = page_content[:3000]
    
    prompt = f"The following text is from a website from the a Google search for \"" + keyword + "\". "
    prompt += f"Please find and summarize all statistics related to \"" + keyword + "\" from the text:\n"
    prompt += "\"\"\"\n" + page_content+ "\n\"\"\"\n"
    prompt += "Format your response in a JSON with the key:value pairs [statistic number]: [the statistic].\n\n"
    prompt += "i.e. keyword = \"webinar market statistics\" and \n"
    prompt += "response = { \n"
    prompt += "    1: \"52% of brands share webinar leads with their sales teams\",\n"
    prompt += "    2: \"Over half consider the quality of leads from webinars to be 'above average'\",\n"
    prompt += "}"
    
    print(f" {prompt=} ")
    get_gpt3_response = asyncio.create_task(get_openai_result(prompt))
    response = await get_gpt3_response
    print(f" {response=} ")
    return response

async def get_resp_task(link):
    resp = requests.get(link)
    return resp

async def get_statistics_task(keyword, link, credentials):
    openai.api_key = credentials["OPENAI_API_KEY"]
    get_resp = asyncio.create_task(get_resp_task(link))
    resp = await get_resp
    if not resp:
        return []
    src = resp.text
    soup = BeautifulSoup(src, 'html.parser')

    ################
    skip_html = True
    if skip_html:
        text_tags = ["p", "h3", "h4", "h5"]
        texts = []
        for text_tag in text_tags:
            tags = soup.find_all(text_tag)
            print(f"1: {tags=} ")
            tags = list(map(str, tags))
            tags = [re.sub("<(.)+?>", " ", tag) for tag in tags]
            tags = [re.sub("\n( )*\n", "\n", tag) for tag in tags]
            print(f"2: {tags=} ")
            tags = [tag for tag in tags if len(tag) > 15]
            texts += tags
        text = "\n".join(texts)
    else:
        text = soup.text

    if len(text) < 300:
        print("Empty Response")
        return []
    get_gpt3_analysis = asyncio.create_task(prompt_gpt3(keyword, text))
    gpt3_analysis = await get_gpt3_analysis
    return gpt3_analysis




    