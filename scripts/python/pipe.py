


def ensureDirectory(path):
	'''
	ensures path is a valid directory for use in pipe tools
	'''
	find = ["/","\\"]
	if any(item in path[-1] for item in find):
		return path[:-1]
	else:
		return path