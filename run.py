'''
Created on Sep 20, 2016

@author: trideep
'''

import LanguageAnalysis.stackexchange as se
import LanguageAnalysis.filepath as fp
from LanguageAnalysis.data_processing.keyphrases import Keyphrase

def main(fetch_questions=False,fetch_keyphrases=False):
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





if __name__ == '__main__':
    main(fetch_questions= False,fetch_keyphrases=True)
    pass