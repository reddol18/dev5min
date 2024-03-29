---
layout: post
title: "HEIC(고효율)이미지 JPG로 변환하기"
description: "파이썬에서 HEIC 파일을 JPG로 변환하는 방법 입니다"
date: 2023-11-02
author: "김민석"
categories: [Others]
tags: [python,heictojpg,heic]
---
- 요즘 고효율 사진 저장방식인 .HEIC 파일을 많이 사용하더라구요
- 그런데 이런 파일을 파이썬에서 이미지 처리에 이용하려면 지원하지 않는 라이브러리들이 있습니다.
- 그래서 다른 파일형식으로 변환을 해야 하는데요, 이럴때 사용하는 코드 입니다.
- 이것 저것 다른 방법도 소개되어 있던데, 이게 제일 확실한 것 같아요.

```python
def heic_to_jpg(img_path):
    pillow_heif.register_heif_opener()
    image = Image.open(img_path)
    pathstr, dst = os.path.split(img_path)
    dst = dst.split('.')

    dst = "%s/%s.jpg" % (pathstr, dst[0])
    image.save(dst, format("jpeg"))
    return dst
```
