import datetime
from pandas import DataFrame as df
from sklearn.feature_extraction.text import TfidfVectorizer
from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
import pickle
from pprint import pprint
import csv




class Keyphrase:

    def __init__(self,integrate_data=True):
        di.integrate_questions(file_read=fp.question_file, file_write=fp.question_file_integrated)
        self.tfidf_gen = tfidf_generator()

    def create_keyphrases(self,save_model=True):
        self.tfidf_gen.create_tfidf_matrix(id_col='language',data_col='question_title',filename=fp.question_file_integrated)
        if save_model == True:
            pickle.dump(self.tfidf_gen,open(fp.tfidf_model,'wb'))

        #keys = self.tfidf_gen.get_keyphrases(key=1,topn=100)
        #pprint(keys)


    def get_keyphrases(self,topn):
        id_index_dict = self.tfidf_gen.id_index_map
        keyphrases_dict = dict(map(lambda doc_id: (doc_id, self.tfidf_gen.get_keyphrases(key=id_index_dict[doc_id], topn=topn)), id_index_dict.keys()))
        return keyphrases_dict

    def save_keyphrases(self,keyphrase_map,write_file=None):
        with open(fp.question_keyphrases,'w') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['language','keyphrase','tfidf'])
            for language in keyphrase_map.keys():
                for tuple in keyphrase_map[language]:
                    print(language,tuple[0],tuple[1])
                    csv_writer.writerow([language,tuple[0],tuple[1]])







class tfidf_generator:

    def __int_(self, tfidf_matrix=None, features=None, id_index_map=None,stop_words=None):
        self.tfidf_matrix = tfidf_matrix
        self.features = features
        self.id_index_map = id_index_map
        self.stop_words = stop_words

    def create_tfidf_matrix(self, ngram_min=2, ngram_max=3, id_col=None, data_col=None, filename=None,
                            save_model=False):
        tf_gen_obj = tfidf_generator()

        print("Creating tfidf matrix")
        start_time = datetime.datetime.now()
        # Converting all reviews into a list of document
        #
        data_pandas = df.from_csv(open(filename,'r'), parse_dates=True)
        data_pandas = data_pandas.reset_index()

        # Copying the dataframe to dictionary
        #
        document_dict = {}
        for id, row in data_pandas.iterrows():
            id_value = row[id_col]
            document_dict[id_value] = row[data_col]

        corpus = []
        index = 0
        document_map = {}
        id_index_map = {}
        for doc_id, doc in document_dict.items():
            corpus.append(doc)
            document_map[index] = id
            id_index_map[doc_id] = index
            index = index + 1



        # Create Tf matrix with ngram for 1,2,3 phrases and stop words as english
        #
        tf = TfidfVectorizer(analyzer='word', ngram_range=(ngram_min, ngram_max),
                             lowercase=True, stop_words='english')

        tfidf_matrix = tf.fit_transform(corpus)
        feature_names = tf.get_feature_names()

        self.tfidf_matrix = tfidf_matrix
        self.features = feature_names
        self.id_index_map = id_index_map


    def get_keyphrases(self, key=None, topn=None):
        tfidf_matrix_dense = self.tfidf_matrix[key].todense()
        tfidf = tfidf_matrix_dense.tolist()[0]
        # creates a list of tuple (feature_id , tfidf_of_feature)
        #
        tfidf_pair = []
        for i in range(0, len(tfidf)):
            if (tfidf[i] > 0):
                pair = ()
                pair = (i, tfidf[i])
                tfidf_pair.append(pair)

        sorted_tfidf = sorted(tfidf_pair, key=lambda t: t[1] * -1)

        final_result = []
        for phrase_id, tfidf in sorted_tfidf:
            tuple = (self.features[phrase_id], tfidf)
            # if len(tuple[0].split(" "))>1:
            final_result.append(tuple)

        if topn is None:
            return final_result

        else:
            return final_result[0:topn]






