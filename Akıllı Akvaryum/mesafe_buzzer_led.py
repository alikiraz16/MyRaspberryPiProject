import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24
red_led_pin_1 = 22
red_led_pin_2 = 27
green_led_pin = 17
buzzer_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(red_led_pin_1, GPIO.OUT)
GPIO.setup(red_led_pin_2, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

GPIO.output(red_led_pin_1, GPIO.LOW)
GPIO.output(red_led_pin_2, GPIO.LOW)
GPIO.output(green_led_pin, GPIO.LOW)
GPIO.output(buzzer_pin, GPIO.LOW)


def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    return distance


try:
    while True:
        dist = distance()

        if dist < 30:
            GPIO.output(red_led_pin_1, GPIO.HIGH)
            GPIO.output(red_led_pin_2, GPIO.HIGH)
            GPIO.output(green_led_pin, GPIO.LOW)
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            GPIO.output(red_led_pin_1, GPIO.LOW)
            GPIO.output(red_led_pin_2, GPIO.LOW)
            GPIO.output(green_led_pin, GPIO.HIGH)
            GPIO.output(buzzer_pin, GPIO.LOW)

        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()