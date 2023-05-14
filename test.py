import json

def save_data(data, file_path):
    # Convert dictionary to string
    data_str = json.dumps(data)

    # Append string to file
    with open(file_path, "a") as file:
        file.write(data_str + "\n")

def load_data(file_path):
    result = []
    with open(file_path, "r") as file:
        for line in file:
            data_str = line.strip()
            if data_str:
                data = json.loads(data_str)
                result.append(data)
    return result

"""
# Example usage

# Save multiple dictionaries in append manner
data1 = {"key1": "value1"}
data2 = {"key2": "value2"}
data3 = {"key3": "value3"}

file_path = "wordpress/page_contents/pages.txt"

save_data(data1, file_path)
save_data(data2, file_path)
save_data(data3, file_path)

# Load data from the file
loaded_data = load_data(file_path)

# Use the loaded data
for data in loaded_data:
    print(data)
"""