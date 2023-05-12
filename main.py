import asyncio
import pandas as pd
from handling import get_handle_statistics


async def main():

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
    
    ########### Override
    blacklisted_urls = ["www.bloomberg.com"]
    get_statistics = asyncio.create_task(get_handle_statistics(queries, blacklisted_urls, credentials))
    statistics = await get_statistics
    return statistics




if __name__ == '__main__':
    asyncio.run(main())
