# -*- coding: utf-8 -*- #

# TITLE: inspect_test_procedure.py

# AUTHOR: Naresh Bolla
import re


''' this function will give the list of Test Procedure '''
def Get_TP_Content(file_name = None):

    with open(file_name) as f:
        text = f.readlines()
    #end with
    
    for index, line in enumerate(text):
        if "MPVI_TEST" in line: #its program specific only.we have to change as per test procedures names in the script file
            break
        #end if
    #end for
    start_id=0
    procedures={} #create dictionary
    for i in text[index:]:
        tc = re.findall('\MPVI_TEST_+\d+',i)
        if tc :
            if tc[0] != start_id:
                procedures[tc[0]] = []
                procedures[tc[0]].append(i)
            else:
                procedures[tc[0]].append(i)
            #end if
            start_id =tc[0]
        else:
            procedures[start_id].append(i)
        #end if
    return procedures
    #end for
#end of Get_TP_Content


''' this function will give the list of Test Procedure '''
def updated_and_new_tps(old_procedures, new_procedures) :    
    final_result = []
    final_result.extend( list(set(new_procedures.keys())-set(old_procedures.keys())))
    for tp in (set(new_procedures.keys())& set(old_procedures.keys())):
        if len(new_procedures[tp]) != len(old_procedures[tp]):
            final_result.append(tp)
        elif(cmp(new_procedures[tp],old_procedures[tp])==1):
            final_result.append(tp)
        #end if
    return final_result
    #end for    
#end of Get_TP_Content
     
#old_procedures = Get_TP_Content(old_file_name)        
#new_procedures = Get_TP_Content(new_file_name)
#tp_run_list = updated_and_new_tps(old_procedures, new_procedures)