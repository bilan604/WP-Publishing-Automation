import re


def filter_spacing(s):
    s = re.sub("\n+?", " ", s)
    s = re.sub(" +", " ", s)
    return s.strip()

def to_key(keyword):
    s = re.sub("statistics", "", keyword.lower())
    s = filter_spacing(s)
    return s

def listify(relevant_data_by_row):
    dd = {}
    for k in relevant_data_by_row:
        dd[k] = {}
        for kk in relevant_data_by_row[k]:
            dd[k][kk] = list(relevant_data_by_row[k][kk])
    return dd