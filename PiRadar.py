import RPi.GPIO as GPIO
from radarPygame import Radar
import time
GPIO.setwarnings(False)
radar = Radar()

SERVO = 3
TRIG = 11
ECHO = 13

# SERVO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

pwm_servo = GPIO.PWM(SERVO, 50)
pwm_servo.start(0)


def SetAngle(angle):
    duty = translate(angle, 0, 180, 2,10) 
    #GPIO.output(3, True)
    pwm_servo.ChangeDutyCycle(duty)
    #time.sleep(5)
    #GPIO.output(3, False)
    #pwm_servo.ChangeDutyCycle(0)
    radar.angle = angle

# DISTANCE SENSOR


def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(.001)
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        t0 = time.time()
    while GPIO.input(ECHO) == 1:
        t1 = time.time()
    distance = 17150*(t1-t0)
    return distance

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


if __name__ == '__main__':
    while True:
        for i in range(0, 180):
            t0 = time.time()
            SetAngle(i)
            distance = get_distance()
            print("Angle:", i, "Distance:", distance)
            radar.update(radar.angle, distance)
            radar.loop()
            print("degrees/second: ", (time.time()-t0)**-1)
        for i in range(0, 180):
            t0 = time.time()
            SetAngle(180-i)
            distance = get_distance()
            print("Angle:", i, "Distance:", distance)
            radar.update(radar.angle, distance)
            radar.loop()
            print("degrees/second: ", (time.time()-t0)**-1)


