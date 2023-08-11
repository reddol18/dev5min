---
layout: post
title: "IntelliJ Idea Remote Development 사용시 프로젝트 모듈 설정이 안될 때"
description: "Project 설정시에 Modules로 디렉토리 지정을 했는데, 실패하는 경우에 대처법을 설명합니다"
date: 2023-08-11
author: "김민석"
categories: [Others]
tags: [intellij,jetbrains,project_structure,modules,problem]
---
IntelliJ Idea Remote Development 사용하시는 분들이 있을겁니다.
저도 로컬보다 강력한 컴퓨팅 파워가 필요한 환경(예:GPU가 필요한 상황)에서 개발해야 할 때, 이 기능을 이용합니다.
그런데 왜 그런지 모르겠는데 프로젝트가 인식되지 않는거에요.

아래처럼 Projec Structure로 들어가서 Modules에 개발 디렉토리를 추가하더라도
![image](https://github.com/reddol18/dev5min/assets/15623847/92db53e7-6d22-4431-8a90-2b27c0d184b9)

무한 프로그레시브 바만 나오고, 다음번에 다시 Remote Development를 키면 프로젝트가 인식되어 있지 않습니다.
그러다보니 프로젝트내 검색이라던가 최근 파일 보기라던가 인덱싱이 필요한 많은 기능들을 사용할 수 없었어요.

이럴때 아래처럼 해보세요.
1. 먼저 .idea 폴더 내에 [프로젝트명].iml 파일을 만들고 아래와 같이 기입합니다. 파이썬 프로젝트 일 때의 예제에요.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$" />
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```
{% include adfit.html %}
2. 같은 폴더내에 modules.xml을 만들고 아래와 같이 기입합니다.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="ProjectModuleManager">
        <modules>
            <module fileurl="file://$PROJECT_DIR$/.idea/[프로젝트명].iml" filepath="$PROJECT_DIR$/.idea/[프로젝트명].iml" />
        </modules>
    </component>
</project>
```

그럼 다음번에 접속해도 잘 나올겁니다.
        
