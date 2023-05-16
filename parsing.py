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
            if not aspect:
                aspect = word
            else:
                aspect += " " + word
    aspect = re.sub("[^a-zA-Z| |\(|\)]", "", aspect)
    for keyword in keywords:
        filtered_keyword = to_key(keyword)    
        filtered_keyword = " ".join([word for word in filtered_keyword.split(" ") if dd[word] < len(keywords)])
        ans.append(filtered_keyword)
    return aspect, ans

def filter_parsed_responses(lst):
    import string
    newLst = []
    for i, s in enumerate(lst):
        letters = list(s)
        while letters and not letters[-1] in string.ascii_letters:
            letters.pop()
        if letters:
            letters.reverse()
            while letters and not letters[-1] in string.ascii_letters:
                letters.pop()
            letters.reverse()
        if letters:
            newLst.append("".join(letters) + ".")
        
    lst = [s for s in newLst if len(s.split(" ")) > 3]
    return lst

def basic_filter(s):
    s = re.sub("\n", " ", s)
    s = re.sub(" +?", " ", s)
    return s

def get_content(parsed_responses):
    contents = []
    total = 0
    for s in parsed_responses:
        for sentence in s.split("."):
            if total + len(sentence) < 4000:
                contents.append(sentence)
            else:
                break
    
    content = ". ".join(contents)
    content = re.sub("\n", " ", content)
    content = re.sub(" +?", " ", content)
    return content

def parse_response2(response2):
    s = ""
    add = False
    for letter in response2:
        if letter == "{":
            add = True
            s += letter
        elif letter == "}":
            s += letter
            add = False
        else:
            if add:
                s += letter
    s = re.sub("\n", "", s)
    return s



#lstt = [': "As of 2021', "Apple's market capitalization increased to 2.533 trillion", 'Apple is one of the most valuable companies in the world with a market capitalization of over 2 trillion as of 2021', 
#'Apple became the first U.S. corporation to surpass 1 trillion in market capitalization in 2018', 'On August 19', "2020 Apple's share price briefly topped 467.77 making Apple the first US company with a market capitalization of 2 trillion", 'Apple was the first American company whose market capitalization reached 1 trillion', 'In 2018 Apple became the first company to ever reach a market capitalization of 1 trillion and a mere two years later the company has broken the record again and more than doubled that figure."', ': Apple is one of the most valuable companies in the world with a market capitalization of over 2 trillion as of 2021', "Apple's share price briefly topped 467.77 making Apple the first US company with a market capitalization of 2 trillion in 2020", 'Apple became the first company to ever reach a market capitalization of 1 trillion in 2018', "Apple's market capitalization increased to 2.533 trillion as"]
#print(filter_parsed_responses(lstt))