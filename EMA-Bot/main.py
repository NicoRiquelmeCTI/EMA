import network
import machine
import bme280
import ssd1306
import time
#from blynklib_mp import Blynk
from blynkapi import Blynk
import requests


BLYNK_AUTH_TOKEN = "TXxZCeqcfno9bau_hf-J9MUM2NU2HR0N"
# EJE X HW: register handler for virtual pin V6 write event

# EJE Y HW: register handler for virtual pin V3 write event

    

# Crear la instancia del sensor de presion en el pin 13 de Blynk 
SensorPresion = Blynk(BLYNK_AUTH_TOKEN, pin = "V13") 

# Crear la instancia del sensor de humedad en el pin 12 de Blynk 
SensorHumedad = Blynk(BLYNK_AUTH_TOKEN, pin = "V12")


   
# Configuración de la conexión Wi-Fi
ssid = 'Cucarachas'
password = 'Cuc4r4ch4s!'

wlan = network.WLAN(network.STA_IF)  # Modo estación (cliente)
wlan.active(True)  # Activa la interfaz Wi-Fi

if not wlan.isconnected():
    print("Conectando a la red Wi-Fi...")
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        pass

print("Conectado a la red Wi-Fi:")
print("Dirección IP:", wlan.ifconfig()[0])


from time import sleep
from machine import Pin

Mot_A_Forward = Pin(2, Pin.OUT)
Mot_A_Back = Pin(3, Pin.OUT)
Mot_B_Forward = Pin(4, Pin.OUT)
Mot_B_Back = Pin(5, Pin.OUT)

def move_forward():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)
    
def move_backward():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(1)
    Mot_B_Back.value(1)

def move_stop():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)

def move_left():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(1)

def move_right():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(1)
    Mot_B_Back.value(0)

move_stop()
sleep(2)

print("Forward test")
move_forward()
sleep(2)

print("Backward test")
move_backward()
sleep(2)

print("Spin left test")
move_left()
sleep(2)

print("Spin right test")
move_right()
sleep(2)

print("'Time for bed' said Zeberdee.")
move_stop()


i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Mostrar texto inicial en la pantalla OLED
oled.fill(0)
oled.text("Hola, mi nombre", 0, 0)
oled.text("es EMA bot", 0, 10)
oled.show()
time.sleep(4)

oled.fill(0)
oled.text("Soy una estacion", 0, 0)
oled.text("de monitoreo", 0, 10)
oled.text("ambiental", 0, 20)
oled.show()
time.sleep(4)

oled.fill(0)
oled.text("A continuacion", 0, 0)
oled.text("te mostrare la", 0, 10)
oled.text("calidad del", 0, 20)
oled.text("-----------", 0, 30)
oled.show()
time.sleep(4)

oled.fill(0)
oled.text("ENTORNO", 40, 10)
oled.text("{-------}", 33, 20)
oled.show()
time.sleep(3)  # Esperar 3 segundos antes de mostrar los datos del sensor

# Crear una instancia del sensor BME280
sensor = bme280.BME280(i2c=i2c)

# Función para mostrar los datos del sensor en la pantalla OLED
def show_sensor_data(temp, pressure, humidity):
    oled.fill(0)
    oled.text("Temperatura: {} C".format(int(temp / 100)), 0, 0)
    oled.text("Presión: {:.2f} hPa".format(pressure / 100), 0, 10)
    oled.text("Humedad: {:.2f} %".format(humidity / 1024), 0, 20)
    oled.show()
    

# Python3 script to interface basic Blynk rest API with Raspberry PI

def write(token,pin,value):
    api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
    response = requests.get(api_url)
    if "200" in str(response):
        print("Value successfully updated")
    else:
        print("Could not find the device token or wrong pin format")

def read(token,pin):
    api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
    response = requests.get(api_url)
    return response.content.decode()
    
while True:
    #BLYNK.disconnect()
    
    # Leer los datos del sensor BME280
    temperature, pressure, humidity = sensor.read_compensated_data()
    # HUMEDAD set pin value (one) 
    print("Humedad: {:.2f} %".format(pressure / 100))
    ValorPresion ="{}".format(pressure / 100)
    SensorPresion.set_val(["120"])
    # PRESION set pin value (one)
    print("Presión: {:.2f} hPa".format(pressure / 100)) 
    ValorHumedad ="{}".format(humidity / 1024)
    SensorHumedad.set_val([ValorHumedad])
    # Mostrar los datos del sensor BME280 en la pantalla OLED
    show_sensor_data(temperature, pressure, humidity)
    # Example: write the virtual PIN v1 to set it to 100:
    #write(BLYNK_AUTH_TOKEN,"v12", "{}".format(humidity / 1024))
    # Example: write the virtual PIN v1 to set it to 100:
    #write(BLYNK_AUTH_TOKEN,"v13", "{}".format(pressure / 100))
    # Lectura analógica del sensor MQ-135
    analog_pin = machine.ADC(26)  # Pin analógico del sensor MQ-135
    analog_value = analog_pin.read_u16()  # Lectura en formato de 16 bits

    # Cálculo de la concentración de gases
    voltage = analog_value * 3.3 / 65535  # Conversión a voltaje

    # Fórmulas de conversión para diferentes gases
    co2_ppm = 5000 * voltage / 3.3  # Concentración de CO2 en partes por millón (ppm)
    co_ppm = 50 * voltage / 3.3  # Concentración de CO en partes por millón (ppm)
    nox_ppm = 100 * voltage / 3.3  # Concentración de NOx en partes por millón (ppm)
    
    # Imprimir los valores de concentración de gases del MQ-135
    print("Concentración de CO2: {:.2f} ppm".format(co2_ppm))
    #write(BLYNK_AUTH_TOKEN,"v1", "{}".format(co2_ppm))
    print("Concentración de CO: {:.2f} ppm".format(co_ppm))
    #write(BLYNK_AUTH_TOKEN,"v2", "{}".format(co_ppm))
    print("Concentración de NOx: {:.2f} ppm".format(nox_ppm))
    #write(BLYNK_AUTH_TOKEN,"v3", "{}".format(nox_ppm))
    time.sleep(5)


