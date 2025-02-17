---
layout: post
title: "Mosquitto와 라즈베리파이 피코를 이용해서 실외 온도 측정하기"
description: "마이크로파이선으로 작성된 IOT코드와 MQTT 통신을 통해 정보를 발행하고, TypeScript 코드로 구독합니다"
date: 2025-02-17
author: "김민석"
categories: [Others]
tags: [mqtt,am2320,mosquitto,micropython,rasberrypi,pico,typescript,dth22]
---
### 라즈베리파이 피코 + DHT22(AM2320) 온습도 센서모듈
- 야외의 온도를 측정하기 위해서는 저전력 IoT 기술이 필요합니다.
- 다행스럽게돋 라즈베리파이 피코는 저전력이면서 상대적으로 훌륭한 연산능력을 보여주죠, 게닫가 Wifi 통신도 가능합니다.
    - ![PICO](https://reddol18.github.io/dev5min/images/20250217/1.jpeg)
- 여기에 온습도 센서모듈을 연결하여 Wifi로 통신을 하면 실외온도 측정이 가능해집니다.
    - ![DHT22](https://reddol18.github.io/dev5min/images/20250217/2.jpeg)
- 교육용 아두이노 키트에 함께 들어있는 DHT11 센서는 영하의 온도는 측정이 불가능합니다. 그래서 저는 DHT22 센서가 들어간 모듈을 이용했습니다.

### 마이크로 파이선 그리고 AM2320 라이브러리 설치
- 라즈베리파이 피코는 마이크로 파이선을 이용해서 코드를 작성할 수 있는데요, 온도센서 모듈을 이용하기 위해서는 AM2320 라이브러리를 추가적으로 설치해야 합니다.
- 그런데 동작하는 라이브러리를 찾기가 어려웠어요. 이게 맞다 저게 맞다 하는 외국 사이트의 포스팅들을 뒤져보다가 제가 찾아낸 것은 바로 아래 링크의 소스코드 입니다.
    - [AM2320 라이브러리](https://github.com/mcauser/micropython-am2320)
    - 설치법은 위 링크를 참고해주세요.

### Mosquitto 그리고 MQTT
- HTTP 서버를 만들고 피코에서 request를 보내서 온도를 확인하는 방법도 있습니다만
- MQTT 통신을 이용하면 전력효율이 더 높다고 하기 때문에, 서버 PC에 mosquitto를 설치했습니다.

### TypeScript MQTT 구독 서버
- 온도값을 구독하기 위한 간단한 서버를 TypeScript를 이용해서 작성합니다.

```javascript
import * as mqtt from 'mqtt';

const client = mqtt.connect('mqtt://IP:PORT', {keepalive: 3600});

client.on('connect', () => {
    console.log('connected');
    client.subscribe('구독토픽');
});

client.on('message', (topic: String, message: Buffer) => {
    console.log(topic + ' ' + message.toString());
});

client.on('error', (err: Error)=> {
    console.error(err);
    client.end();
});

client.on('close', () => {
    console.log('disconnected');
});
```

{% include adfit.html %}    

### 마이크로 파이선 발행 코드
- 이제 피코에 들어갈 발해용 서버를 작성하겠습니다. 구현에 앞서서 mqtt 라이브러리인 설치합니다.

```python
import mip
mip.install('umqtt.simple')
```

- 코드는 아래와 같습니다.

```python
import utime
import rp2 
from machine import I2C, Pin
import network
import time
import urequests as requests
import am2320
import ujson
import umqtt.simple

mqtt_broker_ip = "IP at mosquitto"
client_id = "d2"
ssid = '공유기 ID'
password = '공유기 비번'

def send_message_mqtt(client, h,t):
    print("Publish Mqtt Message")
    msg = ujson.dumps({'device_id': client_id, 'temperature': t, 'humidity': h})
    try:
        client.publish("구독토픽", msg)
    except OSError as e:
        print(e)
    
def wlan_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Setup onboard LED
    onboard_led = Pin('LED', Pin.OUT)  # Adjust the pin number if necessary

    # Initial connection attempt
    max_attempts = 10
    attempts = 0
    connected = False  # Flag to track connection status

    while not wlan.isconnected() and attempts < max_attempts:
        onboard_led.toggle()  # Blink LED while trying to connect
        time.sleep(1)
        attempts += 1
        
    if wlan.isconnected():
        print(f"Connected to {ssid} successfully!")
        print("Network Config:", wlan.ifconfig())
        onboard_led.value(1)  # Keep LED on when connected
        connected = True
    else:
        print("Failed to connect to WiFi.")
        onboard_led.value(0)  # Turn off LED if initial connection fails
    return [wlan, connected]

def mqtt_connect():
    print("Try Mqtt Connect")
    client = umqtt.simple.MQTTClient(client_id = client_id, server = mqtt_broker_ip, port = #MQTT포트)
    client.connect()
    return client

def am2320_connect():
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
    sensor = am2320.AM2320(i2c)

    if sensor.check():
        print(f"AM2320 found at I2C address {am2320.I2C_ADDRESS:#x}")
    
    return sensor

        
def main_mqtt():
    wret = wlan_connect()
    wlan = wret[0]
    connected = wret[1]
    client = 0
    utime.sleep(3)
    try:
        client = mqtt_connect()
    except OSError as e:
        print(f"Error: %s" % e)
    print("Mqtt Connect Done")
    
    step1 = 2
    utime.sleep(1)

    sensor = am2320_connect()
        
    while True:
        if step1 == 2:
            print('reading')
            total=0
            sensor.measure()
            humidity = sensor.humidity()
            temperature = sensor.temperature()
            
            print("M2 Humidity: %d%%, Temp: %dC" % (humidity, temperature))        
                
            if wlan.isconnected() and not connected:
                print("Reconnected to WiFi.")
                onboard_led.value(1)  # Keep LED on when connected
                print("Network Config:", wlan.ifconfig())
                connected = True
            elif not wlan.isconnected() and connected:
                print("Disconnected from WiFi.")
                connected = False

            if not connected:
                print("Wlan Not Connected")
                onboard_led.toggle()  # Blink LED if disconnected
            else:
                if client == 0:
                    print("MQTT is not connected")
                else:
                    send_message_mqtt(client, humidity, temperature)                
                
            step1 = 1
        else:
            step1 = step1 + 1
        
        utime.sleep(30)

main_mqtt()
```

- 위 코드는 30초에 한번씩 온습도를 측정해서 데이터를 발행합니다.
- 서버PC에 mosquitto가 실행중이고, 구독서버가 돌아가고 있다면 발행된 정보가 보여지게 됩니다.
- AM2320 회로구성시, SCL은 피코의 17번 SDL은 피코의 16번 핀에 연결했습니다.
    - ![회로구성](https://reddol18.github.io/dev5min/images/20250217/3.jpeg)

### 시연연상
- 완성된 시스템을 이용해서 온도측정에 성공한 영상 입니다.
- [영상](https://youtube.com/shorts/vd1t1v9K8ZY?si=PVW2bGTOaQHfcr6f)