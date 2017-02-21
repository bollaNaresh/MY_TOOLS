import re
import csv
import os
import Tkinter, tkFileDialog

def Parse_FunProc_Args(data,fun_proc):
   
   all_func_with_param = re.findall(r'%s\s\w+\s?\n?\s{1,100}?\(.*?\)'%(fun_proc), data, re.DOTALL)
         
   patrn1 = r'%s\s\w+\s?\(.*?\)\n?\s{1,100}return\s\w+\.?\w+?\.?\w+?\;'%(fun_proc)
   patrn2 = r'%s\s\w+\sis\snew'%(fun_proc)
   
   exclude_funct_with_param = (re.findall(patrn1, data, re.DOTALL))+(re.findall(patrn2, data, re.DOTALL))

   all_funct = re.sub('\n?\t?',''," ".join(all_func_with_param))

   exclude_funct = re.sub('\n?\t?',''," ".join(exclude_funct_with_param))
   
   all_func_list  =  filter(None,"".join(re.findall(r'%s\s\w+'%fun_proc ,all_funct)).replace(fun_proc, '').split(" "))
   exclu_func_list  =  filter(None,"".join(re.findall(r'%s\s\w+'%fun_proc ,exclude_funct)).replace(fun_proc, '').split(" "))
   

   final_function = sorted([funct for funct in all_func_list if funct not in exclu_func_list]) 
   all_func_with_param = "Naresh ".join(all_func_with_param)
   
   parse_func_arg = (re.sub('\n?\t?','',all_func_with_param).replace(fun_proc+' ', '')).split("Naresh")
   
   final_parse_func_arg = []
   for fn in set(final_function):
      for fn_ar in parse_func_arg:
         if fn == re.sub(r'^\s','',re.search(r'\s?\w+',fn_ar).group()):
            final_parse_func_arg.append(re.sub(r'^\s','',fn_ar))

   return final_function ,final_parse_func_arg
#End of Parse_FunProc_Args

def names():
   
   if not os.path.exists(r"C:\rw_apps\ADA_CSV_FILES"):
    os.makedirs(r"C:\rw_apps\ADA_CSV_FILES")
   
   Valid_Ada_files = []
   root = Tkinter.Tk()
   
   ada_folder = tkFileDialog.askdirectory(parent=root,initialdir=r"C:\rw_apps\ADA_CSV_FILES\TEST",title='Please select a directory');root.destroy()
    
   for root, dirs, files in os.walk(ada_folder):
      for f in files:
         fullpath = os.path.join(root, f)
         if f.endswith(".2.ada"):
             Valid_Ada_files.append( fullpath)
   outputfile = r"C:\rw_apps\ADA_CSV_FILES\Final_Report.csv"
   
   fw= open(outputfile, 'wb')
   writer = csv.writer(fw)
   writer.writerow(["Source File Names","Name Of The Function-Procedures", "Function-Procedure Parameters","Parameters Not Used Inside Function-Procedure"])
   file_num=0
   for ada_file in Valid_Ada_files:
      file_num+=1
      with open(ada_file) as f:
         data = f.readlines()
      data = "".join([ln for ln in data if not re.search(r'\s?\--\s?',ln[:12])])
      print "File:  " + ada_file.split("\\")[-1]
      
       #outputfile = r"C:\rw_apps\ADA_CSV_FILES/"+ada_file.split("\\")[-1] +".csv"
       #fw= open(outputfile, 'wb'); writer = csv.writer(fw)
      
       
        

      for fun_proc in ["function","procedure"
                       ]:
         
         final_function ,final_parse_func_arg =  Parse_FunProc_Args(data,fun_proc)
         

         if len(final_function) > 0:
            try:           
               for each_fun_proc  in final_parse_func_arg:
                  
                  fun  = re.search('\w+',each_fun_proc).group()
                  
                  result = []
                  code = {}
                  function_with_params = {}
                  
                  if (data.find(fun_proc+" %s "%fun)==-1):
                     func_index  = data.find(fun_proc+" %s"%fun)
                  else:
                     func_index  = data.find(fun_proc+" %s "%fun)
                  
                  code[fun] = data[func_index:data.find("end %s;"%fun)]
                  
                  data  = data.replace(data[func_index:data.find("end %s;"%fun)+len(fun)+4], "")
                  
                  code[fun] =  code[fun][code[fun].find(" is\n"):]
               
                  if fun in each_fun_proc:
                     func_param = re.sub(r"--\s{0,4}\w+\.*","",each_fun_proc.replace(fun,''))
                     
                     func_param = func_param.replace('  ','').replace("(",'').replace(")",'').split(";")
                     function_with_params[fun] = func_param
   #                
   #                print ""
   #                print "fun======: "+fun
   #                print code[fun]
   #                print "=======function protitype==============="
   #                print each_fun_proc
   #                print ""
                  
                  params = filter(None, "".join(re.findall('\w+\s?\:\s',",".join(function_with_params[fun]))).replace(": ", " ").split(" "))
                  argus_inside_proc_fun = filter(None,re.split(r'[^\w]',code[fun]))
                  
                  arg_used = [arg for arg in params if arg not in argus_inside_proc_fun ]
               
                  result.append(ada_file.split("\\")[1])
                  result.append(fun)
                  result.append(" , ".join(params))
                  result.append(" , ".join(arg_used))
                  writer.writerow(result)
            except:
               print "**************************"
               print "***** %s has some format issue in %s"%(fun,ada_file.split("\\")[-1] )
               print " feel free to ask Naresh\n"      
         else:
               writer.writerow(["There are "+fun_proc+"s with zero parameters in this file"])
   fw.close()
   raw_input("\n The Number of Files: %d \n Check the Results in %s  \n \n  Press Any Key.............."%(file_num,outputfile))
  
if __name__ == "__main__":
   print "================ Staretd analysis =================="
   print "===================================================="
   names()
   print "===================================================="
   print "===================================================="    
