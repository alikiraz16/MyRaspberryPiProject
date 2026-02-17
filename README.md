# Akıllı Akvaryum Projesi (Raspberry Pi)

Bu proje, Raspberry Pi kullanarak geliştirilmiş bir akıllı akvaryum / çevresel izleme sistemidir. Sistem, sıcaklık ve nem takibi yapar, mesafeyi kontrol eder ve belirli durumlarda uyarı verir. Ayrıca bir servo motoru kontrol ederek yemleme mekanizması için hareket sağlar.

## Özellikler

*   **Sıcaklık ve Nem İzleme:** DHT11 sensörü kullanarak ortamın veya akvaryum çevresinin sıcaklık ve nem değerlerini ölçer.
*   **LCD Ekran Bilgilendirme:** Ölçülen sıcaklık/nem değerlerini ve güncel tarih/saat bilgisini I2C LCD ekran üzerinde dönüşümlü olarak gösterir.
*   **Mesafe Kontrolü ve Uyarı Sistemi:** HC-SR04 ultrasonik sensör ile mesafe ölçümü yapar. Mesafe 30 cm'nin altına düştüğünde (örneğin bir nesne yaklaştığında) sesli (Buzzer) ve görsel (Kırmızı LED) uyarı verir. Normal durumda Yeşil LED yanar.
*   **Servo Motor Kontrolü:** Belirli aralıklarla otomatik yemleme için servo motoru hareket ettirir.
*   **Çoklu Görev (Multithreading):** Sensör okuma ve mesafe kontrolü işlemleri ayrı iş parçacıklarında (thread) eş zamanlı olarak çalışır.

## Gereksinimler

### Donanım
*   Raspberry Pi (Herhangi bir model, GPIO pinleri olan)
*   DHT11 Sıcaklık ve Nem Sensörü
*   HC-SR04 Ultrasonik Mesafe Sensörü
*   I2C LCD Ekran (16x2)
*   Servo Motor
*   Buzzer
*   LED'ler (2x Kırmızı, 1x Yeşil)
*   Dirençler (LED'ler için uygun değerlerde)
*   Bağlantı kabloları (Jumper kablolar)
*   Breadboard (Opsiyonel)

### Yazılım / Kütüphaneler
Projede aşağıdaki Python kütüphaneleri kullanılmaktadır:
*   `RPi.GPIO`
*   `Adafruit_DHT`
*   `rpi_lcd`

Bu kütüphaneleri yüklemek için:
```bash
sudo pip3 install rpi-lcd Adafruit_DHT RPi.GPIO
```
*(Not: Bazı kütüphaneler sistem paketlerine ihtiyaç duyabilir veya `venv` içinde kurulum gerektirebilir.)*

## Pin Bağlantıları

Kod içerisindeki varsayılan pin tanımlamaları şöyledir (BCM numaralandırma):

| Bileşen | Pin (BCM) | Açıklama |
| :--- | :--- | :--- |
| **DHT11** | 4 | Veri Pini |
| **HC-SR04** | TRIG: 23, ECHO: 24 | Mesafe Sensörü |
| **Kırmızı LED 1** | 22 | Uyarı LED'i |
| **Kırmızı LED 2** | 27 | Uyarı LED'i |
| **Yeşil LED** | 17 | Durum LED'i (Normal) |
| **Buzzer** | 12 | Sesli Uyarı |
| **Servo Motor** | 18 | Motor Kontrol Pini |
| **LCD Ekran** | SDA/SCL Pinleri | I2C Bağlantısı |

*(Bağlantı şeması için proje dosyalarındaki `pinler.jpg` veya `raspberryPiBağlantılarıResim.png` görsellerine bakabilirsiniz.)*

## Kurulum ve Çalıştırma

1.  Projeyi klonlayın:
    ```bash
    git clone https://github.com/alikiraz16/MyRaspberryPiProject.git
    cd MyRaspberryPiProject
    ```

2.  Bağlantılarınızı şemaya ve kod içindeki pin tanımlarına göre yapın.

3.  Ana programı çalıştırın:
    ```bash
    python3 main.py
    ```

## Dosyalar Hakkında

*   `main.py`: Projenin ana dosyasıdır. Tüm modülleri (sensör, LCD, servo, mesafe) `threading` kullanarak bir arada çalıştırır.
*   `ekran_ısı.py`: Sadece LCD ekran ve DHT11 sensörünü test etmek veya çalıştırmak için kullanılan modül.
*   `mesafe_buzzer_led.py`: Sadece mesafe sensörü, LED'ler ve buzzer kontrolünü içeren modül.

## Lisans
Bu proje açık kaynaklıdır ve eğitim/hobi amaçlı geliştirilmiştir.
