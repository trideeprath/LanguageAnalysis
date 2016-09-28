'''
Created on Sep 20, 2016

@author: trideep
'''

from stackapi import StackAPI
import json
import csv
import io



def fetch_questions(tags=None,filename=None,page=1,write_mode="w"):

    """
    writes question data to csv file 
    """
    SITE = StackAPI('stackoverflow')
    if tags is None:
        tags = ['java']
    write_list = []
    for tag in tags:
        print("+++++++++++++++++ " + tag + " +++++++++++++++++")
        questions = SITE.fetch('questions',tagged=tag,page=page)
        #json_obj  = json.dumps(questions,indent=4)
        json_obj = json.loads(json.dumps(questions))
        question_list = json_obj['items']
        for ques in question_list:
            ques_obj = json.loads(json.dumps(ques))
            tags_obj = ques_obj['tags']
            tags_str = "|".join(tags_obj)
            owner_obj = json.loads(json.dumps(ques_obj['owner']))
            user_id = owner_obj['user_id'] if "user_id" in owner_obj.keys() else u""
            reputation = owner_obj['reputation'] if "reputation" in owner_obj.keys() else u""
            user_type = owner_obj['user_type'] if "user_type" in owner_obj.keys() else u""
            display_name = owner_obj['display_name'] if "display_name" in owner_obj.keys() else u""
            #display_name = display_name.encode('ascii','ignore')
            temp_tuple = (ques_obj['question_id'], tag,ques_obj['is_answered'], tags_str, ques_obj['title'], ques_obj['answer_count'], 
                          ques_obj['creation_date'],ques_obj['score'],ques_obj['link'],
                          ques_obj['view_count'], user_id, reputation, user_type, display_name)
            #print temp_tuple
            write_list.append(temp_tuple) 
    
  
    
    with io.open(filename, write_mode) as file:
        writer = csv.writer(file)
        writer.writerow(('question_id','language','is_answered','tags','title','answer_count',
                          'creation_date','score','link',
                          'view_count','user_id','reputation','user_type','display_name'))
        for row in write_list:
            try:
                writer.writerow(row)
            except Exception as e:
                pass
        
    print("rows written to csv file "+ filename + " " + str(len(write_list)))
            
    


#is_answered, title , tags , answer_count, creation_date, score, link, bounty_amount, view_count, question_id