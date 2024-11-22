---
layout: post
title: "Flutter에서 느려지는 현상 없는 폴더선택 다이얼로그 만들기"
description: "파일이 매우 많을 경우에 화면이 멈추는 현상을 극복해 봤습니다"
date: 2024-11-22
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,folder,folder_picker,directory,direcotry_picker,dialog,no_delay]
---
- 요즘 스마트폰 용량이 TB급으로 늘어나면서, 사진을 찍어놓고 PC에 옮기지 않는 분들이 많을겁니다.
- 사진 폴더에 파일이 많다보니 폴더 내부에 파일을 로딩할 때 시간이 오래걸리게 됩니다.
- 저 같은 경우에 유튜브에서 사용하기 위한 영상을 PC로 옮기려다 보니, 이럴 때 지연되는 시간이 아깝더라구요.
- 그래서 사진을 년/월/일 별로 폴더화 해서 저장해서 필요한 폴더만 PC로 옮기곤 합니다.
- 그런데 이것도 매번 수동으로 하려고 하니까 귀찮더군요, 그래서 폴더로 저장하는 것을 자동화 하는 앱을 만들어 봤어요.
- 하지만 PC에서 느려지는 문제는 당연히 스마트폰에서도 똑같이 발생하더군요
- 자동화해서 옮길 대상 폴더를 선택하는 다이얼로그도 결국 해당 폴더에 있는 파일 정보를 훑어야 표출할 수 있기 때문에,
  결국 느려지는 문제는 계쇡되게 됩니다.
- 이 문제를 해결하기 위해서 여러 유형의 폴더선택 다이얼로그들을 찾아봤는데요...
  - directory.dart 에 존재하는 listSync 함수를 이용해서 파일 리스트를 가져오는 것만 있더군요.
  - 이 함수는 모든 정보를 가져올 때 까지 기다려야 하기 때문에, 폴더내에 파일이 많으면 느려지는 현상이 발생합니다.
  - 저는 listSync 함수가 아닌 list 함수를 이용해 봤어요.
  - list 함수는 stream을 이용하기 때문에, ListView.builder 와 연결해서 파일 정보를 가져올 때 마다 state를 수정하면서
    갱신하면 됩니다. 이러면 지연 현상이 발생하지 않습니다.

{% include adfit.html %}    

- 주요 코드부는 아래와 같습니다.

```dart
dstream = directory!.list();
dstream.listen((item) {
  debugPrint(item.path);
  if (FileSystemEntity.isDirectorySync(item.path)) {
    setState(() {
      directories.add(item);
    });
  }
}, onDone: () {
  setState(() {
    debugPrint("Done Path Find");
    isDone = true;
  });
});
```

- 이때 다이얼로그를 구성하는 코드는 아래 레포지토리를 참고했어요.
  - [Easy-Folder-Picker](https://github.com/kapilmhr/Easy-Folder-Picker)
  - InheritedWidget과 WidgetsBindingObserver를 이용한 디자인 패턴이 상당히 효과적이더라구요.
  - 물론 이 패키지도 listSync를 쓰기 때문에 지연현상은 발생합니다.

- 제가 만든 어플의 레포지토리는 아래 링크입니다.  
  - [PicFor](https://github.com/reddol18/picfor)