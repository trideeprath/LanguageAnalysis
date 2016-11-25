from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
from pandas import DataFrame as df, Series
from pprint import  pprint
import pickle
from LanguageAnalysis.pre_processing import parse_tags_json
import csv

lang_count= {"matlab": 137756, "mysql":993268, "html": 962972, "c": 590590,
             "c++": 1351140, "java": 3097890, "python": 1612969, "javascript": 3187390, "sql": 755760, "swift" : 121459}

def language_tags(create_data= False):
    tags_map = {}
    if create_data is True:
        post_tag = di.get_post_tag(file_read = fp.posts_file_xml)
        pickle.dump(post_tag, open("data/post_tag.pkl", "wb"))
    else:
        post_tag = pickle.load(open("data/post_tag.pkl", "rb"))

    with open('data/language_tags.csv','w') as out_file:
        writer= csv.writer(out_file)
        writer.writerow(["language", "tag", "count"])
        for lang in post_tag:
            print(lang)
            tag_counter = post_tag[lang]
            top_tags = tag_counter.most_common(30)
            for tag in top_tags:
                writer.writerow([lang, tag[0], tag[1]])


def get_tag_sum(lang_counter,tag_list):
    count = 0
    for tag in tag_list:
        if tag in lang_counter.keys():
            #print(tag, lang_counter[tag])
            count += lang_counter[tag]
    return count


def save_counts(file_read, file_write):
    data = df.from_csv(file_read)
    answer_count = Series.to_frame(data.groupby(['language'])['answer_count'].sum())
    question_count = Series.to_frame(data.groupby(['language'])['post_type'].count())
    answer_count = answer_count.reset_index()
    question_count = question_count.reset_index()
    question_count.columns = ['language', 'question_count']
    merge = df.merge(question_count, answer_count, on=['language', 'language'])
    merge['total'] = merge.question_count + merge.answer_count
    merge['ratio'] = merge.answer_count / merge.question_count
    merge.to_csv(file_write)


if __name__ == '__main__':
    language_tags(False)
    pass

