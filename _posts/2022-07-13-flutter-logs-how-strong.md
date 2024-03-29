---
layout: post
title: "Flutter Logs는 얼마나 견고한가?"
description: "Flutter Logs가 끊김없이 계속 실행되는지 실험해봤습니다"
date: 2022-07-13
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,logs]
---
CLI로 ``flutter logs``를 실행하면 flutter에서 print 명령으로 전달된 로그를 확인할 수 있습니다.
이건 너무 간단한 일인데, 사용하다보니 과연 끊김없이 잘 전달 될까 하는 고민이 들더라구요.
그래서 실험을 해봤습니다.
지난번에 메모리 체크를 위해 만들었던 HelloWord 앱을 조금 바꿔서 테스트를 해봤어요.

```dart
_timer = Timer.periodic(Duration(seconds: 10), (timer) {
    if (_counter < 2880) {
      setState(() {
        _counter++;
      });
      print("MyLog: ${_counter}");
    }
  });
```

10초에 한번씩 2880번, 그러니까 8시간동안 계속 로그를 남겨봤습니다.

``
flutter logs > mylog.log
``

PC에서는 이렇게 실행해놓고

앱을 킨 다음에 와이파이 켜놓고 8시간동안 잠을 자면 실험 끝인데요.

다음날 일어나서 로그파일을 확인하니, 2880번 실행된게 아니군요.
1770번 까지만 실행되어 있었습니다.
중간에 앱이 꺼져있기도 했고, PC의 절전모드를 끄는걸 깜빡했습니다.
뭐.. 아무튼 1770번 로그가 전달되는 동안 빠트림 없이 왔느냐를 체크해봅면 됩니다.
그런데 뭔가 이상하네요.

![이미지1](https://reddol18.github.io/dev5min/images/20220713/2/1.png)

1770개가 있어야 하는데 1771개가 존재한다고 나옵니다.
뭔가 중복된게 아닌지 의심됩니다.
거참 귀찮게 하는구먼~

스크립트를 짤까 하다가 자세히보니 오! 찾았다 요놈!!
중간에 26이 두번 왔네요.
- 타이머가 2번 발생할리는 없겠죠?
- 그렇다면 패킷이 두번 왔다는건가? 근데 그것도 타이머가 2번 발생할 확률만큼 낮지 않을까요?
- print가 2번 데이터를 보냈다는게 합리적인 추론인데, 이게 print 자체의 
문제인지 값을 받아들이는 flutter logs의 문제인지는 더 연구가 필요할 듯 합니다.

### 결론

상황에 따라서 flutter logs가 중복된 log를 받을 수 있으니 유의합시다