# -*- coding: utf-8 -*- #

# TITLE: inspect_test_procedure.py

# AUTHOR: Naresh Bolla

import os
from inspect_test_procedure import * 
import sys


#Define the local paths to use.
#We find the directory this file exists in, and then set the os CWD to that directory
#This makes it so all the checkouts/file creations occur in the folder this script file exists in
#rootDir = r"%s"%os.getcwd()
rootDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(r'%s'rootDir)
svncheckouts = r"%s\checkouts"%rootDir

files = []
updated_tp =[]
        
#create the folder if not exist
script_path = [svncheckouts + "\current", svncheckouts + "\old"]
for file_ in script_path:
    if not os.path.exists(file_):
        os.makedirs(file_)
    else:
        print "folder already present. We need to perform the svn cleanup and svn update"
        #call the batch file to clean up the svn file
        #print "called the batch file for clean up the svn files"
        os.system('Cleanup_Old_Comparison_Checkout.bat')
        print "clean done"
    #end if
#end for

#Define the paths of the output files
output_path = [r'%s'%rootDir + "\output_test.txt", r'%s'%rootDir + "\output_file.txt"]
for path in output_path:
    if os.path.exists(path):
            os.remove(path)
    #end if
#end for

###See if revision file exists, if it does not, set 
os.system('First_Time_Revision_Check.bat')
###Process the Revision file
with open('revision','r') as fd:
    txt = fd.readlines()
#end with

#Remove any possible new lines from the file
timestamp = txt[0].replace('\n','')
#Provide confirmation of timestamp
print "Timestamp is %s"%timestamp

#Commands to checkout the specific version being checked
svnc_cmd_Older = "svn co -r "+timestamp+" "+svn_url 
svnc_cmd_head = "svn co -r HEAD "+svn_url 

#clean up command
os.chdir(r'%s'%svncheckouts + "\old")
os.system(svnc_cmd_Older)
os.chdir(r'%s'%svncheckouts + "\current")
os.system(svnc_cmd_head)
os.chdir(r'%s'%rootDir)

#add all the directory of rootDir into python namespace
for Dir,subdir,filelist in os.walk(rootDir):
    files.append(filelist)
    sys.path.append(Dir)
#end for setting the path

#make sure that svn_diff_report.txt (try.txt) file is not present as every time we need new file
if os.path.exists(r'%s'%rootDir+"/svn_diff_report.txt"):
    os.remove(r'%s'%rootDir+"/svn_diff_report.txt")
    #print "Deleted try.txt"
else:
    delete_string = r'%s'%rootDir + "/svn_diff_report.txt"
    print "Cound not find svn_diff_report.txt in %s"%delete_string
#end if

summarize_command = 'svn diff -r %s:HEAD --summarize "http:MPVI SVN PATH/">>svn_diff_report.txt'%timestamp
print "Summarize Command: %s"%summarize_command
os.system(summarize_command)

#Open and read the diff report from the SVN command
with open('svn_diff_report.txt') as fd:
    txt = fd.readlines()
#end with

#this code will give the file which are modified from previous version
file_operation = {} #create a dictionary
for file_tp in txt:
    file_mod = file_tp[0].split(''.ljust(7))[0]
    file_name = file_tp.split(''.ljust(7))[1].split('test_mpvi')[-1].replace('\n','')
    file_operation[file_name ] = file_mod
#end for    

#set the directory to python namespace
sys.path.append(svncheckouts+"\old\test_mpvi")
sys.path.append(svncheckouts+"\current\test_mpvi")

new_added_file = []
final_updated_tp_list = []
for script,mod in file_operation.items():

    if mod=="M" or mod =="U":
        old_procedures = Get_TP_Content(r"%s\old\test_mpvi/"%svncheckouts + script)
        new_procedures = Get_TP_Content(r"%s\current\test_mpvi/"%svncheckouts + script)
        final_updated_tp_list.extend(updated_and_new_tps(old_procedures, new_procedures))
        #print final_updated_tp_list
    else:
        new_added_file.append(script)
#end for

#write the output into text file
with open(output_path[0],'w') as fd:
    for data in range(len(final_updated_tp_list)):
        fd.write(final_updated_tp_list[data]+"\n")
    #end for
#end with
#end with
with open(output_path[1],'w') as fd:
    for data in range(len(new_added_file)):
        fd.write(new_added_file[data]+"\n")
    #end for
#end with


#Update revision
os.system("Update_Revision_File.bat")

