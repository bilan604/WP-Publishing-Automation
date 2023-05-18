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
    ##################
    #clears saved data
    clear()
    
    ######### Overide
    blacklisted_urls = ["www.bloomberg.com", "www.kinsta.com", "www.nasdaq.com"]

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
    # override 25
    for i in range(25):
        queries[i] = {
            "keywords": columns["keywords"][i],
            "results to check": columns["results to check"][i],
            "status": columns["status"][i]
        }
    
    get_statistics = asyncio.create_task(get_handle_statistics(queries, blacklisted_urls, credentials))
    await get_statistics
    return 

#company,0,OpenAI,"OpenAI history, OpenAI company profile, OpenAI market capitalization, OpenAI annual report, OpenAI financial statistics, OpenAI revenue breakdown, OpenAI growth trends, OpenAI product sales, OpenAI service sales, OpenAI market share, OpenAI unit sales, OpenAI upcoming products/services, OpenAI operation locations, OpenAI production capacity, OpenAI service delivery statistics, OpenAI user/customer demographics, OpenAI active users/customers, OpenAI customer behavior, OpenAI number of employees, OpenAI employee breakdown, OpenAI diversity report, OpenAI environmental impact, OpenAI carbon footprint, OpenAI renewable energy usage, OpenAI sustainability report, OpenAI stock price, OpenAI dividend yield, OpenAI stock performance, OpenAI comparison with industry peers",30,,openai-statistics
if __name__ == '__main__':
    asyncio.run(main())
