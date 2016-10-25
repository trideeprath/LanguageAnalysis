'''
Created on Sep 20, 2016

@author: trideep
'''

import LanguageAnalysis.stackexchange as se
import LanguageAnalysis.filepath as fp
from LanguageAnalysis.data_processing.keyphrases import Keyphrase
from LanguageAnalysis.data_processing.language_sim import LanguageSimilarity

def main(fetch_questions=False,fetch_keyphrases=False,language_similarity=False):
    #tags = ['javascript','java','mysql','python',
    #        'c++','c','sql','swift','matlab','html']
    language_keyphrase_map= {}
    if fetch_questions:
        tags = ['java','javascript','swift']
        se.fetch_questions(page=1, tags=tags, filename=fp.question_file,write_mode='w')

    if fetch_keyphrases:
        keyphrase_gen = Keyphrase(integrate_data=True)
        keyphrase_gen.create_keyphrases()
        language_keyphrase_map = keyphrase_gen.get_keyphrases(topn=30)
        keyphrase_gen.save_keyphrases(language_keyphrase_map,fp.question_keyphrases)

    if language_similarity:
        lang_sim = LanguageSimilarity()





if __name__ == '__main__':
    main(fetch_questions= False,fetch_keyphrases=False, language_similarity=True)
    pass