"""Run scripted tests on ACR

Options:
None currently

Bugs:
Mouse movement is very erratic(not sure of a good way to resolve this)
"""
import autopy
import sys
import time
import threading
import autorun

sX, sY = autopy.screen.get_size()
		   
def sendScript(command):
	send = "/"
	for i in command:
		send += i+" "
	autopy.key.type_string(send[:-1]+'\n', 120)

def moveMouse(position):
	x, y = autopy.mouse.get_pos()
	if x + position[0] > sX:
		x = sX - position[0] - 1
	elif x + position[0] < 0:
		x = -1*position[0] + 2
	if y + position[1] > sY:
		y = sY - position[1] - 1
	elif y + position[1] < 0:
		y = -1*position[1] + 2
	print autopy.mouse.get_pos()
	if len(position) == 2:
		autopy.mouse.move(x+position[0], y+position[1])
	else:
		autopy.mouse.smooth_move(x+position[0], y+position[1])

def moveOverTime(params):
	x, y = (params[0],params[1])
	tx, ty = (x/(30.0*params[2]), y/(30.0*params[2]))
	for i in xrange(int(50*params[2])):
		ox, oy = autopy.mouse.get_pos()
		ax, ay = (tx, ty)
		if ax + ox > sX:
			ax = sX - ox - 1
		elif ax + ox < 0:
			ax = -1*ox + 2
		if ay + oy > sY:
			ay = sY - oy - 1
		elif ay + oy < 0:
			ay = -1*oy + 2
		ox += ax
		oy += ay
		autopy.mouse.move(int(ox), int(oy))
		time.sleep(1.0/30.0)
	
def mousePress(key):
	if key[0] == "r":
		kp = autopy.mouse.RIGHT_BUTTON
	elif key[0] == "m":
		kp = autopy.mouse.CENTER_BUTTON
	else:
		kp = autopy.mouse.LEFT_BUTTON
	if len(key) == 1:
		autopy.mouse.click(kp)
	else:
		autopy.mouse.toggle(key[1], kp)
	
def sendKeys(keys):
	for key in keys:
		if len(key) == 1:
			autopy.key.type_string(key[0], 0)
		elif len(key) == 2:
			autopy.key.tap(key[0], key[1])
		elif len(key) == 3:
			autopy.key.toggle(key[0], key[1], key[2])

tests = [
		]
commands = { "m"	: moveMouse,
			 "mt"	: moveOverTime,
			 "mp"	: mousePress,
			 "s"	: time.sleep,
			 "ss"	: sendScript,
			 "k"	: sendKeys
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