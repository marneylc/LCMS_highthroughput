import threading
import os
import sys

def main():
	path = sys.argv[1]
	maxthreads = sys.argv[2]
	files = listdir(path)
	thread_handle(files,maxthreads,hrms.R)

# initiates as many threads as maxthreads for the 
# methods defined in R_threadClass
def thread_handle(files,maxthreads,R_threadClass):
	anchor = range(0,len(files),maxthreads)
	for i in anchor:
		file_lim = files[anchor[i:i+maxthreads]]
		
		for R_threadClass in files_lim:
			R_threadClass.start()	
		
		if files_lim[-1].isAlive(): # check to make sure -1 indexes the final entry in files_lim
			time.sleep(1) # need to make sure this actually pausese the queue before going on to the rest of the threads


class hrms.R(threading.thread)
	def __init__(self,filename):
		self.filename = filename
		threading.thread.__init__(self)

	def run(self):
		print ("Processing file: " + self.filename)
		os.system("R CMD BATCH hrms.R " + self.filename)
		print ("File: " self.filename + " is all done!"

main()