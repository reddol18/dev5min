---
layout: post
title: "Flutter 에서 Google ML Kit으로 아기사진 골라내기"
description: "Google ML Kit을 이용해서 아기사진만 골라내는 간단한 Flutter 앱을 만들었습니다"
date: 2023-04-05
author: "김민석"
categories: [Computer Vision]
tags: [flutter,google ml kit,image labeling]
---
지난번에 Google ML Kit for Flutter의 Face Detection을 이용하는
간단한 앱을 만들어 봤습니다.

- [Flutter 에서 Google ML Kit으로 얼굴인식 수행하기
](https://reddol18.github.io/dev5min/flutter-google-ml-kit-face-detection)

오늘은 Image Labeling을 이용해서 아기사진만 골라내는 코드를 작성해 보았습니다.
지난번 코드에서 크게 달라지는 부분은 없습니다. FaceDetection 관련된 로직이
Image Labeling으로 바뀌는 정도 입니다.

자세한 정보는 아래 링크를 참고하세요.

- [ML Kit Image Labeling](https://developers.google.com/ml-kit/vision/image-labeling?hl=ko)

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
// 이미지 라벨링 용 오브젝트를 선언합니다.
  List<ImageObj> images = [];
  final imageLabeler =
        ImageLabeler(options: ImageLabelerOptions(confidenceThreshold: 0.5));
  
  Future<void> _doDetect() async {
    final ImagePicker picker = ImagePicker();
    // 이미지 선택 다이얼로그 띄웁니다
    List<XFile> imagesFromPicker = await picker.pickMultiImage();
    List<bool> hasBabyIndex = [];
    List<String> textLabels = [];
    List<double> confidences = [];
    images = [];
    for(XFile item in imagesFromPicker) {
      // 이미지 피커에서 사용하는 XFile 타입을 ML Kit에서 사용하는 InputImage 형태로 변경
        final List<ImageLabel> labels =
                await imageLabeler.processImage(InputImage.fromFilePath(item.path));
        bool hasBaby = false;
        for (ImageLabel label in labels) {
          // 아기 사진 레이블의 색인(index)이 421번 입니다.
          if (label.index == 421) {
            hasBaby = true;
          }
        }
        hasBabyIndex.add(hasBaby);
    }
    setState(() {
      int i = 0;
      for(XFile item in imagesFromPicker) {
        // XFile 타입을 이미지 뷰어에서 사용하는 Image 타입으로 변환하기 위해서
        // cross_file_image 패키지를 여기서 사용합니다.
        images.add(ImageObj(
            title: hasBabyIndex[i++] ? "Baby" : "No Baby",
            image: Image(image: XFileImage(item))));
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
- ![이미지1](https://reddol18.github.io/dev5min/images/20230406/1.jpg)
- 그 전에 No Human으로 나왔던 사진과 사람이 아닌 사진을 따로 뽑아서 돌려봤습니다.
- 보시다시피 이제는 Baby로 체크해주네요. 정확성이 얼굴인식보다는 더 높아 보입니다.
- 다만 엄마와 함께 찍은 사진은 다른 레이블로 분류되고 있습니다. 
  - 이럴때는 커스텀 모델을 만들거나 객체 감지 기술을 이용해야 할 것으로 보입니다.
- 다음 시간에는 객체 감지 기술에 대해 알아보도록 하겠습니다.   
