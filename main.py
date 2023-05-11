import pandas as pd



def main(path):
    df = pd.read_csv(path)
    
    columns = {}
    for colName in df.columns:
        columns[colName] = list(df[colName])
    
    queries = {}
    for i in range(len(df)):
        queries[i] = {}
        query = " ".join([columns["Keyword1"][i], columns["Keyword2"][i], columns["Keyword3"][i]])
        queries[i]["query"] = query
        queries[i]["SERPNumber"] = columns["SERPNumber"][i]



if __name__ == '__main__':
    path = "input.csv"
    main(path)
