---
layout: post
title: "파이썬에서 이미지 파일의 진짜 속성을 알아보자"
description: "확장자에 속지 마세요, 이미지의 진짜 속성은 파일내용에 있습니다."
date: 2024-01-30
author: "김민석"
categories: [Others]
tags: [python,mimetypes,imghdr,python-magic]
---
- 이미지를 이용하는 서비스를 운영하는 경우 정말 다양한 확장자의 이미지 파일들을 다루게 되는데요.
- 대표적인 이미지 타입인 PNG,JPG는 물론이거니와 최근에 많이 사용하는 HEIC나 WEBP등의 파일도 처리해야 하는 경우가 있습니다.
- 이와 관련해서는 제 블로그에 포스팅을 남긴바가 있죠.
  - [HEIC(고효율)이미지 JPG로 변환하기](https://reddol18.pe.kr/heic-to-jpg-python)
  - [WebP 이미지 PNG로 변환하기 ](https://reddol18.pe.kr/webp-to-png-python)
- 그런데 간혹가다가 확장자는 PNG인데 파일의 진짜 속성은 그렇지 않은 파일이 업로드되는 경우도 경험하게 됩니다.
- 즉, 파일의 확장자만 믿고 해당 파일타입으로 이미지를 로딩하면 문제가 발생할 수 있다는 의미입니다.
- 이럴때 파이썬에서 사용할 수 있는 방법들이 몇 가지 있는데요. 먼저 내장된 패키지인 mimetypes를 생각해 볼 수 있을겁니다.
  - 아래 이미지를 heic, jfif, webp, jpg, png 형태로 각각 저장하여 mimetypes를 이용해서 파일속성을 판단해 보겠습니다.
    - ![사용이미지](https://reddol18.github.io/dev5min/images/20240130/5.png)
    ```python
        import mimetypes
  
        print("\n\nUse Mimetypes\n")
        print(mimetypes.guess_type("./test/imgs/1.heic"))
        print(mimetypes.guess_type("./test/imgs/2.jfif"))
        print(mimetypes.guess_type("./test/imgs/3.webp"))
        print(mimetypes.guess_type("./test/imgs/4.jpg"))
        print(mimetypes.guess_type("./test/imgs/5.png"))
    ```
  - 이러면 결과는 아래처럼 나타납니다.
    ```
    Use Mimetypes

    (None, None)
    (None, None)
    (None, None)
    ('image/jpeg', None)
    ('image/png', None)
    ```
    - 결과를 보면 PNG, JPG를 제외하고는 속성 파악을 못하는 것으로 확인되는데요.
    - 그렇다면 heic, jfif, webp를 png로 확장자만 바꾸고 같은 소스를 실행하면 어떻게 될까요?
    ```
    Use Mimetypes

    ('image/png', None)
    ('image/png', None)
    ('image/png', None)
    ('image/jpeg', None)
    ('image/png', None)
    ```
    - 세 경우 모두 확장자인 PNG로 인식하게 됩니다. 즉, 진짜 이미지의 파일속성을 알고 싶다면 mimetypes는 쓰지 않는게 좋아요.

{% include adfit.html %}    

- 다음으로 imghdr을 이용해서 확인해 봅시다.
    - 같은 이미지를 사용했구요, png로 바꾼 세개의 파일도 그대로 사용합니다. 아래처럼 소스코드를 작성해보았습니다.
    ```python
        import imghdr
    
        print("\n\nUse Imghdr\n")
        print(imghdr.what("./test/imgs/1.png")) #원래 heic
        print(imghdr.what("./test/imgs/2.png")) #원래 jfif
        print(imghdr.what("./test/imgs/3.png")) #원래 webp
        print(imghdr.what("./test/imgs/4.jpg"))
        print(imghdr.what("./test/imgs/5.png"))
    ```
    - 그리고 결과는 다음과 같습니다.
    ```
    Use Imghdr

    None
    jpeg
    webp
    jpeg
    png
    ```
    - imghdr은 heic는 파악하지 못하는 것으로 보이구요, jfif는 JPG의 변형판 같은거라 같은 JPG로 나옵니다.
- heic를 파악하지 못하는 아쉬움으로 인해 다른 대안을 찾아봐야 겠군요. python-magic을 사용해 봅시다.
    - 이번에도 역시 같은 이미지를 사용했습니다.
    ```python
        import magic
        
        print("Use Magic\n")
        print(magic.from_file("./test/imgs/1.png", mime=True)) #원래 heic
        print(magic.from_file("./test/imgs/2.png", mime=True)) #원래 jfif
        print(magic.from_file("./test/imgs/3.png", mime=True)) #원래 webp
        print(magic.from_file("./test/imgs/4.jpg", mime=True))
        print(magic.from_file("./test/imgs/5.png", mime=True))
    ```
    - 결과를 보면 다음과 같습니다.
    ```
    Use Magic

    image/heic
    image/jpeg
    image/webp
    image/jpeg
    image/png
    ```
    - 다행이군요, python-magic은 heic까지 판별해냅니다.

