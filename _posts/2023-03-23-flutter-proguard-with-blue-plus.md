---
layout: post
title: "Flutter 에서 flutter_blue_plus 이용시 릴리즈모드 에러 해결하기"
description: "proguard-rules 설정을 통해 특정 의존성의 코드/리소스 축소 제외시키기"
date: 2022-11-04
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,proguard_rule,bluetooth,flutter_blue_plus]
---
### 문제의 상황

- Flutter를 이용해서 bluetooth 연결을 하고자 합니다.
- 그래서 저는 flutter_blue_plus라는 패키지를 이용하기로 했습니다. 
  - https://pub.dev/packages/flutter_blue_plus
- 디버그 모드에서는 잘 돌아갔으나, 릴리즈 모드에서 아래와 같은 에러가 발생하면서 기기 스캔이 정상동작 하지 않더군요.
```
    E/flutter (20889): [ERROR:flutter/lib/ui/ui_dart_state.cc(209)] 
    Unhandled Exception: PlatformException(startScan, 
    Field androidScanMode_ for j.e0 not found. 
    Known fields are [private int j.e0.h, 
    private k.b0$i j.e0.i, private boolean j.e0.j, private static final j.e0 
    j.e0.k, private static volatile k.a1 j.e0.l], 
    java.lang.RuntimeException: Field androidScanMode_ for j.e0 not found. 
    Known fields are [private int j.e0.h, private k.b0$i j.e0.i, 
    private boolean j.e0.j, private static final j.e0 j.e0.k, private static volatile k.a1 j.e0.l]

    E/flutter (20889):      at k.v0.n0(Unknown Source:72)
    E/flutter (20889):      at k.v0.T(Unknown Source:655)
    E/flutter (20889):      at k.v0.R(Unknown Source:12)
    E/flutter (20889):      at k.k0.e(Unknown Source:60)
    E/flutter (20889):      at k.k0.a(Unknown Source:49)
    E/flutter (20889):      at k.d1.d(Unknown Source:17)
    E/flutter (20889):      at k.d1.e(Unknown Source:4)
    E/flutter (20889):      at k.z$a.z(Unknown Source:9)
    E/flutter (20889):      at k.z$a.y(Unknown Source:4)
... 생략
```

### 원인은? 

- 원인을 파악해보니 android/app/build.gradle 파일에서 릴리즈 모드시에 설정한 코드 축소관련 내용 때문이었습니다.
```
    shrinkResources true
    minifyEnabled true
    proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'       
``` 
- minifyEnabled 는 코드를 축소해서 릴리즈시켜주고, shrinkResources 는 리소스를 축소키져주죠. 여기서 충돌이 일어났던것 같군요.
- 둘다 false로 해주면 정상동작이야 하지만, 이러면 앱이 무거워지므로 좋은 방법이 아닙니다.
   
 
### 해결책

- proguard-rules에서 해당 의존성을 제외해주세요. proguard-rules.pro 파일에 보면 아래와 같이 축소대상에서 제외되는 패키지들을 지정할 수 있는데요.

```
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

-keep class com.boskokg.flutter_blue_plus.** { *; }

-dontwarn io.flutter.embedding.**
```

- flutter_blue_plus 는 위와 같이 지정해주면 됩니다. github 주소를 보면 전체주소 값이 추측이 됩니다.
  - https://github.com/boskokg/flutter_blue_plus