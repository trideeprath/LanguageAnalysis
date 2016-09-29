'''
Created on Sep 20, 2016

@author: trideep
'''

import stackexchange as se
import filepath as fp
from data_processing.keyphrases import Keyphrase

def main(tags = ['java','C'], fetch_questions=False,fetch_keyphrases=False, outfile="data/question_java+C.csv"):
    #tags = ['javascript','java','mysql','python',
    #        'c++','c','sql','swift','matlab','html']
    language_keyphrase_map= {}

    ## Doing it for Python, SQL, c++
    if fetch_questions:
        se.fetch_questions(page=1, tags=tags, filename=outfile,write_mode='w')

    if fetch_keyphrases:
        keyphrase_gen = Keyphrase(integrate_data=True)
        keyphrase_gen.create_keyphrases()
        language_keyphrase_map = keyphrase_gen.get_keyphrases(topn=30)
        keyphrase_gen.save_keyphrases(language_keyphrase_map,fp.question_keyphrases)


if __name__ == '__main__':
    main(fetch_questions= True,fetch_keyphrases=False)
    pass