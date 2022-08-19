---
layout: post
title: "Dart 언어 관련 기초적인 정리"
description: "변수선언 관련하여 주지사항"
date: 2022-07-13
author: "김민석"
categories: [Flutter and Dart]
tags: [dart,dynamic,var,final,const,static,future,stream]
---
다른 언어도 마찬가지지만 아주 기본적인 개념이지만 쉽게 까먹거나 정리를 잘 안하고 넘어가는 것들이 있습니다.

이런것들을 한번 개념정리 해봅시다.

### dynamic vs var
```dart
var a = 1;
a = "Hello"; // ERROR
dynamic b = 1;
b = "Hello"; // OK
```
- var : 불분명한 타입이지만 한번 선언된 타입을 바꾸면 안됩니다.
- dynamic : 타입을 바꿀 수 있습니다.

JavaScript의 변수와 비슷한건 dynamic이라고 할 수 있겠네요. 추측건데 저장비용이나 연산비용은 후자가 더 많을 것 같습니다.

### final vs const vs static

먼저 final 과 const의 차이점을 알아봅시다. 간단하죠~
```dart
const int a = 1; // OK
const int b = getOne(); // ERROR
final int c = 2; // OK
final int d = getTwo(); // OK
``` 
- 공통점 : 둘다 처음에 결정된 값을 바꾸지 못합니다.
- 차이점 : const는 컴파일 전에 값을 결정, final은 런타임시에 값을 결정해도 됩니다.

당연히 이것도 저장비용, 연산비용에 차이점에 있으니까 고대부터 다르게 존재해 왔겠죠?

**그럼 static은 무엇이냐?**
```dart
class Aclass {
  static int B = 1;
  get getB => B;
  int addB() => B++;
}

void main() {
  var a1 = Aclass();
  var a2 = Aclass();
  a2.addB();
  print(a1.getB);
  print(a2.getB);
  print(Aclass.B);
  print(Aclass.getB); // ERROR
}
```
- static 으로 선언하면 해당 클래스로 선언된 모든 오브젝트에 공통으로 적용됩니다.
- 심지어 클래스명 자체로 접근도 가능하죠.
- 일종의 같은 클래스끼리의 전역변수로 사용할 수 있습니다.

### Future vs Stream

- Future는 JavaScript에서 async/await를 생각하면 됩니다. 실행이 완료될 때 까지 기다립니다.
- Stream은 yield를 이용해서 특정 변수를 리턴함으로써, 중간과정에서 이벤트를 발생시킵니다.
- Flutter에서 시간에 따른 UI 변화를 줘야 할 때 두 기능을 이용한 FutureBuilder, StreamBuilder를 사용하게 됩니다.
이때 용도도 그 정의에 따라서 달라집니다.
  - FutureBuilder : 뭔가 값이 완성될 때 까지 뺑뺑이를 돌리다가 값이 완성되면 UI 표출 할 때 사용
  - StreamBuilder : 초시계처럼 특정순간 마다 값이 바뀔때 사용