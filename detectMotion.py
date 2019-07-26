import RPi.GPIO as GPIO
import time
import datetime
import picamera
import pymysql.cursors

pirSensorPin = 18
dbpasswordpath = "/home/pi/PYSCRIPTS/DetectMotionPi3"


#Set up PIR sensor pin.
GPIO.setmode(GPIO.BCM)
GPIO.setup(pirSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Set up camera
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

#Get Password information from config file.

with open("%s/dbpassword.config" % dbpasswordpath) as pwfile:
	pwfilelist = pwfile.read().splitlines()

hostf = pwfilelist[0]
userf = pwfilelist[1]
passwordf = pwfilelist[2]
databasef = pwfilelist[3]
tablef = pwfilelist[4]

while 1:
	GPIO.wait_for_edge(pirSensorPin, GPIO.RISING)
	#print("Motion detected")
	timeString = time.strftime("%Y%m%d-%H%M%S")
	filename = ('/share/MotionDetectPi3/' + timeString + ".jpg")
	camera.capture(filename)
	sql = "INSERT INTO %s.%s (filename) VALUES ('%s')" % (databasef, tablef, (timeString + ".jpg"))
	connection = pymysql.connect(host=hostf, user=userf, password=passwordf, db=databasef, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
		connection.commit()
	finally:
		connection.close()




		

