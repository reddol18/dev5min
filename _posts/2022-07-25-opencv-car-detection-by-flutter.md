---
layout: post
title: "Method Channel을 이용해서 플러터에서 OpenCV Car Detection 구현하기(1)"
description: "Kotlin Native Code와 Flutter를 연결해서 OPENCV Car Detection을 구현해 봤습니다"
date: 2022-07-25
author: "김민석"
tags: [flutter,opencv,car detection,CascadeClassifier]
---
Flutter에서 Dart 언어 이용해서 OPENCV를 쓸 수 있는 플러그인이 있긴 합니다.

[OPENCV for FLutter](https://pub.dev/packages/opencv)

그런데 제가 구현해 보고 싶은 사진속 자동차 인식은 CascadeClassifier 함수를 사용해야 하거든요.
위 플러그인은 그게 지원이 안되더라구요. 제가 구현하고 싶은건 아래와 같은 내용을 플러터앱으로 시도해 보는 것 이라서요.

[Vehicle Detection and Counting System using OpenCV](https://www.analyticsvidhya.com/blog/2021/12/vehicle-detection-and-counting-system-using-opencv/)

그래서 어쩔수 없이 Kotlin에서 OpenCV를 이용하고 Method Channel을 통해서 그 결과를 받는 쪽으로 구현을 해봤습니다.
먼저 android/app/build.gradle 파일에 Kotlin에서 사용할 OpenCV 의존성을 추가해 주셔야 합니다.

### build.gradle 일부 코드
```
dependencies {
    // .. 원래 있던 것은 놔두시고 아래 내용 추가해주세요. 버젼은 매번 달라질 수 있습니다. ..
    implementation 'com.quickbirdstudios:opencv:4.5.2'
}
```

android/app/src/main에 assets 폴더를 만드시고 car.xml을 저장해두세요. 저는 아래 링크에서 구했어요. 이게 맞는지는 확인을 해봐야 합니다만...
[car.xml](https://gist.github.com/199995/37e1e0af2bf8965e8058a9dfa3285bc6)

### MainActivity.kt 주요 코드
```kotlin
  // import는 알아서 해주세요~
  class MainActivity: FlutterActivity() {
      private val CHANNEL = "패키지 이름/채널 이름";
  
      override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
          super.configureFlutterEngine(flutterEngine)
          OpenCVLoader.initDebug();
          MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler{call, result ->
              // dart 코드에서 Method Channel 호출 할 때 filepath라는 변수에 이미지 절대주소를 넣어서 보냅니다. 
              var filepath: String? = call.argument("filepath")
              if (call.method == "findEdge") {
                  val srcMat: Mat = Imgcodecs.imread(filepath)
                  // 그레이 스케일  
                  val graySrc = Mat()
                  Imgproc.cvtColor(srcMat, graySrc, Imgproc.COLOR_BGR2GRAY)
                  // 가우시안 블러
                  val gausSrc = Mat()
                  Imgproc.GaussianBlur(graySrc, gausSrc, Size(5.0, 5.0), 0.0)
                  // 적절한 단어가 뭔지 모르겠으나, 팽창?
                  val diSrc = Mat()
                  val kernel = Imgproc.getStructuringElement(Imgproc.MORPH_RECT, Size(3.0, 3.0))
                  Imgproc.dilate(gausSrc, diSrc, kernel)
                  // 이 부분도 팽창의 일환인것 같습니다. 모폴로지 연산이라고 하네요.
                  val morSrc = Mat()
                  val kernel2 = Imgproc.getStructuringElement(Imgproc.MORPH_ELLIPSE, Size(2.0,2.0))
                  Imgproc.morphologyEx(diSrc, morSrc, Imgproc.MORPH_CLOSE, kernel2)
                  val rects = MatOfRect()
                  val assetManager = resources.assets
                  // assets에 넣어놓은 car.xml을 불러옵니다.
                  val inputStream = assetManager.open("car.xml")
                  val cdir = getDir("cascade", Context.MODE_PRIVATE)
                  val mfile = File(cdir, "car.xml")
                  mfile.writeBytes(inputStream.readBytes())
                  inputStream.close()
                  // CascadeClassifier 호출합니다
                  val car = CascadeClassifier(mfile.getAbsolutePath())
                  car.detectMultiScale(morSrc, rects, 1.1, 1)
                  var ret: String = ""
                  val pts:Array<Rect> = rects.toArray()
                  // 리턴값 준비
                  for (j in 0 until pts.size) {
                      ret = ret + pts[j].x.toString() + "," +
                              pts[j].y.toString() + "," + pts[j].width.toString() + "," + pts[j].height.toString() + "\n"
                      Log.d("Contour", pts[j].x.toString() +
                              "," + pts[j].y.toString() + "," + pts[j].width.toString() + "," + pts[j].height.toString())
                  }
                  result.success(ret)
              }
          }
      }
  }
```

플러터 쪽 코드는 method_channel과 image_picker 그리고 CustomPainer를 이용해서 구현했습니다.
이건 그렇게 어렵지 않으니 스스로 검색해서 만들어 보세요~

### 테스트 결과
- 시료1
  - ![이미지1](https://reddol18.github.io/dev5min/images/20220725/1/1.jpg)
  - 인터넷에서 구한 네비게이션 화면 입니다. 저는 네비게이션 화면을 이용해서 자동차 디텍팅하는 앱을 생각하고 있어서 이런 유형의 시료가 제일 중요한데 정적 이미지에서는 정확도가 그리 높지 않아 보이네요. 
- 시료2
  - ![이미지2](https://reddol18.github.io/dev5min/images/20220725/1/2.jpg)
  - 제가 직접 찍은건데요, 이것도 그다지 높아보이진 않습니다만 앞에 것보다는 좀 쓸모 있어 보이기도 합니다. 
- 시료3
  - ![이미지3](https://reddol18.github.io/dev5min/images/20220725/1/3.jpg)
  - 위에 있는 링크에서 사용한 시료 인데요. 이건 해당 포스팅에 있는것과 거의 비슷하게 나왔네요. 아마도 촬영각도가 높으면 높을 수록 결과가 좋게 나오는거 아닌가 생각이 듭니다.
- 시료4
  - ![이미지4](https://reddol18.github.io/dev5min/images/20220725/1/4.jpg)
  - 사람은 어떨까? 하는 궁금증이 들어서 광고에 나왔던 CCTV 화면을 한번 시도해봤습니다. 사람용은 아닌듯 하네요.
  
추가적으로 검색을 해본 결과, 정적이미지의 결과 만으로는 쓸만한 값이 나오기 어렵다고 하네요.
동영상에서 일정 간격으로 이미지를 추출해서 변화값을 함께 이용하는 방식을 채택해야 실사용 할 수 있는 결과가 나온다고 합니다. 그것도 시간이 나는데로 구현해 보겠습니다.    
 