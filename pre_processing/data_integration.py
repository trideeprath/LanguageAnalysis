
import csv
import pandas as pd


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




