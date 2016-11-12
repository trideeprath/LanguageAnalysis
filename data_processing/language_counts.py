
from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
from pandas import DataFrame as df, Series




def question_count(create_data= False):
    if create_data is True:
        di.parse_xml_questions(file_read=fp.posts_file_xml,file_write=fp.question_data)
    save_counts(file_read = fp.question_data, file_write= fp.language_counts)

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
    question_count()
    pass
