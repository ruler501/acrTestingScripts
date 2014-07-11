import gdb
import psutil

currentbufoffset = 0

def retint(var):
	return gdb.execute("p (int)"+var, False, True).split()[2]

def getchar(p='p'):
	global currentbufoffset
	currentbufoffset += 1
	return retint(p+".buf["+p+".len+"+str(currentbufoffset-1)+"]")

def getint(p):
	global currentbufoffset
	a = getchar(p='p')
	if a == -128:
		currentbufoffset += 2
		return getchar(p) | (getchar(p)<<8)
	elif a == -127:
		currentbufoffset += 4
		return getchar(p) | (getchar(p)<<8) | (getchar(p)<<16) | (getchar(p)<<24)
	else:
		return a
		
class TypeChecker(gdb.Breakpoint):
	def stop (self):
		global currentbufoffset
		currentbufoffset = 0
		if getint('p') >= 105:
			gdb.write(gdb.execute("p p.buf"))
			return True
		return False

class RAMChecker(gdb.Breakpoint):
	def stop (self):
		return psutil.Process(gdb.inferiors().pid).memory_info()[0] > 1073741824

TypeChecker("server.cpp:2860", internal=True)
RAMChecker("main.cpp:1260", internal=True)