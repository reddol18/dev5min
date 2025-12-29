---
layout: post
title: "Google STT와 Gemini를 이용해서 캘린더에 음성으로 스케쥴 추가하기"
description: "음성을 이용해서 구글 캘린더에 스케쥴을 입력하는 앱을 만들어 봤습니다"
date: 2025-01-22
feature_image: https://reddol18.github.io/dev5min/images/20250122/1.jpeg
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,stt,gemini,calendar]
---
# HeyMySec
- [GitHub Respository](https://github.com/reddol18/heymysec)
- 음성으로 구글 캘린더에 스케쥴을 입력할 수 있는 어플리케이션 입니다.
- Flutter를 이용해서 개발했습니다.
- 안드로이드 버젼에 한해서 실행가능 합니다.
- 구글 로그인, 구글 캘린더 및 Gemini API를 이용합니다.

## 개발하게 된 계기

- 아래 글에 개발하게 된 이유가 설명되어 있습니다.
  - https://blog.naver.com/dolja21/223392231706
- 위와 같은 이유로 자연어 문장으로 이루어진 스케쥴 정보를 구글 캘린더에 정확하게 입력하는 앱을 구상하게 되었습니다.
- 처음에는 자연어 처리를 위한 AI 솔루션이 백엔드 서버로 존재하고, 앱에서는 파이어베이스 Realtime Database에
  요청을 추가하면 백엔드 서버에서 배치작업으로 스케쥴 정보를 인식한 후 이를 다시 앱에 전달하는 방식으로 구현 했었습니다.
- 그런데 이 방식은 관리하는데 들어가는 비용측면, 그리고 여기에 사용한 슬롯필링, NER 등의 AI 모델의 정확성 문제로 인해서
  지금의 방식으로 전환하였습니다.
- 지금은 위에서 구상했던 백엔드 서버가 해야 할 작업을 구글 Gemini(LLM) 서비스에 맡기고 있습니다.

## 실행하기 전에 필요한 것

- 구글 로그인 및 캘린더 API에 접근 가능한 계정 및 google-services.json
  - android/app 폴더에 복사해야 합니다.
- 구글 Gemini API 키 : main.dart 에서 이에 해당하는 부분에 키를 입력해야 합니다

## 실행화면

- 사용법은 간단합니다.
- 먼저 구글 계정으로 로그인 합니다.
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/1.jpeg)
- 권한 지정
  - 마이크 사용을 위한 권한을 허용해야 합니다.
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/2.jpeg) 
- 음성 인식 시작
  - 녹음 버튼을 터치 해서 메시지를 남겨보세요
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/3.jpeg)
  - 멈춤 버튼을 터치 하여 메시지 녹음을 중단하고, 인식된 문장을 확인합니다.
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/4.jpeg)
  - 재녹음 하고 싶으면 다시 녹음 버튼을 터치하면 됩니다.
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/5.jpeg)
  - 그게 아니고 스케쥴 입력을 진행하고 싶으면 보내기 버튼을 터치합니다.
- 정보 확인
  - 스케쥴을 입력하기 전에, 마지막으로 자신이 요청한 정보가 맞는지 확인합니다. 
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/6.jpeg)
  - 구글 캘린더에 들어가보면 스케쥴이 새로 만들어진 것을 확인할 수 있습니다.
  - ![Login](https://reddol18.github.io/dev5min/images/20250122/result.png)

## 사용된 기술

- 구글 로그인 및 캘린더 API
- 구글 Gemini API
- 구글 STT

## 앞으로의 계획

- UI/UX 개선
- STT 인식 정화도 개선
- 카테고리명 띄어쓰기 반영
- 스케쥴 수정 기능 추가