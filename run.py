'''
Created on Sep 20, 2016

@author: trideep
'''

import stackexchange as se
import filepath as fp

def main():
    #tags = ['javascript','java','mysql','python',
    #        'c++','c','sql','swift','matlab','html']
    tags = ['java']
    se.fetch_questions(page=1, tags=tags, filename=fp.question_file)
    

if __name__ == '__main__':
    main()
    pass