from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
from pandas import DataFrame as df, Series
from pprint import  pprint
import pickle
from LanguageAnalysis.pre_processing import parse_tags_json
import csv

lang_count= {"matlab": 137756, "mysql":993268, "html": 962972, "c": 590590,
             "c++": 1351140, "java": 3097890, "python": 1612969, "javascript": 3187390, "sql": 755760, "swift" : 121459}
def language_usecase(create_data= False):
    tags_map = {}
    if create_data is True:
        tags_map = di.get_tags_map(file_read=fp.tags_file)
        pickle.dump(tags_map, open("data/tags_map.pkl", "wb"))
        post_tag = di.get_post_tag(file_read = fp.posts_file_xml)
        pickle.dump(post_tag, open("data/post_tag.pkl", "wb"))
    else:
        tags_map = pickle.load(open("data/tags_map.pkl", "rb"))
        post_tag = pickle.load(open("data/post_tag.pkl", "rb"))
        #pprint(tags_map)
        #pprint(post_tag_list)
    web_tags = parse_tags_json.get_tags_map('data/web_tags')
    db_tags = parse_tags_json.get_tags_map('data/dba_tags')
    datascience_tags = parse_tags_json.get_tags_map('data/datascience_tags')
    system_tags = parse_tags_json.get_tags_map('data/system_tags')
    front_end_tags = parse_tags_json.get_tags_map('data/front_end_tags')
    lang_domain_tuple = []
    header = ["language", "web-dev", "database", "datascience", "system-dev", "user-interface"]
    for lang in post_tag.keys():
        #print(lang)
        tag_counter = post_tag[lang]
        web_sum = get_tag_sum(tag_counter, web_tags) * 100/lang_count[lang]
        #print("web ", web_sum/lang_count[lang])
        db_sum = get_tag_sum(tag_counter, db_tags) * 100/lang_count[lang]
        #print("db ", db_sum//lang_count[lang])
        ds_sum = get_tag_sum(tag_counter, datascience_tags) * 100/lang_count[lang]
        #print("ds ", ds_sum/lang_count[lang])
        system_sum = get_tag_sum(tag_counter, system_tags) * 100/lang_count[lang]
        #print("system ", system_sum/lang_count[lang])
        fe_sum = get_tag_sum(tag_counter, front_end_tags) * 100/lang_count[lang]
        #print("front-end ", fe_sum/lang_count[lang])
        #print("==================================")
        total = web_sum + db_sum + ds_sum + system_sum + fe_sum
        factor = 100/total
        web = int(web_sum*factor)
        db = int(db_sum*factor)
        ds = int(ds_sum*factor)
        system = int(system_sum*factor)
        fe = int(fe_sum*factor)
        tag_tuple = (lang, web, db, ds, system, fe)
        lang_domain_tuple.append(tag_tuple)

    with open('data/language_domain.csv','w') as out:
        writer = csv.writer(out)
        writer.writerow(header)
        for lang_tup in lang_domain_tuple:
            writer.writerow(lang_tup)


    #pprint(lang_domain_tuple)




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
    language_usecase(False)
    pass

