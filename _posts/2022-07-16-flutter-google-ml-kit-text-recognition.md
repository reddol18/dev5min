---
layout: post
title: "Flutter 에서 Google ML Kit으로 OCR 해보기"
description: "Google ML Kit을 이용해서 OCR을 수행하는 간단한 Flutter 앱을 만들었습니다"
date: 2022-07-16
author: "김민석"
categories: [Computer Vision]
tags: [flutter,google ml kit,ocr,text recognition,text,detection]
---
지난번에 EasyOCR을 이용해서 이미지에서 텍스트를 인식하는 시도를 해보았습니다.

[EASYOCR을 이용해서 글자인식을 해보자](easyocr-use)

오늘은 이러한 동작을 스마트폰에서도 수행할 수 있도록 간단한 앱을 만들어 보았습니다.
Flutter에서도 Google ML Kit을 이용해서 이것이 가능한데요. 아래 링크를 참고하세요.

[Google ML Kit for Flutter](https://pub.dev/packages/google_ml_kit)

저는 이중에서 Text Recognition V2를 이용했습니다. 이걸 써야 한글도 인식할 수 있어요.

사용한 주요 함수의 소스코드를 공유합니다.
이미지 선택하는 라이브러리는 아래 링크의 것을 이용했습니다.

[Flutter Image Picker](https://pub.dev/packages/image_picker)

### 주요 소스코드

{% include more_front.html %}
```dart
  // 이렇게 하면 기본세팅인 영어 입니다.     
  final TextRecognizer _textRecognizer = TextRecognizer();
  // 아래 주석내용 처럼 해야 한국어 입니다.
  // final TextRecognizer _textRecognizer = TextRecognizer(script: TextRecognitionScript.korean);
        
  // UI에서 버튼 클릭했을 때 이벤트 함수  
  Future<void> textDetect() async {
    var image = await ImagePicker.platform.pickImage(source: ImageSource.gallery);
    String path = image!.path;
    await processImage(InputImage.fromFilePath(path));
  }

  // 실제 텍스트를 인식하는 함수
  Future<void> processImage(InputImage inputImage) async {
    if (!_canProcess) return;
    if (_isBusy) return;
    _isBusy = true;
    setState(() {
      _text = '';
    });
    final recognizedText = await _textRecognizer.processImage(inputImage);
    if (inputImage.inputImageData?.size != null &&
        inputImage.inputImageData?.imageRotation != null) {
    } else {
      _text = 'Recognized text:\n\n${recognizedText.text}';
    }
    _isBusy = false;
    if (mounted) {
      setState(() {});
    }
  }
```
**recognizedText.blocks 를 이용해서 인식된 텍스트 영역을 알아낼 수 있습니다.**
{% include more_tail.html %}

EasyOCR에서 사용했던 시료를 똑같이 써서 테스트 해봤습니다. 
어떤 시료 였는지는 최상단 링크의 글을 확인해주세요.

### 테스트 결과
- 시료1
  - ![이미지1](https://reddol18.github.io/dev5min/images/20220716/2/1.jpg)
  - EasyOCR 보다는 인식률이 좋습니다. 속도도 빠르구요. 특수문자도 인식하는군요.
- 시료2
  - ![이미지2](https://reddol18.github.io/dev5min/images/20220716/2/2.jpg)
  - 이건 차이가 없습니다. 오히려 특수문자로 오인식되는 부분이 있네요. 
- 시료2
  - ![이미지3](https://reddol18.github.io/dev5min/images/20220716/2/3.jpg)
  - 이건 오히려 영어로 인식해 버리네요. EasyOCR은 `벼`로 오인식했는데, 이건 `L4`로 인식해 버립니다.
 