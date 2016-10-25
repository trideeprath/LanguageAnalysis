
import datetime
from pandas import DataFrame as df
from sklearn.feature_extraction.text import TfidfVectorizer
from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
import pickle
from pprint import pprint
import csv



class LanguageSimilarity():

    def __init__(self,integrate_data=True):
        di.parse_xml_language_similarity(file_read=fp.posts_file_xml,file_write=None)


