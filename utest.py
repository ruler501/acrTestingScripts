import autopy
import sys
import time
import threading
import autorun
		   
def sendScript(command):
	send = command
	if type(command) == type([]):
		send = command[0]
		for i in command[1:]:
			send += " "+i
	autopy.key.tap('/')
	autopy.key.type_string(send, 60)

def sendKeys(keys):
	for key in keys:
		if len(key) == 1:
			autopy.key.type_string(key[0], 60)
		elif len(key) == 2:
			autopy.key.tap(key[0], key[1])
		elif len(key) == 3:
			autopy.key.toggle(key[0], key[1], key[2])

tests = [("k",("/monitors 3"))]
commands = { "sm"	: autopy.mouse.smooth_move,
			 "m"	: autopy.mouse.move,
			 "s"	: time.sleep,
			 "k"	: sendKeys,
		   }			

def main():
	child = autorun.debugRun(target = autorun.main)
	child.start()
	time.sleep(10)
	#while child.is_alive():
	for action in tests:
		commands[action[0]](action[1])
	child.stop()
	child.join()

if __name__=="__main__":
	main()