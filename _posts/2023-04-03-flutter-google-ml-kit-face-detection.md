---
layout: post
title: "Flutter 에서 Google ML Kit으로 얼굴인식 수행하기"
description: "Google ML Kit을 이용해서 얼굴인식을 수행하는 간단한 Flutter 앱을 만들었습니다"
date: 2023-04-03
author: "김민석"
categories: [Computer Vision]
tags: [flutter,google ml kit,face,detection]
---
오늘은 Flutter에서 다양한 유형의 사진을 다중선택 한 후
Google ML Kit의 얼굴인식 기능을 이용하여 사람이 사진 속에 존재하는지를
판정하는 간단한 앱을 만들어 보겠습니다. 

- [Google ML Kit for Flutter](https://pub.dev/packages/google_ml_kit)

사진 다중 선택은 예전에도 사용해봤던 아래 패키지를 이용하고자 합니다.

- [Flutter Image Picker](https://pub.dev/packages/image_picker) 

아울러서 이미지 타입을 용이하게 변환하고자 다음 패키지도 이용합니다.
- [cross_file_image](https://pub.dev/packages/cross_file_image) 

### 주요 소스코드
```dart
// .. 전략
// 간단하게 클래스 하나 정의하구요
class ImageObj {
  final String title;
  final Image image;
  ImageObj({
    required this.title,
    required this.image,
  });
}

class _MyHomePageState extends State<MyHomePage> {
// 스테이트 클래스 내부에 아래처럼 위에서 정의한 클래스와 
// 얼굴인식 용 오브젝트를 선언합니다.
  List<ImageObj> images = [];
  final FaceDetector _faceDetector = FaceDetector(
    options: FaceDetectorOptions(
      enableContours: true,
      enableClassification: true,
    ),
  );
  Future<void> _doDetect() async {
    final ImagePicker picker = ImagePicker();
    // 이미지 선택 다이얼로그 띄웁니다
    List<XFile> imagesFromPicker = await picker.pickMultiImage();
    List<int> faceCount = [];
    images = [];
    for(XFile item in imagesFromPicker) {
      // 이미지 피커에서 사용하는 XFile 타입을 ML Kit에서 사용하는 InputImage 형태로 변경
      final faces = await _faceDetector.processImage(InputImage.fromFilePath(item.path));
      faceCount.add(faces.length);
    }
    setState(() {
      int i = 0;
      for(XFile item in imagesFromPicker) {
        // XFile 타입을 이미지 뷰어에서 사용하는 Image 타입으로 변환하기 위해서
        // cross_file_image 패키지를 여기서 사용합니다.
        images.add(
          ImageObj(title: faceCount[i++] > 0 ? 
            "Human" : "No Human", image: Image(image: XFileImage(item))));
      }
    });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: images.length > 0 ? ListView.builder(
            itemCount: images.length,
            itemBuilder: (context, index) {
                  return ListTile(
                    leading: images[index].image,
                    title: Text(images[index].title),
                    onTap: () {
                    },
                );
        }) : Text("No Images"),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _doDetect,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ), 
    );
  }
}
```

### 수행결과
- ![이미지1](https://reddol18.github.io/dev5min/images/20230403/1.png)
- ![이미지2](https://reddol18.github.io/dev5min/images/20230403/2.png)
- 사람이 아닌 것은 확실히 "아니라고" 합니다. 정확히 표현하면 사람 얼굴을 0개 찾아냅니다.
  - 빵, 꽃, 고양이 사진을 선택했는데 모두 아니라고 나옵니다.
- 그런데 사람의 경우에는 정면사진이 아닐 경우 오인식이 나타나는군요.
  - 아무래도 ML 모델의 원리가 눈도 2쌍, 귀도 2쌍이어야 하고
  - 동공이 측정되어야하고 이목구비의 거리 및 비율 등을 특징값으로 학습한 것이 아닐까 추측됩니다.
  - 옆 모습이나, 눈감은 모습, 누워있는 모습은 얼굴이 0개로 측정되는 경우가 있습니다.