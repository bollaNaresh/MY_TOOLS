import os
import pickle
os.environ['BUILD_DIR'] = 'C:\\FINAL_GUI_BUILD\\'
os.environ['APPLICATION'] = 'COMBINED'
sys.path.append(os.environ['BUILD_DIR']+r'fmsa-ver\environment\utils\lua')
sys.path.append(os.environ['BUILD_DIR']+r'fmsa-ver\environment\utils\python')
sys.path.append(os.environ['BUILD_DIR']+r'fmsa-ver\environment\utils\vcl')
sys.path.append(os.environ['BUILD_DIR']+r'fmsa-ver\environment\utils\python\layers')
os.environ['HOST_TARGET'] = 'HOST'
os.environ['DEVELOPMENT'] = 'FALSE'
os.environ['INSTRUMENTED'] = 'FALSE'
os.environ['FMSA_TYPE'] = 'FMSA-3'
os.environ['PROGRAM'] = 'EDS'
os.environ['RFS'] = 'FALSE'

f = open(os.environ['BUILD_DIR']+r"fmsa-ver\VISTA_BATCH_RUN\scripFilesList.txt")
tp_list =  f.readlines()
f.close()
tp_list = map(lambda x:x.replace('\n',''),tp_list)
tpstatusfiel  = os.environ['BUILD_DIR']+r"fmsa-ver\VISTA_BATCH_RUN\tpstatusfile.pickle"
execute_tp_list = {}
if not os.path.exists(tpstatusfiel):
    for scrpt in tp_list:
        execute_tp_list[scrpt] = "NotRun" 
    handle = open(tpstatusfiel, 'wb',)         
    pickle.dump( execute_tp_list, handle,protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()
else:
    handle = open( tpstatusfiel, "rb" )
    if len(pickle.load(handle ))==0:
        for scrpt in tp_list:
            execute_tp_list[scrpt] = "NotRun" 
        handle = open(tpstatusfiel, 'wb',)         
        pickle.dump( execute_tp_list, handle,protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

handle = open( tpstatusfiel, "rb" )  
exc_tps = pickle.load(handle )
handle.close()

for t in tp_list:
    if exc_tps.get(t) == None:
        exc_tps[t] = "NotRun"
print exc_tps

Not_Run_Scripts = filter(lambda x:"NotRun"==x[1],exc_tps.items())
tp_crashes = ""
if len(Not_Run_Scripts)>0:
    tp = Not_Run_Scripts[0][0]
    fs  = open(os.environ['BUILD_DIR']+r"fmsa-ver\VISTA_BATCH_RUN\scriptRunningStatus.txt",'w')
    fs.write('0')
    fs.close()
    try:
        execfile(os.environ['BUILD_DIR']+"fmsa-ver\VISTA_BATCH_RUN\TP_LIST\%s"%(tp))
    except:
        tp_crashes = "Exception occuured.. Please check the LOG FILE and Script File"
    exc_tps[tp] = "Executed"
    handle = open(tpstatusfiel, "wb" )
    pickle.dump( exc_tps, handle )
    handle.close()
    fs1  = open(os.environ['BUILD_DIR']+r"fmsa-ver\VISTA_BATCH_RUN\scriptRunningStatus.txt",'w')
    fs1.write('1')
    fs1.close()
    fr  = open(os.environ['BUILD_DIR']+r"fmsa-ver\VISTA_BATCH_RUN\BATCH_TP_RESULTS.txt",'a')
    fr.write(tp)
    if tp_crashes =="":
        reslt = str(logger.lastResults())
    else:
        reslt = tp_crashes
    fr.write(" ==> "+ reslt)
    fr.write("\n")
    fr.close()
    if os.path.exists(os.environ['BUILD_DIR']+r"fmsa-ver\TESTINSS.DAT"):
        os.rename(os.environ['BUILD_DIR']+r"fmsa-ver\TESTINSS.DAT",os.environ['BUILD_DIR']+r"fmsa-ver\TESTINSS_%s.DAT"%(tp.split('.py')[0]))
    
