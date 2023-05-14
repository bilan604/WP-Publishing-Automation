import json
import time

def save_sentences(data):
    with open("data_container/sentences.json", "w") as f:
        json.dump(data, f)

def save_row_numbers(data):
    with open("data_container/row_numbers.json", "w") as f:
        json.dump(data, f)

def save_relevant_data(data):
    with open("data_container/relevant_data_by_row.json", "w") as f:
        json.dump(data, f)

    return

def save_completed_keywords(keywords: list):
    vis = set(get_completed_keywords())
    with open("data_helper_folder/completed_keywords.txt", "r") as f:
        vis = set([line[:-1] for line in f.readlines()])
    
    with open("data_helper_folder/completed_keywords.txt", "a") as f:
        for keyword in keywords:
            if keyword not in vis:
                f.write(keyword+"\n")
    return

def get_completed_keywords():
    # Append string to file
    with open("data_helper_folder/completed_keywords.txt", "r") as f:
        return [s[:-1] for s in f.readlines() if s]
