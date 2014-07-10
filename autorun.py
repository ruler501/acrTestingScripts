import Queue
import sys
from threading import Thread

if sys.platform.startswith('win32'):
	from winpexpect import EOF
	from winpexpect import winspawn as spawn
else:
	from pexpect import EOF
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


def main():
	log = open('debug.log','w')
	print "Starting child"
	child = spawn("gdb -quiet -fullname -args "+ACRcommand())
	child.expect('(gdb)')
	log.write(child.before + child.after)
	print "Loading Scripts"
	child.sendline('source test.py')
	child.expect('(gdb)')
	log.write(child.before + child.after)
	print "Running child"
	child.sendline('r')
	try:
		while child.isalive():
			i = child.expect(['(gdb)', 'exited with code'], timeout=None)
			if i == 0:
				log.write(child.before + "ERROR ABOVE" + child.after)
				print "continuing"
				child.sendline('c')
			elif i == 1:
				log.write(child.before + child.after + "Exited")
				log.close()
				return 0
	except EOF:
		pass
	log.write(child.before)
	log.close()
	return 0

if __name__=="__main__":
	main()


	
	