
import csv
import pandas as pd
import xml.etree.ElementTree
import re
from nltk.tokenize import sent_tokenize


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

#parse_xml_user_location(file_read="/home/trideep/Downloads/Users.xml",file_write="/home/trideep/python_workspace/LanguageAnalysis/data/user_location.csv")