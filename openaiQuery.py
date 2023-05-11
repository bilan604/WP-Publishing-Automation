import openaiQuery
import time
from dotenv import load_dotenv

load_dotenv()


async def queryGPT(query):
    print("query", query)
    if type(query) != str:
        return
    if len(query) == 0:
        return "Empty Query Recieved"
    # Check if a command got passed in
    elif len(query) >= 1 and query[0] == "/":
        print("askOpenAI003(): command passed in as query")
        return ""

    message = "No Response"
    try:
        curr_temp = 0.32
        response = openaiQuery.Completion.create(model="text-davinci-003",
                                            prompt=query,
                                            temperature=curr_temp,
                                            max_tokens=1400)
        message = response.choices[0].text
        time.sleep(2)
    except Exception as e:
        print(e)

        time.sleep(2)
    return message
