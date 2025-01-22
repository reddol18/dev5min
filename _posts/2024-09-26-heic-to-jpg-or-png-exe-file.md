---
layout: post
title: "HEIC 파일을 JPG와 PNG로 변환해주는 프로그램"
description: "터미널에서 간단하게 사용할 수 있습니다."
date: 2024-09-26
author: "김민석"
categories: [Others]
tags: [heic,png,jpg,convert]
---
- 예전에 heic 파일 변환 관련한 코드를 이 블로그에 올린적이 있는데요.
  - [https://reddol18.pe.kr/heic-to-jpg-python](https://reddol18.pe.kr/heic-to-jpg-python)
- 정작 실제로 사용할 일이 생기니까, 실행파일로 만들어야 편하겠더라구요. 그래서 만들어 봤습니다. 소스코드도 함께 공개할게요. 사용방법은 아래와 같습니다.
  - ``h2j.exe --input HEIC_파일이_있는_폴더 --output 저장할_폴더 --mode jpg|png``
  - output을 생략하면 input 폴더와 같은 폴더에 저장됩니다.
  - 변경대상 파일형식은 jpg와 png로 구분하며, 생략하면 jpg로 저장됩니다.
- 파일 다운로드
  - [h2j.exe](https://github.com/reddol18/dev5min/blob/master/snippets/h2j.exe)

- 코드는 아래와 같습니다.

```python
import argparse

from PIL import Image
from pillow_heif import register_heif_opener
import os

def heic_to_jpg(input_folder, output_folder, ext):
    """
    HEIC 파일을 JPG 파일로 변환하는 함수

    Args:
      input_folder: HEIC 파일이 있는 폴더 경로
      output_folder: 변환된 JPG 파일을 저장할 폴더 경로
    """

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.heic'):
                heic_path = os.path.join(root, file)
                jpg_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.' + ext)

                try:
                    with Image.open(heic_path) as img:
                        if ext == "jpg":
                            img.save(jpg_path, 'JPEG')
                        elif ext == "png":
                            img.save(jpg_path, 'PNG')
                        print(f"Converted {heic_path} to {jpg_path}")
                except OSError as e:
                    print(f"Error converting {heic_path}: {e}")

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='', help="input folder")
parser.add_argument('--output', default='', help="output folder")
parser.add_argument('--mode', default='jpg', help="output folder")
args = parser.parse_args()
register_heif_opener()
input_folder = args.input
output_folder = args.input if not args.output else args.output

if args.mode == "jpg" or args.mode == "png":
    heic_to_jpg(input_folder, output_folder, args.mode)
```
