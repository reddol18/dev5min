---
layout: post
title: "동영상의 특정 영역안에서 움직이는 물체가 있는 구간찾기"
description: "Python과 OpenCV를 이용해서 특정 영역안의 움직임이 있는 구간을 찾아내는 루틴을 구현해 보았습니다"
date: 2022-10-18
feature_image: https://reddol18.github.io/dev5min/images/20221019/1/capture.png
author: "김민석"
categories: [Computer Vision]
tags: [opencv,python,cctv,moving,detection]
---
최근에 출시되는 CCTV 관제 프로그램에는 움직임을 감지해서, 해당 구간만 조회할 수 있는 기능이 있습니다.
그런데 구형 CCTV 시스템이거나, 원본 동영상 파일만 가지고 있을 때 이런 기능을 구현하려면 별도의 프로그램이 있어야 합니다.
게다가 특정 영역안에서만 움직임을 필터링하려면 몇 가지 조건을 더 추가해 주어야 하지요.
오늘은 이러한 프로그램의 핵심기술이 될 수 있는 루틴을 공유해 보고자 합니다.
```python
def make_frames_and_trace(self, filename):
    # 비디오 캡쳐할 파일을 지정하고 각종 변수 가져오기
    cpt = cv2.VideoCapture(filename)
    frame_count = int(cpt.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cpt.get(cv2.CAP_PROP_FPS)
    f_width = cpt.get(cv2.CAP_PROP_FRAME_WIDTH)
    f_height = cpt.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # 첫번째 프레임 이미지 얻기
    cpt.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, frame1 = cpt.read()
    on_blank = True
    prev_second = 0.0

    # 1초 단위로 움직임을 체크하려고 합니다
    fps_i = int(fps)

    has_track = None

    for i in range(1, frame_count - 1, fps_i):
        if i + fps < frame_count:
            # 비교할 프레임 이미지 얻기
            cpt.set(cv2.CAP_PROP_POS_FRAMES, i+fps_i)
            _, frame2 = cpt.read()
            preview = frame1
            dst1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            dst2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(dst1, dst2)
            ret_thr, thr = cv2.threshold(
                diff, 30, 255, cv2.THRESH_BINARY)
            dilate = cv2.dilate(thr, self.kernel)
            contours, hierarchy = cv2.findContours(
                dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            has_it = False
            for ct in range(len(contours)):
                # 내가 지정한 영역 rect1과 윤곽선추출된 최소영역인 rect2가 겹치는지를 점검합니다
                area_size = cv2.contourArea(contours[ct])
                min_rect = cv2.minAreaRect(contours[ct])
                rect1 = [self.rect.left(), self.rect.top(),
                         self.rect.right(), self.rect.bottom()]
                rect2 = [min_rect[0][0] / f_width, min_rect[0][1] / f_height,
                         (min_rect[0][0] + min_rect[1][0]) / f_width,
                         (min_rect[0][1] + min_rect[1][1]) / f_height]
                if area_size > 100 and rect2[2] - rect2[0] > 0.01 and rect2[3] - rect2[1] > 0.01 and self.check_overlap(rect1, rect2):
                    x,y,w,h = cv2.boundingRect(contours[ct])
                    # 미리보기 화면 그리기
                    cv2.rectangle(preview, (x,y), (x+w,y+h), (255, 0, 0), 5)
                    has_it = True

            current_second = int((i-1) / fps)

            # 변화가 감지되었나?
            if has_it:
                # 기존에 공백구간이었나?
                if on_blank:
                    on_blank = False
                    prev_second = current_second
                    has_track = TrackItem(filename, current_second, current_second)
                else:
                    prev_second = current_second
                    if has_track is not None:
                        has_track.end = current_second
            else:
                # 10초 이상 감지되지 않았는가? 10초 이상 변화가 없으면 새로운 구간을 만들어도 됩니다
                if current_second - prev_second > 10:
                    on_blank = True
                    if has_track is not None:
                        # 감지된 구간의 길이가 3초 이상일 때만 추가
                        if has_track.end - has_track.start >= 3:
                            self.trackAdded.emit(has_track)
                        has_track = None
            # 감지를 원하는 영역을 미리보기에 그려주기
            cv2.rectangle(preview,
                          (int(self.rect.left() * f_width), int(self.rect.top() * f_height)),
                          (int(self.rect.right() * f_width), int(self.rect.bottom() * f_height)),
                          (0,255,0), 5)
            frame1 = frame2
    if has_track is not None:
        self.trackAdded.emit(has_track)

# arr1과 arr2 구간이 겹치는지 체크
def check_overlap(self, arr1, arr2):
    if arr1[0] == arr1[2] or arr1[1] == arr1[3] or arr2[0] == arr2[2] or arr2[1] == arr2[3]:
        return False
    if arr1[0] > arr2[2] or arr2[0] > arr1[2]:
        return False
    if arr1[1] > arr2[3] or arr2[1] > arr1[3]:
        return False
    return True
```
그리하여 아래와 같은 응용프로그램을 만들어 볼 수 있었는데요, 테스트가 완료되어서 최소한의 안정화 버전이 갖춰지는대로
github에 공개하고 여기에도 공유해 보겠습니다.
![이미지1](https://reddol18.github.io/dev5min/images/20221019/1/capture.png)

