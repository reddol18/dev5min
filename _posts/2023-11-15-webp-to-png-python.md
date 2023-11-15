---
layout: post
title: "WebP 이미지 PNG로 변환하기"
description: "파이썬에서 WebP 파일을 PNG로 변환하는 방법 입니다"
date: 2023-11-15
author: "김민석"
categories: [Others]
tags: [python,webptopng,webp]
---
- 구글에서 개발한 이미지 파일 저장방식인 .webp 파일, 지난번에 HEIC 파일처럼 사용량이 늘어나고 있는 확장자 입니다.
- webp 역시 파이썬에서 이미지 처리에 이용하려면 지원하지 않는 라이브러리들이 있습니다.
- 그래서 다른 파일형식으로 변환을 해야 하는데요, 이럴때 사용하는 코드 입니다.
- 오늘은 지난번과 다르게 특정 폴더에 있는 모든 webp 파일을 변환하는 함수로 만들었습니다.

{% include adfit.html %}

```python
from PIL import Image

def convert_webp_to_png(img_path):
    exts = ['webp', 'WEBP']
    files = []
    for ext in exts:
        files.extend(
            glob.glob('%s/*.%s' % (img_path, ext)))

    for file in files:
        im = Image.open(file).convert('RGB')
        temp = file.split('.')
        new_name = ".".join(temp[0:-1]) + '.png'
        im.save(new_name, 'png')
```
