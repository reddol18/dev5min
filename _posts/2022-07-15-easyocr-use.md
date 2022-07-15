---
layout: post
title: "EASYOCR을 이용해서 글자인식을 해보자"
description: "EASYOCR 처음 사용해보기"
date: 2022-07-15
author: "김민석"
tags: [easyocr,ocr,text,detection]
---
### 이미지에서 글자를 자동으로 인식하려면

- OCR(광학 문자 인식) 기술을 이용해서 이미지상의 글자를 인식해 보고자 합니다.
- 여러가지 라이브러리가 있지만 저는 EasyOCR을 선택했습니다.
  - [https://github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) 
- README만 봐서는 설치가 쉬울것 같은데, OPENCV 관련 의존성 문제가 발생하고 쉽지 않더군요.
- 아나콘다를 이용해서도 해보고, 이것저것 방법을 찾아가면서 해봤지만 하나 해결하면 하나 터지고 하는 식이라 이러다 날이 새겠다 싶었습니다. 
- 그래서 속시원하게 도커로 해결했습니다. 도커파일을 제공하더라구요.
  - [https://github.com/JaidedAI/EasyOCR/blob/master/Dockerfile](https://github.com/JaidedAI/EasyOCR/blob/master/Dockerfile)
  - 빌드 : ``docker build -t easyocr:1 .``
  - 컨테이너 실행 : ``docker run -d --name easyocr -it --rm easyocr:1``
  - docker cp로 사용할 이미지시료 파일과 예제코드를 복사합니다.
  - docker exec로 컨테이너 내부로 접근해서 파이썬 예제코드를 실행하면 됩니다.
  - 실행속도가 빠르지는 않습니다.
  
### 테스트 결과
- 시료1
  - 스마트폰 에뮬레이터에서 돌아가는 게임의 자막입니다.
  - ![이미지1](https://reddol18.github.io/dev5min/images/20220715/1/1.jpg)
  - ```
    [([[62, 401], [382, 401], [382, 433], [62, 433]], 'YMonsters from al', 0.45920909949028654), 
    ([[390, 400], [535, 400], [535, 430], [390, 430]], 'ouer the', 0.6884365613873595), 
    ([[92, 441], [535, 441], [535, 480], [92, 480]], 'world compete uith skill or', 0.521200997045897), 
    ([[92, 486], [294, 486], [294, 516], [92, 516]], 'sueat it out', 0.8942020647336351), 
    ([[302, 486], [488, 486], [488, 516], [302, 516]], 'here in the', 0.42585217998940594), 
    ([[496, 486], [630, 486], [630, 514], [496, 514]], 'Monster', 0.9837152453574232), 
    ([[94, 530], [202, 530], [202, 556], [94, 556]], 'Rrena', 0.9947436302295627),
    ... 
    ```
  - 원하는 결과
    - `Monsters from all over the world compete with skill or sweat it out here in the Monster Arena!`
    - 구글 번역기에 돌리면 나오는 해석
      - `몬스터 아레나에서 전 세계의 몬스터들이 실력을 겨루거나 땀을 흘려보세요!`
  - 산출된 결과
    - `YMonsters from al ouer the world compete uith skill or sueat it out here in the Monster Rrena!`
    - 구글 번역기에 돌리면 나오는 해석 
      - `전 세계의 YMonsters가 기술을 경쟁하거나 여기 Monster Rrena에서 겨루세요!`
- 시료2
  - 제 차의 앞 번호판 입니다.
  - ![이미지2](https://reddol18.github.io/dev5min/images/20220715/1/2.jpg)
  - 숫자부분은 모두 맞게 인식되었는데, 한글 `너` 부분이 `4`로 인식되었습니다.
- 시료3
  - 제 차의 뒷 번호판 입니다.
  - ![이미지3](https://reddol18.github.io/dev5min/images/20220715/1/3.jpg)
  - 숫자부분은 모두 맞게 인식되었는데, 한글 `너` 부분이 `벼`로 인식되었습니다.
- 추가적인 연구과제
  - 폰트를 지정해서 트레이닝 할 수 있는가? 그렇다면 정확도가 개선될것인가?
  - 한글과 숫자가 혼합되어있을 때와 그렇지 않을때의 정확도가 어떻게 될까?
  
   