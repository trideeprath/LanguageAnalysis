import json
from pprint import pprint

def get_tags_map(file_read):
    domain_list = []
    with open(file_read) as data_file:
        data = json.load(data_file)
        items = data['items']
        for item in items:
            domain_list.append(item['name'])
    return domain_list

#tags = get_tags_map("data/web_tags")