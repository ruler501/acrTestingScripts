import gdb

currentbufoffset = 0

def getchar(p='p'):
	global currentbufoffset
	currentbufoffset += 1
	return int(gdb.execute("p (char)"+p+".buf["+p+".len+"+str(currentbufoffset-1)+"]", False, True).split()[2])

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

TypeChecker("server.cpp:2860")