import threading
from rpi_lcd import LCD
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)  # GPIO pin numaralandırma modunu BCM olarak ayarla

lcd = LCD()
sensor = Adafruit_DHT.DHT11
pin = 4  # DHT11 sensörünün bağlı olduğu GPIO pinini buraya girin


# Sensör verilerini okuma işlevi
def read_sensor_data():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            lcd.text("SICAKLIK: {:.1f}C".format(temperature), 1)
            lcd.text("NEM: {}%".format(humidity), 2)
        else:
            lcd.text("Failed to read", 1)
            lcd.text("sensor data", 2)

        time.sleep(5)  # 5 saniye bekleme

        lcd.clear()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")
        lcd.text("TARIH:" + current_date, 1)
        lcd.text("SAAT: " + current_time, 2)

        time.sleep(5)  # 5 saniye bekleme


# Mesafe kontrolü işlevi
def control_distance():
    TRIG = 23
    ECHO = 24
    red_led_pin_1 = 22
    red_led_pin_2 = 27
    green_led_pin = 17
    buzzer_pin = 12

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
        pass

    finally:
        GPIO.cleanup()


# Servo motor kontrolü işlevi
def setAngle(angle):
    servoPIN = 18  # Servo motorun GPIO pin numarası

    try:
        GPIO.setup(servoPIN, GPIO.OUT)
        pwm = GPIO.PWM(servoPIN, 50)  # PWM frekansını 50 Hz olarak ayarla
        pwm.start(0)

        duty = angle / 18 + 2
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)

        pwm.stop()
        GPIO.cleanup(servoPIN)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup(servoPIN)


if __name__ == "__main__":
    sensor_thread = threading.Thread(target=read_sensor_data)
    sensor_thread.start()

    control_distance_thread = threading.Thread(target=control_distance)
    control_distance_thread.start()

    try:
        while True:
            setAngle(0)  # 0 dereceye git
            time.sleep(0.5)  # Bekleme süresi
            setAngle(180)  # 180 dereceye git
            time.sleep(0.5)  # Bekleme süresi
            setAngle(0)  # 0 dereceye geri dön
            time.sleep(10)  # 10 saniye bekle

    except KeyboardInterrupt:
        GPIO.cleanup()