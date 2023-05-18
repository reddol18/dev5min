---
layout: post
title: "이미지 파일에 대한 URL 라우팅 속도비교 Node vs Go vs Nginx"
description: "이미지 파일에 대한 URL 라우팅 속도를 비교해 봤습니다"
date: 2023-05-18
author: "김민석"
categories: [Data and Api]
tags: [url_route,node,go,nginx,vue]
---
- 평소에 궁금했던 사항인데요. 정적 이미지 파일을 URL로 나눠서 로딩하는데 걸리는 시간이 언어나 프레임워크 별로
얼마나 차이가 날까였어요.
- 그래서 한 번 시도해 봤습니다. 먼저 Node 코드 입니다.

```javascript
var express = require('express');
var app = express();
var fs = require('fs');

app.get("/image1", function (req, res) {
  var img = fs.readFileSync("./image1.jpg");
  res.set({'Content-Type': 'image/jpeg'});
  res.send(img);
});
app.get("/image2", function (req, res) {
  var img = fs.readFileSync("./image2.jpg");
  res.set({'Content-Type': 'image/jpeg'});
  res.send(img);
});

module.exports = app;
``` 

- JMeter로 동접자 100으로 시도해 봤어요. 그러자 첫번째 파일의 LoadTime은 26ms, 두번째 파일은 8ms 가 나왔습니다.
- 다음은 Go 코드 입니다.

```
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/image1", func(res http.ResponseWriter, req *http.Request) {
		buf, err := ioutil.ReadFile("image1.jpg")
		if err != nil {
			fmt.Printf("error: %s", err.Error())
		}
		res.Header().Set("Content-Type", "image/jpeg")
		res.Write(buf)
	})
	mux.HandleFunc("/image2", func(res http.ResponseWriter, req *http.Request) {
		buf, err := ioutil.ReadFile("image2.jpg")
		if err != nil {
			fmt.Printf("error: %s", err.Error())
		}
		res.Header().Set("Content-Type", "image/jpeg")
		res.Write(buf)
	})
	http.ListenAndServe(":3001", mux)
}
```

- 첫번째 파일은 11ms, 두번째 파일은 6ms가 나왔습니다. 싱글쓰레드인 Node와 그렇지 않은 Go의 성능차이는
어느정도 추측되었는데요.
{% include adfit.html %}
- 그렇다면 Nginx에서 Alias를 이용해서 정적파일을 다른 URL 로딩하면 어떻게 될까요?

```

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    server {
        listen 80;
        location /image1/ {
            alias /images1/;
        }
        location /image2/ {
            alias /images2/;
        }
    }
}
```

- 첫번째 파일이 46ms, 두번째 파일이 17ms가 나왔습니다. 단순비교상으로 Node > Nginx 라니 좀 신선하네요. 
- 아무래도 캐시를 사용하면 결과가 달라질 수 있겠지만, 개인화된 이미지나 동영상을 처리해야 할 때는 캐시가 부적절 할 수 있죠.
- 보너스로 Vue-Router를 이용하면 어떻게 될지 추측해봤습니다. 참고로 Vue는 SPA이고 가상URL을 사용하기 때문에 JMeter로 테스트하기가 어렵더라구요.
- 단순히 이미지 로딩시간만 보면 첫번째 파일이 53ms, 두번째 파일이 45ms가 소요됩니다.
- 다만 컴포넌트화 한 페이지 모두가 로딩되려면 각가 280ms, 150ms 정도가 필요하구요. 

