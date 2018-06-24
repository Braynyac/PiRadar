import RPi.GPIO as GPIO
from PiRadar.radarPygame import Radar
import time

radar = Radar()

SERVO = 3
TRIG = 23
ECHO = 24
# SERVO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

pwm_servo = GPIO.PWM(SERVO, 50)
pwm_servo.start(0)


def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm_servo.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(3, False)
    pwm_servo.ChangeDutyCycle(0)
    radar.angle = angle

# DISTANCE SENSOR


def get_distance():
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
      t0 = time.time()
    while GPIO.input(ECHO) == 1:
      t1 = time.time()
    duration = t0 - t1
    distance = 17150 * duration
    return distance


if __name__ == '__main__':
    while True:
        for i in range(0, 180):
            SetAngle(i)
            radar.update(radar.angle, get_distance())
            radar.loop()

#
