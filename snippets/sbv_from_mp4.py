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
    if str(td).find('.') == -1:
        return "%s.000" % str(td)
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