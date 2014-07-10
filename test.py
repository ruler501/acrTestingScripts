import gdb

def getchar(n):
	return int(gdb.execute("p (char)p.buf[p.len+"+str(n)+"]", False, True).split()[2])

def getint():
	a = getchar(0)
	if a == -128:
		return getchar(1) | (getchar(2)<<8)
	elif a == -127:
		return getchar(1) | (getchar(2)<<8) | (getchar(3)<<16) | (getchar(4)<<24)
	else:
		return a
		
class TypeChecker(gdb.Breakpoint):
	def stop (self):
		if getint() >= 105:
			gdb.write(gdb.execute("p p.buf"))
			return True
		return False

TypeChecker("server.cpp:2860")