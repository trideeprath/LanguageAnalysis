from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
from pandas import DataFrame as df, Series
from pprint import  pprint
import pandas
import pickle
from LanguageAnalysis.pre_processing import parse_tags_json
import csv
import json
from importlib.machinery import SourceFileLoader
import os
path = os.path.dirname(pandas.__file__)
print(path)

lang_count= {"matlab": 137756, "mysql":993268, "html": 962972, "c": 590590,
             "c++": 1351140, "java": 3097890, "python": 1612969, "javascript": 3187390, "sql": 755760, "swift" : 121459}
complete_tag_list = []

word_meaning_map = pickle.load(open('model/word_meaning_map.pkl', 'rb'))

def language_tag_meaning(create_data= False):
    tags_map = {}
    if create_data is True:
        tags_map = di.get_tags_map(file_read=fp.tags_file)
        pickle.dump(tags_map, open("data/tags_map.pkl", "wb"))
        post_tag = di.get_post_tag(file_read = fp.posts_file_xml)
        pickle.dump(post_tag, open("data/post_tag.pkl", "wb"))
    else:
        tags_map = pickle.load(open("data/tags_map.pkl", "rb"))
        post_tag = pickle.load(open("data/post_tag.pkl", "rb"))
        lang_pair_dict = {}
        for lang1 in post_tag:
            counter_l1 = post_tag[lang1]
            for lang2 in post_tag:
                if lang1 != lang2:
                    print(">>>>>>>", lang1, lang2)
                    counter_l2 = post_tag[lang2]
                    common_counter = counter_l1 & counter_l2
                    common_counter = common_counter.most_common(100)
                    common_counter_tags = [data[0] for data in common_counter]
                    #pprint(common_counter.most_common(20))
                    #print("-----")
                    lang1_list = list(filter(lambda tag_tup: tag_tup[0] not in common_counter_tags, counter_l1.most_common(1000)))[0:20]
                    lang2_list = list(filter(lambda tag_tup: tag_tup[0] not in common_counter_tags, counter_l2.most_common(1000)))[0:20]
                    #print(lang1, lang1_list)
                    #print(lang2, lang2_list)
                    lang1_list_meaning = get_meaning(lang1_list)
                    lang2_list_meaning = get_meaning(lang2_list)
                    common_counter_meaning = get_meaning(common_counter)
                    lang1_dict = json.dumps({lang1: lang1_list_meaning})
                    lang2_dict = json.dumps({lang2: lang2_list_meaning})
                    common_dict = json.dumps({"common": common_counter})
                    #print(common_dict)
                    #print(lang1_dict)
                    #print(lang2_dict)
                    lang_pair_dict[lang1+"-"+lang2] = {"common": common_counter_meaning, lang1: lang1_list_meaning, lang2: lang2_list_meaning}
                    #langpair_json_obj = json.dumps({lang1+"-"+lang2 : {"common": common_counter, lang1: lang1_list_meaning, lang2: lang2_list_meaning}})
                    #print(langpair_json_obj)
    langpair_json_obj = json.dumps(lang_pair_dict)
    with open('data/language_compare_tag_meaning', 'w') as outfile:
        json.dump(langpair_json_obj, outfile)
    print(langpair_json_obj)


def get_meaning(lang_list):
    lang_list_new = []
    for data in lang_list:
        tag = data[0]
        meanings = word_meaning_map[tag]
        meanings = list(map(lambda x: x.lower(), meanings))
        meanings = list(filter(lambda x: (x not in tag) and (tag not in x), meanings))
        lang_list_new.append((tag, data[1], meanings))
        #return word_meaning_map[tag]
    return lang_list_new


if __name__ == '__main__':
    language_tag_meaning(False)
    pass

