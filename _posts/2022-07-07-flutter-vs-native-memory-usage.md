---
layout: post
title: "Flutter VS Native 메모리 사용량 비교"
description: "오늘은 프로젝트를 막 생성했을 때. 즉 초기상태의 Hello World 앱만 가지고 Flutter와 Native 앱의 메모리 사용량 비교를 해보았습니다"
date: 2022-07-07
author: "김민석"
tags: [안드로이드,네이티브,flutter,memory,native,플러터,android,메모리,ram]
---
지난번 포스팅에서 Flutter DevTools을 이용하면서 제가 만든 앱의 메모리 사용량이 너무 과도하다는 점을 확인했었습니다. 별거 아닌 테스트용 앱인데도 카카오톡의 사용량을 능가하는게 너무 이상했었죠.

[IntelliJ Idea에서 Flutter App 성능 프로파일링 하기](IntelliJ-Idea-Flutter-App-Profile)

그래서 오늘은 프로젝트를 막 생성했을 때. 즉 초기상태의 Hello World 앱만 가지고 Flutter와 Native 앱의 메모리 사용량 비교를 해보았습니다. 다 읽는데 5분도 안걸려요~

먼저 Flutter 입니다. 이런 앱이에요. 만들면 바로 나오는거...

   ![이미지1](images/20220707/2/1.png)

160MB나 할당되어 있네요. 인스타그램이 300인데.. 지까지것이 뭐라고... ㄷㄷㄷ

   ![이미지1](images/20220707/2/2.png)

이번에는 Native 앱입니다. 이런 앱입니다. 생김새는 다르지만 하는일은 크게 다르지 않은 초기상태의 Hello World 앱이에요.

   ![이미지1](images/20220707/2/3.png)

보이시나요? hello_world_flutter와 hello_word_native(?) 의 메모리 차이가~ 
앱 이름에 'l'자 하나 안들어갔다고 3배 차이가 나고 있네요. (아이고 이놈의 오타)

   ![이미지1](images/20220707/2/4.png)
   
여기저기서 아티클을 검색해서 보니까 어쩔수 없는 차이가 있는것 같네요.
아무래도 flutter로 계속 개발하려면 메모리 최적화에 신경 안쓸수가 없을것 같아요.
할당되는 메모리양(RSS) 줄이는것도 방법이 있다면 찾아보려고 합니다. 
방법이 있다면 공유하도록 하겠습니다.

