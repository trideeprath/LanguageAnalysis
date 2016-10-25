
import datetime
from pandas import DataFrame as df
from sklearn.feature_extraction.text import TfidfVectorizer
from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
import pickle
from pprint import pprint
import csv
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence



class LanguageSimilarity():

    def __init__(self,integrate_data=False):
        if integrate_data is True:
            di.parse_xml_language_similarity(file_read=fp.posts_file_xml,file_write=fp.posts_sentences_file)


    def start_training(self):
        in_sentence = LineSentence(fp.posts_sentences_file)
        print("Starting word2vec Training")
        word2vec_model = Word2Vec(in_sentence, size=200, window=5, workers=4)
        word2vec_model.save_word2vec_format(fp.w2vfilepath)
        print("Word2vec training complete")


    def create_lang_similarty_data(self):
        model = Word2Vec.load_word2vec_format(fp.w2vfilepath)
        lang_list = ['java', 'python', 'matlab', 'html', 'c++', 'c', 'mysql', 'javascript', 'sql']
        '''
        for lang_o,lang_i in zip(lang_list,lang_list):
            for lan_i in lang_list:
                sim = model.similarity(lang_o,lan_i)
                print(lang_o,lan_i,sim)
        '''

        with open(fp.language_sim, 'w') as mycsvfile:
            temp_list = lang_list[:]
            temp_list.insert(0," ")
            print(temp_list)
            datawriter = csv.writer(mycsvfile)
            datawriter.writerow(temp_list)
            for lang_o in lang_list:
                lang_sim = ["{0:.2f}".format(abs(model.similarity(lang_o,lang))) for lang in lang_list]
                lang_sim.insert(0,lang_o)
                print(lang_sim)
                datawriter.writerow(lang_sim)
