import sys
import threading
import psutil

if sys.platform.startswith('win32'):
	from winpexpect import EOF, TIMEOUT
	from winpexpect import winspawn as spawn
else:
	from pexpect import EOF, TIMEOUT
	from pexpect import spawn

class PlatformError(Exception):
	def __init__(self, platform):
		self.platform = platform
	def __str__(self):
		return self.platform+" is not currently supported"

def ACRcommand(client=True):
	if sys.platform.startswith('linux'):
		if client:
			return "bin_unix/native_client --home=data --mod=acr --init"
		else:
			return "bin_unix/native_server"
	elif sys.platform.startswith('win32'):
		if client:
			return "bin_win32/ac_client.exe --home=data --mod=acr --init"
		else:
			return "bin_win32/ac_server.exe"
	else:
		raise PlatformError(sys.platform)
		
def checkRAM():
	if childPID < 1:
		return False
	return psutil.Process(childPID).memory_info()[0] > 1073741824

shouldExit = False
childPID = -1

def main(argv=None):
	global shouldExit
	global childPID
	if argv == None:
		argv = sys.argv
	for i in xrange(len(argv)):
		if argv[i] == "--log":
			log = open(argv[i+1],'w')
			break
	else:
		log = open('debug.log','w')
	print "Starting child"
	child = spawn("gdb -quiet -fullname -args "+ACRcommand(), logfile=log)
	child.expect_exact('(gdb)')
	print "Loading Scripts"
	child.sendline('source client.py')
	child.expect_exact('(gdb)')
	print "Running child"
	child.sendline('r')
	child.expect(r"New Thread \d+\.")
	try:
		childPID = int(child.after.split('.')[0].split()[-1])
	except ValueError:
		print "Couldn't find the child's PID"
	if "--ucontrol" in argv:
		child.interact()
	else:
		try:
			while child.isalive():
				i = child.expect_exact(['(gdb)', 'exited with code', TIMEOUT], timeout=1)
				if i == 0:
					log.write("ERROR ABOVE\n")
					print "continuing"
					child.sendline('c')
				elif i == 1:
					log.write("Exited\n")
					log.close()
					return 0
				elif i == 2:
					if checkRAM():
						log.write("Memory Overflow")
						child.kill(5)
						#child.terminate()
					if shouldExit:
						print "Exitting"
						child.terminate()
		except EOF:
			pass
	log.close()
	return 0

class debugRun(threading.Thread):
	def stop(self):
		global shouldExit
		shouldExit = True
	
if __name__=="__main__":
	main()


	
	