import os
import openai
import asyncio
import pandas as pd
from handling import get_handle_statistics
import json
    

async def main():

    path = "c:/Users/bill/github/WP-Publishing-Automation"

    os.chdir(path)

    credentials = {}
    with open(".env", "r") as f:
        lines = f.readlines()
        for row in lines:
            key, value = row.split("=")
            credentials[key] = value
    

    df = pd.read_csv("input.csv")
    
    columns = {}
    for colName in df.columns:
        columns[colName] = list(df[colName])
    
    queries = {}
    for i in range(len(df)):
        queries[i] = {}
        keywords = " ".join([columns["Keyword1"][i], columns["Keyword2"][i], columns["Keyword3"][i]])
        queries[i]["keywords"] = keywords
        queries[i]["SERPNumber"] = columns["SERPNumber"][i]
    
    ###########
    blacklisted_urls = ["www.bloomberg.com"]
    get_statistics = asyncio.create_task(get_handle_statistics(queries, blacklisted_urls, credentials))
    statistics = await get_statistics
    return statistics




if __name__ == '__main__':
    asyncio.run(main())
