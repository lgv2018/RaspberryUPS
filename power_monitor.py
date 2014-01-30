import os
import syslog
import time
import RPi.GPIO as GPIO

SHUTDOWN_GRACE = 2
POWER_PIN = 17
time_power_lost = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_PIN,GPIO.IN)

try:
	POWER_AT_START = GPIO.input(POWER_PIN)
	while POWER_AT_START:
		GPIO.wait_for_edge(POWER_PIN, GPIO.FALLING)
		out = "Power disconnected. Waiting "+str(SHUTDOWN_GRACE)+" minutes until shutting down."
		syslog.syslog(syslog.LOG_ALERT, out)
		os.system("echo \""+out+"\" | wall")
		time_power_lost = time.time()
		while not GPIO.input(POWER_PIN):
			if time.time() > time_power_lost+SHUTDOWN_GRACE*60:
				os.system("shutdown -h now")
				time.sleep(60)
			time.sleep(1)
		time_left = time_power_lost+SHUTDOWN_GRACE*60-time.time()
		out = "Power connected. Aborting countdown with "+str(time_left)+" seconds to spare."
		syslog.syslog(syslog.LOG_ALERT, out)
		os.system("echo \""+out+"\" | wall")
	syslog.syslog("Power detection line isn't connected. Aborting power monitor.")
finally:
        GPIO.cleanup()