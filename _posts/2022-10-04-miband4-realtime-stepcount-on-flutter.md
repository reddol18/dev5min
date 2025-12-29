---
layout: post
title: "Flutter에서 MiBand4의 현재걸음수를 가져오기"
description: "블루투스 통신을 이용해서 MiBand4의 현재걸음수 정보를 가져오는 방법을 알아봤습니다"
date: 2022-10-04
feature_image: /images/default-thumbnail.jpg
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,miband,miband4,stepcount,bluetooth]
---
써드파티 앱에서 샤오미 미밴드(MiBand4)에 집계된 현재걸음수를 알아내려면 어떻게 해야 할까요?
오늘은 그 방법에 대해 정리해보고자 합니다. 방법은 간단합니다. 
일단 flutter_blue_plus 라이브러리를 dependencies에 정의해주세요.

그런 다음 flutter_blue_plus 인스턴스와 변수들을 초기화 합니다.
```dart
static const String MI_BAND_NAME = "Mi Smart Band 4";
static const String UUID_SERVICE_MIBAND =
      "0000fee0-0000-1000-8000-00805f9b34fb";
static const String UUID_CHARACTERISTIC_REALTIME_STEPS =
      "00000007-0000-3512-2118-0009af100700";
FlutterBluePlus flutterBlue = FlutterBluePlus.instance;
BluetoothDevice? miDevice;
BluetoothCharacteristic? stepChr;
``` 

그리고 나서 연결하려는 블루투스 디바이스를 찾습니다. 저 같은 경우엔 디바이스 네임을 특정해서 하드코딩된 방식으로
찾았지만, 보통의 경우 별도의 선택 UI를 만들어서 연결합니다.
```dart
// 이미 연결되어 있으면 먼저 연결을 해제합니다
List<BluetoothDevice> devices = await flutterBlue.connectedDevices;
if (devices.length > 0) {
  for (BluetoothDevice d in devices) {
    if (d.name == MI_BAND_NAME) {
      d.disconnect();
    }
  }
}
// 이제 다시 연결합니다. 
flutterBlue.startScan(timeout: Duration(seconds: 4));
var subs = flutterBlue.scanResults.listen((results) async {
  for (ScanResult r in results) {
    if (r.device.name == MI_BAND_NAME) {
      miDevice = r.device;
      flutterBlue.stopScan();
      await miDevice!.connect(timeout: Duration(seconds: 4), autoConnect: false);
    }
  }
});
```

이제 현재걸음수를 얻기 위해 필요한 블루투스특성을 얻어옵니다. 
```dart
List<BluetoothService> services = await miDevice!.discoverServices();
for (BluetoothService s in services) {
    if (s.uuid.toString() == UUID_SERVICE_MIBAND) {
        for (BluetoothCharacteristic c in basicService!.characteristics) {
            if (c.uuid.toString() == UUID_CHARACTERISTIC_REALTIME_STEPS) {
              stepChr = c;
            }
        }
    }
}
```

마지막으로 해당특성을 이용해서 현재 걸음수를 얻어와 봅시다. 여기서 중요한 점은 돌아오는 바이트스트림의 1,2번째에
숫자가 패키징되어서 저장된다는 점 입니다.
```dart
await stepChr!.setNotifyValue(true);
stepChr!.value.listen((data) {
    if (data.length > 2) {
        int steps = ((((data[1] & 255) | ((data[2] & 255) << 8))));
        print("Current Step: ${steps}");
    }      
});
```

심박수 정보도 얻어오고 싶은데 아직은 연구가 필요한 상황입니다. 추후에 정리되면 게시하겠습니다.
그 이후에 음악재생하는 방법도 게시해보고자 합니다.  