import gdb
import psutil

currentbufoffset = 0

logfile=open("debug.log",'w')

def retint(var):
	return int(gdb.parse_and_eval("(int)"+var))

def getchar(p='p'):
	global currentbufoffset
	p = str(p)
	currentbufoffset += 1
	return int(gdb.parse_and_eval("char*)"+p+"["+str(currentbufoffset-1)+"]"))

def getint(p):
	global currentbufoffset
	p = str(p)
	a = getchar(p)
	if a == -128:
		currentbufoffset += 2
		return getchar(p) | (getchar(p)<<8)
	elif a == -127:
		currentbufoffset += 4
		return getchar(p) | (getchar(p)<<8) | (getchar(p)<<16) | (getchar(p)<<24)
	else:
		return a
		
class TypeChecker(gdb.Breakpoint):
	def stop(self):
		global currentbufoffset
		currentbufoffset = 0
		if retint('type') >= 105:
			gdb.write(str(gdb.execute("p p.buf")), gdb.STDOUT)
			return True
		return False

class RAMChecker(gdb.Breakpoint):
	def stop(self):
		return psutil.Process(gdb.selected_inferior().pid).memory_info()[0] > 1073741824

class BotChecker(gdb.Breakpoint):
	def stop(self):
		if gdb.parse_and_eval("m_pMyEnt->enemy != NULL"):
			return True
		return False

class KDPrinter(gdb.Breakpoint):
	def stop(self):
		logfile.write("killer "+str(gdb.parse_and_eval("act->clientnum"))+'\n')
		for i in xrange(int(gdb.parse_and_eval("NUMGUNS"))):
			k = int(gdb.parse_and_eval("act->weapstats["+str(i)+"].kills"))
			d = int(gdb.parse_and_eval("act->weapstats["+str(i)+"].deaths"))
			if k != 0 or d != 0:
				logfile.write("Weap "+str(i)+" k:"+str(k)+" d:"+str(d)+"\n")
		logfile.write("victim "+str(gdb.parse_and_eval("pl->clientnum"))+'\n')
		for i in xrange(int(gdb.parse_and_eval("NUMGUNS"))):
			k = int(gdb.parse_and_eval("pl->weapstats["+str(i)+"].kills"))
			d = int(gdb.parse_and_eval("pl->weapstats["+str(i)+"].deaths"))
			if k != 0 or d != 0:
				logfile.write("Weap "+str(i)+" k:"+str(k)+" d:"+str(d)+"\n")
		return False

class WeaponSelChecker(gdb.Breakpoint):
	def stop(self):
		weap = int(gdb.parse_and_eval("bestWeapon"))
		logfile.write('client:'+str(gdb.parse_and_eval("m_pMyEnt->clientnum"))+" weap:"+str(weap)+'\n')
		if weap not in [0, 1, 5, 6]:
			gdb.write(str(weap)+',')
		return False
		
TypeChecker("server.cpp:2866", internal=True)
RAMChecker("main.cpp:1260", internal=True)
#BotChecker("bot_ai.cpp:775", internal=True) Fixed issue
#KDPrinter("clientgame.cpp:927", internal=True) Fixed issue
#WeaponSelChecker("ac_bot_ai.cpp:113", internal=True) Fixed issue