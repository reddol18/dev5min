---
layout: post
title: "MediaPipe와 Selenium을 이용해서 웹 CCTV 영상속 고양이 포착하기"
description: "라즈베리파이로 만든 CCTV 웹 모니터링 화면을, 원격 PC에서 MediaPipe와 Selenium을 이용해서 인식하는 방법입니다."
date: 2024-03-19
author: "김민석"
categories: [Computer Vision]
tags: [mediapipe,object detection,selenium,webdriver]
---
- MediaPipe 유용하게 쓰고 있나요? 저는 이것 저것 잘 쓰고 있습니다.
- 물체인식이나 이미지분류, 얼굴인식, 얼굴 표시게 인식 등 정말 잘 쓰고 있어요.
- 그 중에서도 오늘은 물체인식(Object Detection)에 관한 내용입니다. 
- 예전에 Flutter를 이용해서 비슷한 이슈를 다룬적이 있으니 아래 링크 참고해주시면 감사하겠구요.
  - [Flutter 에서 Google ML Kit으로 아기사진 골라내기](https://reddol18.pe.kr/flutter-google-ml-kit-imagelabeling)
- 오늘은 이미 만들어져 있는 DIY CCTV 웹 모니터링 화면을 Selenium Webdriver를 이용해서 캡쳐한 다음
- 캡쳐 화면속에 고양이가 있으면 해당 화면의 사진을 저장하는 프로그램을 만들어 봤습니다.
- 매우 간단하니까 한 번 코드리뷰를 해봐주시면 감사하겠습니다.

- CCTV는 라즈베리파이를 이용해서 자작한 건데요. 이것과 관련한 사연은 아래 블로그 글과 유튜브 영상을 참고해주세요.
  - [📹라즈베리파이로 만든 냥씨티비로 마당냥이 뚱이 염탐하기🐈](https://blog.naver.com/dolja21/223364917052)
  - <iframe width="560" height="315" src="https://www.youtube.com/embed/JS809HC8u_M?si=lllKKAuI7pFWevNM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

{% include adfit.html %}    

- 원격에서 확인할 수 있도록 만들어진 CCTV 모니터링 페이지에 접속하면 이런 화면이 나타납니다.
  - ![화면](https://reddol18.github.io/dev5min/images/20240319/1.png)
  - 위와 같이 고양이가 있으면 캡쳐해서 저장하면 되는거에요.
- 코드는 아래와 같습니다. 아주 간단하죠??

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

options = Options()
# 브라우저 창을 띄우지 않고 처리 합니다.
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# 모니터링 페이지의 URL이 들어갑니다.
driver.get("http://")

# https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/1/efficientdet_lite0.tflite 파일을 다운로드 해서 이름만 바꿨어요.
base_options = python.BaseOptions(model_asset_path='cat.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)
i = 0
while True:
    # 5초마다 수행됩니다.
    sleep(5)
    driver.save_screenshot("screenshot.png")
    image = mp.Image.create_from_file("screenshot.png")
    detection_result = detector.detect(image)
    if len(detection_result.detections) > 0 and \
            detection_result.detections[0].categories is not None:
        for item in detection_result.detections[0].categories:
            # cat이 들어가면 일단 걸립니다. 판독가능한 레이블에 cat이란 단어가 들어가는건 말그대로 cat 밖에 없기 때문에 == 을 써도 무방합니다.
            # 레이블 리스트 : https://storage.googleapis.com/mediapipe-tasks/object_detector/labelmap.txt
            if 'cat' in item.category_name:
                print(item.category_name)
                i = i + 1
                driver.save_screenshot("screenshot_%s.png" % i)
                break

```

- 이렇게 해서 실제로 사용한 사연은 아래 블로그 글과 유튜브 영상을 참고해주세요.
  - [AI를 이용해서 길고양이 쉬는 장면 포착하기](https://blog.naver.com/dolja21/223387650582)
  - <iframe width="560" height="315" src="https://www.youtube.com/embed/jiOM2Y-yzug" title="AI 카메라를 이용해서 길고양이 쉬는 장면 전격 포착! 📸🐈" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>