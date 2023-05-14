import json


def save_sentences(data):
    old_data = {}
    with open("data_container/row_numbers.json", "r") as f:
        old_data = json.loads(data)
    print(f" {old_data=} ")
    if len(data) >= len(old_data):
        with open("data_container/row_numbers.json", "w") as f2:
            json.dumps(data, f2)
    else:
        print("Skip overwriting data")
    return

def save_row_numbers(data):
    old_data = {}
    with open("data_container/sentences.json", "r") as f:
        old_data = json.loads(data)
    print(f" {old_data=} ")
    if len(data) >= len(old_data):
        with open("data_container/sentences.json", "w") as f2:
            json.dumps(data, f2)
    else:
        print("Skip overwriting data")
    return







def save_relevant_data(data):
    print("Saving data")

    old_data = {}
    with open("data_helper_folder/relevant_data_by_row.json", "r") as file:
        contents = file.readline().strip()
        old_data = json.loads(contents)
    
    for row in data:
        if row not in old_data:
            old_data[row] = []
        for keyword in data[row]:
            if keyword not in old_data[row]:
                # already listified but listification should be done here
                old_data[row][keyword] = list(data[row][keyword])
            else:
                # only update larger storages
                all_ids = old_data[row][keyword] + list(data[row][keyword])
                all_ids = sorted(list(set(all_ids)))
                old_data[row][keyword] = all_ids
    
    
    # Convert dictionary to string
    data_str = json.dumps(old_data)
    print(data_str)
    with open("data_helper_folder/relevant_data_by_row.json", "w") as file:
        json.dumps(data_str, file)

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

def get_completed_keywords(keywords: list):
    # Append string to file
    with open("data_helper_folder/completed_keywords.txt", "r") as f:
        return [s[:-1] for s in f.readlines() if s]
