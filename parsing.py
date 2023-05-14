import re


def filter_spacing(s):
    s = re.sub("\n+?", " ", s)
    s = re.sub(" +", " ", s)
    return s.strip()

def to_key(s):
    s = re.sub("\(.+?\)", "", s)
    s = s.lower()
    s = filter_spacing(s)
    return s

def listify(relevant_data_by_row):
    dd = {}
    for k in relevant_data_by_row:
        dd[k] = {}
        for kk in relevant_data_by_row[k]:
            dd[k][kk] = list(relevant_data_by_row[k][kk])
    return dd

def get_filtered_keywords(keywords):
    ans = []
    keywords = keywords.lower().split(",")
    dd = {}
    for s in keywords:
        c = s.split(" ")
        for word in c:
            if word not in dd:
                dd[word] = 0
            dd[word] += 1
    
    aspect = ""
    for word in dd:
        if dd[word] == len(keywords):
            aspect = word
            break
    for keyword in keywords:
        filtered_keyword = to_key(keyword)    
        filtered_keyword = " ".join([word for word in filtered_keyword.split(" ") if dd[word] < len(keywords)])
        ans.append(filtered_keyword)
    return aspect, ans