'''
Ensures JOB variable standard

Notes:
hou.putenv DOESNT WORK
http://forums.odforce.net/topic/27174-job-variables-problem-with-setenv/
use hou.hscript(setenv VAR = VALUE) instead

'''


import os
import hou

# check 456 script run with hython in command line tools
#print 'IN 456 SCRIPT'

hou.allowEnvironmentToOverwriteVariable("JOB", True)

JOB = hou.getenv("JOB")
HIP = hou.getenv("HIP")
PROJ = hou.getenv("PROJ")
DEFAULT = "C:/Users/Luis"


def normpath(path):
	path = os.path.normpath(path)
	path = path.replace("\\", "/")
	return path

def isCorrect(variable):	
	if os.path.isdir(JOB) == False:
		return False
	if JOB == "C:/Users/Luis":
		print 'JOB is default'
		return False
	find = ["/","\\"]
	if any(item in variable[-1] for item in find):
		print 'JOB ends in slash'
		return False
	if JOB != normpath(JOB):
		print 'JOB is not equal to normpath(JOB)'
		return False


#print(JOB, HIP, PROJ)

if PROJ in HIP:
	#print 'yes proj in hip'
	if isCorrect(JOB) == False:	
		if HIP != DEFAULT:		
			#folders = HIP.split("/")
			find = "/houdini"
			idx = HIP.rfind(find)
			if idx > -1:			
				JOB = HIP[0:idx+len(find)]
				JOB = normpath(JOB)		
			else:
				# go up one level			
				JOB = os.path.dirname(HIP)
				JOB = normpath(JOB)
				print JOB
				#hou.putenv("JOB", JOB)

			print 'JOB variable modified'
			print 'from %s -> %s' % [hou.getenv("JOB"), JOB]
			hou.hscript("setenv JOB = %s" % JOB)

	


