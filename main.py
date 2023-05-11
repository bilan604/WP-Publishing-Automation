import os
import openaiQuery
import pandas as pd
from handle import *




def main():
    df = pd.read_csv("input.csv")
    
    columns = {}
    for colName in df.columns:
        columns[colName] = list(df[colName])
    
    queries = {}
    for i in range(len(df)):
        queries[i] = {}
        query = " ".join([columns["Keyword1"][i], columns["Keyword2"][i], columns["Keyword3"][i]])
        queries[i]["query"] = query
        queries[i]["SERPNumber"] = columns["SERPNumber"][i]
    
    ###########
    blacklisted_urls = ["www.bloomberg.com"]
    handle(queries, blacklisted_urls)




if __name__ == '__main__':
    path = "c:/Users/bill/github/WP-Publishing-Automation"

    os.chdir(path)

    credentials = {}
    with open(".env", "r") as f:
        lines = f.readlines()
        for row in lines:
            key, value = row.split("=")
            credentials[key] = value
    openaiQuery.api_key = credentials["OPENAI_API_KEY"]

    main()
