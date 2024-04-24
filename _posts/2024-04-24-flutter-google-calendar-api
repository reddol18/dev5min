---
layout: post
title: "Flutter에서 google_sign_in 라이브러리 이용해서 캘린더 API 연동하기(1)"
description: "나의 캘린더 리스트를 가져오도록 하겠습니다."
date: 2024-04-24
author: "김민석"
categories: [Flutter and Dart]
tags: [flutter,google_sign_in,google_calendar_api]
---
- 구글 캘린더 많이 사용하시나요? 저는 그것 만큼 직관적인 UI를 가진 스케쥴 앱을 못 찾겠더군요.
- 그래서 몇 년째 애용하고 있는데요. 회사에서는 팀장, 블로그와 유튜버 크리에이터 그리고 육아대디로 활동하다보니 스케쥴 만들고 수정하는 것도 하나의 스케쥴이 되어 버렸어요.
- 저의 이런 고충을 이야기해 본 포스팅이 아래 링크로 있구요.
  - [AI 비서 3종을 비교해 봤습니다](https://blog.naver.com/dolja21/223392231706)
- 위 포스팅에서도 이야기 했지만, 구글 캘린더에 음성인식 기술을 이용해서 이벤트 추가하는게 생각보다 어렵더군요.
- 그래서 제가 직접 만들어보려고 합니다. 오늘은 그 중 첫번째 시간으로 제가 만들어서 관리중인 캘린더 리스트를 뽑아오는 것 까지 해보겠습니다.

{% include adfit.html %}    

- 아래 코드를 보시면 되겠구요. 생각보다 간단합니다. 앱을 시작하면 구글 로그인을 해서 권한 설정을 하고, 모두 완료되면 콘솔에 프린트를 하도록 해놨습니다.

```dart
import 'dart:convert';


import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;


void main() {
 runApp(const MyApp());
}
class MyApp extends StatelessWidget {
 const MyApp({super.key});

 @override
 Widget build(BuildContext context) {
   return MaterialApp(
     title: 'Flutter Demo',
     theme: ThemeData(
       colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
       useMaterial3: true,
     ),
     home: const MyHomePage(title: 'Flutter Demo Home Page'),
   );
 }
}


class MyHomePage extends StatefulWidget {
 const MyHomePage({super.key, required this.title});

 final String title;


 @override
 State<MyHomePage> createState() => _MyHomePageState();
}


class _MyHomePageState extends State<MyHomePage> {
 int _counter = 0;
 List<String> items = [];
 final _googleSignIn = GoogleSignIn(
   scopes: [
     'https://www.googleapis.com/auth/calendar',
   ],
 );
 GoogleSignInAccount? _currentUser;
 late Map<String, dynamic> cals;


 @override
 void initState() {
   super.initState();
   _googleSignIn.onCurrentUserChanged.listen((GoogleSignInAccount? account) {
     setState(() {
       _currentUser = account;
       if (_currentUser != null) {
         _getCalendarList();
       }
     });
   });
   _googleSignIn.signIn().then((GoogleSignInAccount? account) {
     if (account != null) {
       setState(() {
         _currentUser = account;
         _getCalendarList();
       });
     }
   });
 }


 void _getCalendarList() async {
   http.Client client = http.Client();
   var headers = await _currentUser?.authHeaders;
   var resp = await client.get(Uri.parse("https://www.googleapis.com/calendar/v3/users/me/calendarList"), headers: headers);
   cals = jsonDecode(resp.body);
   for(var i=0;i<cals['items'].length;i++) {
     print(cals['items'][i]['summary']);
   }
 }


 void _incrementCounter() {
   setState(() {
     for(var i=0;i<cals['items'].length;i++) {
       print(cals['items'][i]['summary']);
     }
   });
 }


 @override
 Widget build(BuildContext context) {   
   return Scaffold(
     appBar: AppBar(       
       title: Text(widget.title),
     ),
     body: Center(
       child: Column(         
         mainAxisAlignment: MainAxisAlignment.center,
         children: <Widget>[
           const Text(
             'You have pushed the button this many times:',
           ),
           Text(
             '$_counter',
             style: Theme.of(context).textTheme.headlineMedium,
           ),
         ],
       ),
     ),
     floatingActionButton: FloatingActionButton(
       onPressed: _incrementCounter,
       tooltip: 'Increment',
       child: const Icon(Icons.add),
     ),
   );
 }
}
```

- 여기서 주목할 점은 우리가 사용하는 캘린더 상의 이름은 summary 라는 점 이에요.
- package.yaml 파일에 아래 의존성 정의 추가하세요.
    - `google_sign_in: ^6.2.1`
- 이러면 아래처럼 출력이 됩니다.
    - ![이미지1](https://reddol18.github.io/dev5min/images/20240424/1.png)