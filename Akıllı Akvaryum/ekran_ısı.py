from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import Adafruit_DHT
import time
from datetime import datetime

lcd = LCD()
sensor = Adafruit_DHT.DHT11
pin = 4  # DHT11 sensörünün bağlı olduğu GPIO pinini buraya girin


def safe_exit(signum, frame):
    exit(1)


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    while True:
        # Sıcaklık ve nem bilgisi
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            lcd.text("SICAKLIK: {:.1f}C".format(temperature), 1)
            lcd.text("NEM: {}%".format(humidity), 2)
        else:
            lcd.text("Failed to read", 1)
            lcd.text("sensor data", 2)

        time.sleep(5)  # 5 saniye bekleme

        # Tarih ve saat bilgisi
        lcd.clear()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")
        lcd.text("TARIH:" + current_date, 1)
        lcd.text("SAAT:" + current_time, 2)

        time.sleep(5)  # 5 saniye bekleme

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()