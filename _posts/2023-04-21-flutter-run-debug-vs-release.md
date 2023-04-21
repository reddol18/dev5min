---
layout: post
title: "Flutter 개발시 IDE에서도 Release 모드로 실행하다 낭패본 사연"
description: "Debug Mode가 왜 필요한지 더 나아가 빌더툴의 필요성까지 고민해봅니다"
date: 2023-04-05
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,debug_mode,release_mode]
---
- 제가 개발중인 고양이 집사를 위한 만보기앱에서 발생한 이슈입니다.
   - [냥이야 놀자](https://github.com/reddol18/walk_with_cat)
- 이 앱에는 블루투스 기기를 선택하는 페이지가 있습니다.
- SingleChildScrollView 가 전체 body를 감싸고 있고, 그 안에 LoadingOverlay를 두어서
  배타적으로 동작해야 하는 행위들을 막아버립니다. 이때 사용한 LoadingOverlay를 패키지는 아래
  링크에 해당합니다.
  - [LoadingOverlay](https://github.com/java-james/loading_overlay/)
- LoadingOverlay 내부에는 복잡한 위젯들의 조합으로 구성되어 있습니다.
- 그런데 LoadingOverlay가 나타나야 하는 순간 아래와 같은 화면 깨짐이 발생하게 되었습니다.
  - ![이미지1](https://reddol18.github.io/dev5min/images/20230421/1.jpg)
- 원래 원했던 실행화면은 아래와 같습니다. 
  - ![이미지2](https://reddol18.github.io/dev5min/images/20230421/2.jpg)
- 이러한 화면 깨짐은 "transform layer is constructed with an invalid matrix." 에러와 함께 발생했는데요.
{% include adfit.html %}
- 이슈의 실체를 구체적으로 기술하면, LoadingOverlay가 Stack을 이용해서 CircularProgressIndicator를 만들어 삽입 할 때 
  중앙정렬을 하지 못하는 상황인 것 인데요.
- 원인은 LoadingOverlay 내부의 Stack 구성시에 자식위젯의 높이가 무한대로 지정되어 버려서 인 것으로 파악되었습니다.
- 사실 이 이슈는 디버그모드에서 실행했다면 쉽게 찾아낼 수 있는 버그 였는데요, 왜냐하면 디버그모드에서는 해당상황에 대한
경고메시지와 함께 페이지 구성이 아예 되지 않기 때문입니다. 반면 릴리즈 모드에서는 우스꽝스럽게라도 화면이 만들어 집니다.
당연히 원인이 되는 경고메시지도 출력되지 않습니다. 
- 디버그모드를 무겁다는 이유로 간과한 결과, 상당한 기술적부채가 발생한 것이죠. 아울러 이런 상황을 애당초에 방지하기 위해서라도
빌더툴의 사용해야 겠다는 생각이 점점 드네요. flutterflow 같은 툴이 괜히 있는게 아닐듯 합니다. 이런 툴이 있으면
애당초에 하지 말아야 할 위젯의 조합이나 구성을 막아주지 않을까 싶네요.
  - [flutterflow](https://flutterflow.io/)