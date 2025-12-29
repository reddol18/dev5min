---
layout: post
title: "Flutter 에서 많은 이미지 로딩시 메모리 오버플로우 막는 방법"
description: "한번에 대량의 이미지를 표시해야 할 때 발생하는 메모리 문제를 해결해 봅시다"
date: 2023-04-29
feature_image: https://reddol18.github.io/dev5min/images/20230429/1.jpg
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,image,memory,leak,overflow,cachewidth,cacheheight]
---
- GroupGridView 를 이용해서 한 번에 여러개의 사진을 보여주고자 했습니다.
   - [GroupGridView](https://pub.dev/packages/group_grid_view)
- 그런데 이런상황에서 용량이 큰 사진을 한번에 로딩하면 메모리 문제가 발생합니다.
- 이럴때는 아래와 같이 cacheWidth, cacheHeight 속성을 이용합니다.
```dart
    Image.file(File(filepath), 
      cacheWidth: newWidth, 
      cacheHeight: newHeight));
```  
{% include adfit.html %}
- 실제 이미지의 크기와 다르게 위에서 지정한 값으로 로딩하여 레이아웃에 반영하기 
때문에 사용하는 메모리를 현격하게 줄일 수 있습니다.
  - ![이미지1](https://reddol18.github.io/dev5min/images/20230429/1.jpg)