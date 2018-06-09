
import os
import hou

# check 456 script run with hython in command line tools
print 'IN 456 SCRIPT'

def isCorrect(variable):
	find = ["/","\\"]
	return any(item in variable[-1] for item in find)

# clean JOB variable
job = hou.getenv("JOB")

if not isCorrect(job):
	job = os.path.dirname(job)
	hou.putenv("JOB", job)
