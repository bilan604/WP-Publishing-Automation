import openaiQuery
import time


def get_openai_result(prompt):
    if type(prompt) != str:
        return
    if len(prompt) == 0:
        return "Empty Query Recieved"

    response = openaiQuery.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1400)
    return response.choices[0].text