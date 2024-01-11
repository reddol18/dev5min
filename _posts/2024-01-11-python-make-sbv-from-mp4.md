---
layout: post
title: "동영상 속의 자막으로부터 SBV 파일 추출하기"
description: "파이썬을 이용해서 mp4 파일의 영상에서 타임라인에 따른 SBV 자막을 추출해봅시다"
date: 2024-01-11
author: "김민석"
categories: [ComputerVision]
tags: [python,sbv,youtube,mp4,subtitle,자막,자막추출기,easyocr,ocr]
---
- 저는 블로그 뿐만 아니라 유튜브 채널도 운영하고 있는데요.
  - [유튜브채널 호박이의 망난감랜드](https://www.youtube.com/channel/UC93XE6tpuPX4HeXMDWtIMfA)
- 비록 미미한 구독자수와 형편없는 조회수를 자랑하지만, 그래도 1년 넘게 꾸준히 영상을 업로드하고 있습니다.
- 제가 만드는 컨텐츠들은 주로 영상속에 포함되어 렌더링되는 자막에 크게 의존하고 있는데요. 내용을 이해하는데 이 자막들이 상당히 중요합니다.
- 그런데 구독자들 중에 외국인들이 생기면서 몇 가지 고민거리가 생겼어요. 그 고민거리는 아래와 같습니다.
  - 적어도 영어 자막은 제공하고 싶다.
  - 사용하는 영상제작 프로그램에서 sbv와 같은 시퀀싱 자막 파일을 추출할 수 없다.
  - 매번 유튜브 자막제작툴을 이용하고 있는데, 타임 레인지 맞추는게 너무 불편하다.
- 이런 고민을 해결해보려고 여러가지 프로그램을 찾아봤지만, 뾰족한 대안을 찾기어려웠어요.
- 그래서! 직접 만들어 봤습니다. 전체코드는 아래 링크로 공유할게요.
  - 핵심적으로 사용한 기술은 OCR인데요, 예전에도 한 번 살펴본바 있는 easyocr을 이용했어요.
  - [EASYOCR을 이용해서 글자인식을 해보자](https://reddol18.pe.kr/easyocr-use)

{% include more_front.html %}

```python
import easyocr
from difflib import SequenceMatcher
import cv2
import os
import numpy
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt
from datetime import timedelta

def get_text_from_frame(img_file):
    reader = easyocr.Reader(['ko','en']) # this needs to run only once to load the model into memory
    result = reader.readtext(img_file)
    if len(result) > 0:
        text = ''
        for item in result:
            if len(item) > 1:
                text = "%s %s" % (text, item[1])
        return text
    return ''

def text_diff(t1, t2):
    return SequenceMatcher(None, t1, t2).ratio()

def frame_to_time(fps, frame):
    as_msecond = (frame / fps) * 1000
    td = timedelta(milliseconds=as_msecond)
    return str(td)[:-3]

filepath = '[추출할동영상].mp4'
video = cv2.VideoCapture(filepath)
if not video.isOpened():
    print("Could not Open :", filepath)
    exit(0)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
fps2 = int(fps/2)
before_text = ''
count = 0
before_diff = 0
start_frame = 0
end_frame = 0
data = []
text_count = {}
while(video.isOpened() and count < length):
    ret, image = video.read()
    if(int(video.get(1)) % fps2 == 0): #앞서 불러온 fps 값을 사용하여 0.5초마다 추출
        cv2.imwrite('frame.png', image)
        text = get_text_from_frame('frame.png')
        diff = text_diff(text, before_text)
        if diff < 0.75:
            diff = 0.0
        else:
            diff = 1.0
        if text == '':
            diff = 0.0
        else:
            if text in text_count:
                text_count[text] = text_count[text] + 1
            else:
                text_count[text] = 1
        print("%s, %s" % (diff, text))
        if before_diff == 0.0 and diff == 1.0:
            start_frame = count
        elif before_diff == 1.0 and diff == 0.0:
            end_frame = count
            sorted_text_count = sorted(text_count.items(), key = lambda item: item[1], reverse = True)
            print(sorted_text_count)
            if sorted_text_count[0][0] != '':
                data.append([start_frame, end_frame, sorted_text_count[0][0]])
            text_count = {}
        before_diff = diff
        before_text = text

    print("%d / %d" % (count, length))
    if count < length:
        count = count + 1

if start_frame > end_frame:
    end_frame = count
    sorted_text_count = sorted(text_count.items(), key = lambda item: item[1], reverse = True)
    print(sorted_text_count)
    if sorted_text_count[0][0] != '':
        data.append([start_frame, end_frame, sorted_text_count[0][0]])

video.release()

f = open('[자막파일명].sbv', 'w')
for cap in data:
    start_time = frame_to_time(fps, cap[0])
    end_time = frame_to_time(fps, cap[1])
    f.write("%s,%s\n" % (start_time, end_time))
    f.write("%s\n\n" % cap[2])
f.close()
```

[전체코드 다운로드](https://github.com/reddol18/dev5min/blob/master/snippets/sbv_from_mp4.py)

- 주의사항
  - CUDA를 지원하는 GPU가 없을 경우 CPU만 이용해서 OCR을 수행하기 때문에 매우 느립니다.
  - GPU가 없다면 구글 코랩에서 하드웨어 가속기를 이용해보세요.

{% include more_tail.html %}

- 원래는 번역까지 자동으로 되게하는 코드를 작성하려고 했었습니다만...
- OCR의 품질이 번역 가능할 수 있는 정도까지 결과를 만들어내지는 못합니다.
- 일단 타임레인지를 잡아내는 정도에서 만족해 보려고 하구요.
- 아래 영상은 자동으로 추출한 타임레인지의 SBV 파일에서 영어 번역만 수행해서 올린 것 입니다.
<div style="margin: 0 auto;
  width:424px;
  margin-top: 10px;
  margin-bottom: 10px;">
<iframe width="424" height="238" src="https://www.youtube.com/embed/T4EkWG6MtQE" title="LED로 고양이 장난감 만들기" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>