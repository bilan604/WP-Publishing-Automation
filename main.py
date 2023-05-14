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
    ##############################
    #clears saved data
    #clear()
    
    ######### Overide
    blacklisted_urls = ["www.bloomberg.com", "www.kinsta.com"]

    credentials = {}
    with open(".env", "r") as f:
        lines = f.readlines()
        for row in lines:
            key, value = row.split("=")
            credentials[key] = value
    
    df = pd.read_csv("Statistics Pages Automation - Sheet1.csv")
    queries = {}
    columns = {colName: list(df[colName]) for colName in df.columns}

    ################################################
    ################################################
    ################################################
    for i in range(3):
        queries[i] = {
            "keywords": columns["keywords"][i],
            "results to check": columns["results to check"][i],
            "status": columns["status"][i]
        }
    
    get_statistics = asyncio.create_task(get_handle_statistics(queries, blacklisted_urls, credentials))
    await get_statistics
    return 

if __name__ == '__main__':
    asyncio.run(main())
