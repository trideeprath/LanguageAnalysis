
import csv
import pandas as pd
import xml.etree.ElementTree
import re
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from collections import Counter
lang_list = ['java', 'python', 'matlab', 'html', 'c++', 'c', 'mysql','javascript', 'sql','swift']

def integrate_questions(file_read,file_write):
    """
    :param file_read: reads the file containing question
    :param file_write: writes the integrated data to the file
    :return
    creates a csv of (language, all_question_tex)
    """
    in_pd = pd.read_csv(file_read)
    in_pd_grouped = in_pd.groupby("language")
    write_map = {}
    for language,group in in_pd_grouped:
        title_list = list(group["title"])
        write_map[language] = ". ".join(title_list)

    with open(file_write,'w') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['language','question_title'])
        for language,title in write_map.items():
            csv_writer.writerow([language,title])





def parse_xml_language_similarity(file_read,file_write):
    count = 0
    with open(file_read,'r') as f, open(file_write,'w') as out:
        for line in f:
            count +=1
            if count %1000 == 0: print(count)
            if "row Id" in line:
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    body = remove_tags(root.get('Body'))
                    title = remove_tags(root.get('Title'))
                    body_sentences = sent_tokenize(body)
                    title_sentences = sent_tokenize(title)
                    for line in body_sentences:
                        out.write(line+"\n")
                    for line in title_sentences:
                        out.write(line+"\n")
                except:
                    continue


def get_tags_map(file_read):
    tag_map = {}
    with open(file_read, 'r') as inp:
        for line in inp:
            if "row Id" in line:
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    id = remove_tags(root.get("Id"))
                    tag_name = remove_tags(root.get("TagName"))
                    count = root.get("Count")
                    tag_map[tag_name] = count
                except Exception as e:
                    print(e)
                    continue
    return tag_map


def get_post_tag(file_read):
    tag_map = defaultdict(Counter)
    for lang in lang_list:
        tag_map[lang] = Counter()

    count = 0
    with open(file_read, 'r') as inp:
        for line in inp:
            if "row Id" in line:
                count += 1
                if count % 10000 == 0:
                    perc = count * 100 / 32209819
                    print(str(perc) + " % done")
                    if perc > 20:
                        break;
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    id = remove_tags(root.get("Id"))
                    tags_text = root.get("Tags")
                    tag_list = []
                    if tags_text is None:
                        tags = ""
                    else:
                        tags = parse_tags(tags_text).lower()
                        tag_list = tags.split(",")
                        common_list = list(set(tag_list).intersection(lang_list))
                        if len(common_list) !=0:
                            for lang in common_list:
                                for tag in tag_list:
                                    if tag not in lang_list:
                                        tag_map[lang].update([tag])
                except Exception as e:
                    print(e)
                    continue
    return tag_map


def get_post_common_tag(file_read):
    tag_map = defaultdict(Counter)
    for lang in lang_list:
        for lang_sec in lang_list:
            if lang !=lang_sec:
                tag_map[lang+"-"+lang_sec] = Counter()

    count = 0
    with open(file_read, 'r') as inp:
        for line in inp:
            if "row Id" in line:
                count += 1
                if count % 10000 == 0:
                    perc = count * 100 / 32209819
                    print(str(perc) + " % done")
                    if perc > 50:
                        break;
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    id = remove_tags(root.get("Id"))
                    tags_text = root.get("Tags")
                    tag_list = []
                    if tags_text is None:
                        tags = ""
                    else:
                        tags = parse_tags(tags_text).lower()
                        tag_list = tags.split(",")
                        common_list = list(set(tag_list).intersection(lang_list))
                        if len(common_list) == 2:
                            for tag in tag_list:
                                if tag not in lang_list:
                                    tag_map["-".join(common_list)].update([tag])
                except Exception as e:
                    print(e)
                    continue

    for lang_pair in list(tag_map.keys()):
        counter_obj = tag_map[lang_pair]
        if len(list(counter_obj.elements())) == 0:
            tag_map.pop(lang_pair, None)

    return tag_map


def parse_xml_questions(file_read, file_write):
    count = 0
    with open(file_read, 'r') as inp, open(file_write, 'w') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(['id','post_type','language','answer_count','date'])
        for line in inp:
            count += 1
            if count % 10000 == 0:
                perc = count * 100 / 32209819
                print(str(perc) + " % done")
                if perc > 50:
                    break;
            if "row Id" in line:
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    id = remove_tags(root.get("Id"))
                    post_type = remove_tags(root.get("PostTypeId"))
                    tags_text = root.get("Tags")
                    tag_list = []
                    if tags_text is None:
                        tags = ""
                    else:
                        tags = parse_tags(tags_text).lower()
                        tag_list = tags.split(",")

                    ans_count = root.get("AnswerCount")
                    if ans_count is None:
                        ans_count = ""
                    else:
                        ans_count = remove_tags(ans_count)
                    date = remove_tags(root.get("CreationDate"))
                    #print(id,post_type,tags,ans_count,date)
                    if int(post_type) == 1 and bool(set(tag_list) & set(lang_list)):
                        lang = get_common_tag(tag_list)
                        row = [id, post_type, lang, ans_count, date]
                        #csv_writer.writerow(row)
                except Exception as e:
                    print(e)
                    continue


def integrate_language_posts(file_read, file_write):
    count = 0
    data_map = defaultdict(list)
    for lang in lang_list:
        data_map[lang] = []
    with open(file_read, 'r') as inp, open(file_write, 'w') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(['language','document'])
        for line in inp:
            count += 1
            if count % 10000 == 0:
                perc = count * 100 / 32209819
                print(str(perc) + " % done")
                if perc > 80:
                    break;
            if "row Id" in line:
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    id = remove_tags(root.get("Id"))
                    post_type = remove_tags(root.get("PostTypeId"))
                    tags_text = root.get("Tags")
                    body = remove_tags(root.get("Title"))
                    tag_list = []
                    if tags_text is None:
                        tags = ""
                    else:
                        tags = parse_tags(tags_text).lower()
                        tag_list = tags.split(",")
                    if bool(set(tag_list) & set(lang_list)) and len(body) > 10:
                        lang = get_common_tag(tag_list)
                        data_map[lang].append(body)
                        #csv_writer.writerow(row)
                except Exception as e:
                    #print(e)
                    continue

    with open(file_read, 'r') as inp, open(file_write, 'w') as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(['language', 'body'])
        for lang in data_map:
            all_post = " .".join(data_map[lang])
            csv_writer.writerow([lang, all_post])



def get_common_tag(tag_list):
    for tag in tag_list:
        if tag in lang_list:
            return tag

def parse_xml_user_location(file_read,file_write):
    lang_list = [' java ','python','matlab','html','c++',' c ','mysql','swift',' javascript ','sql']
    write_list = []
    with open(file_read,'r') as f:
        for line in f:
            if "row Id" in line:
                line = line.strip()
                root = xml.etree.ElementTree.fromstring(line)
                try:
                    aboutMe = remove_tags(root.get('AboutMe')).lower()
                    location = remove_tags(root.get('Location'))
                    for lang in lang_list:
                        if lang in aboutMe:
                            temp_tuple = (lang.strip(), location)
                            write_list.append(temp_tuple)
                except:
                    continue

    for tuple in write_list:
        print(tuple)

    with open(file_write, 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        for row in write_list:
            thedatawriter.writerow(row)
    print(file_write)

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    output = TAG_RE.sub('', text)
    output = output.replace("<p>"," ")
    output = output.replace("<", " ")
    output = output.replace(">", " ")
    output = output.replace("\n"," ")
    return output

def parse_tags(text):
    output = text.replace(">","")
    output = output.replace("<", ",")
    output = output[1:]
    return output



#parse_xml_user_location(file_read="/home/trideep/Downloads/Users.xml",file_write="/home/trideep/python_workspace/LanguageAnalysis/data/user_location.csv")