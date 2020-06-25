import pandas as pd
import datetime as dt
from dateutil.relativedelta import *
import threading
import os
import time

def GenerateFile(filename):
	xls = pd.ExcelFile(filename)

	dfSheetA = xls.parse("Sheet A")
	dfSheetB = xls.parse("Sheet B")

	dt_now = dt.datetime.now()
	last_month = dt_now + relativedelta(months=-1)

	df_merged = pd.merge(dfSheetA, dfSheetB, how="inner", on=["Begin Date", "End Date"])

	dfResult=\
		df_merged.loc\
		[
			(df_merged["Begin Date"].dt.strftime("%m") == last_month.strftime("%m")) 
			& 
			(df_merged["End Date"].dt.strftime("%m") == last_month.strftime("%m"))
		]

	outputFilename = "Last Month.xls"
	dfResult.to_excel(outputFilename, "Sheet Result")
	print("File {0} recently generated.".format(outputFilename))

def RunProcess(filename):
	(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
	old_mtime= str(dt.datetime.fromtimestamp(mtime))
		
	while(True):
		time.sleep(5.5)
			
		(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
		cur_mtime = str(dt.datetime.fromtimestamp(mtime))
		
		if old_mtime == cur_mtime:
			pass #same excel file -no changes
		else:
			old_mtime = cur_mtime
			GenerateFile(filename)
				
if __name__ == "__main__":
	thread = threading.Thread(target=RunProcess, args=("History.xls",))
	thread.start()	
