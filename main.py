import asyncio
import pandas as pd
from handler import get_handle_statistics

def clear():
    import json
    with open("data_container/relevant_data_by_row.json", "w") as f1:
        json.dump({}, f1)
    with open("data_container/sentences.json", "w") as f2:
        json.dump({}, f2)        
    with open("data_container/row_numbers.json", "w") as f3:
        json.dump({}, f3)


async def main():

    # clears saved data
    #clear()
    
    ######### Overide
    blacklisted_urls = ["www.bloomberg.com", "www.kinsta.com"]

    credentials = {}
    with open(".env", "r") as f:
        lines = f.readlines()
        for row in lines:
            key, value = row.split("=")
            credentials[key] = value
    
    df = pd.read_csv("input.csv")
    queries = {}
    columns = {colName: list(df[colName]) for colName in df.columns}
    for i in range(len(df)):
        queries[i] = {
            "Keywords": columns["Keywords"][i],
            "SERPNumber": columns["SERPNumber"][i],
            "KeywordStatuses": columns["KeywordStatuses"][i]
        }
    
    get_statistics = asyncio.create_task(get_handle_statistics(queries, blacklisted_urls, credentials))
    statistics = await get_statistics
    return statistics


if __name__ == '__main__':
    asyncio.run(main())
