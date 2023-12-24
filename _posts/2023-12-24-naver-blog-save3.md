---
layout: post
title: "네이버 블로그를 백업해보자 - 3편"
description: "파이썬을 이용해서 깃헙 파일을 업데이트 하고, 구글 서치 콘솔에 URL 인덱싱을 생성시켜 보겠습니다"
date: 2023-12-24
author: "김민석"
categories: [Data and Api]
tags: [naver,naverblog,blog,backup,githubapi,githubblog,google,searchconsole,urlindexing]
---
- 오늘은 이번 네이버 블로그 백업 연재의 마지막편입니다.
    - [네이버 블로그를 백업해보자 - 1편](https://reddol18.pe.kr/naver-blog-save)
    - [네이버 블로그를 백업해보자 - 2편](https://reddol18.pe.kr/naver-blog-save2)
- 블로그 포스팅의 내용이 바뀌었다면 깃헙 레포지토리에도 바뀐 내용을 업데이트 해야겠죠?
    - 2편에서는 커밋을 통해 새로운 파일을 만들었다면, 이번에는 이미 파일이 있는 경우 수정하도록 해보겠습니다.
    - 방법을 간략하게 정리해 보면
        - 먼저 해당 파일이 존재하는지 확인하기 위해서 아래 페이지의 내용을 살펴봅시다.
            - [깃헙파일 정보얻기](https://docs.github.com/ko/rest/repos/contents?apiVersion=2022-11-28#get-repository-content)
            - 위 링크의 호출에서 파일이 존재하면 200 상태로 반응하고 Body에 sha 프로퍼티가 존재합니다.
                ```python
                def get_github_sha(url, token):
                    headers = {
                        "Accept": "application/vnd.github+json",
                        "Authorization": "Bearer %s" % token,
                        "X-GitHub-Api-Version": "2022-11-28"
                    }
                    r = requests.get(url, headers=headers)
                    if r.status_code == 200:
                        return r.json().get("sha")
                    return False
                ```
        - 위에서 얻게된 sha를 지난번까지 사용했던 PUT 호출에 함께 넣어 보내면 Create가 아니라 Update가 되는 것 입니다.
            - [깃헙파일 생성 혹은 수정하기](https://docs.github.com/ko/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents)
            - 파일이 수정되면 자동으로 푸시되게 하기 위해서 branch 프로퍼티를 추가했습니다.            
                ```python
                def put_github_file(url, github_owner, email, content, token):
                    headers = {
                        "Accept": "application/vnd.github+json",
                        "Authorization": "Bearer %s" % token,
                        "X-GitHub-Api-Version": "2022-11-28"
                    }
                    sha = get_github_sha(url, token)
                    if sha == False:
                        ## No sha means No File
                        data = {
                            "message": "commit",
                            "branch": "master",
                            "committer": {
                                "name": github_owner,
                                "email": email
                            },
                            "content": content
                        }
                        requests.put(url, data=json.dumps(data), headers=headers)
                    else:
                        ## Update File
                        data = {
                            "message": "commit",
                            "branch": "master",
                            "sha": sha,
                            "committer": {
                                "name": github_owner,
                                "email": email
                            },
                            "content": content
                        }
                        requests.put(url, data=json.dumps(data), headers=headers)
                ```
        - 그렇게 되면 깃헙페이지 특성상 자동으로 깃헙액션을 수행하고, 빌드 및 배포가 진행됩니다.

{% include adfit.html %}

- 한편 배포된 깃헙 페이지의 URL이 구글검색에 표시될 수 있도록, 서치콘솔에 URL을 등록하는 호출도 해보겠습니다.
    - 그러기 위해서는 구글 개발자 서비스계정을 등록해야합니다.
    - 그리고 나서 인증에 사용되는 사용자를 등록한 후 JSON 파일을 받아야 합니다.
        - [서비스계정 등록 및 설정 방법](https://developers.google.com/search/apis/indexing-api/v3/prereqs?hl=ko)
    - 마지막으로 서치콘솔 URL Indexing을 사용하겠다고 지정해야 아래의 호출을 정상적으로 수행 할 수 있습니다.
        - [URL Indexing Creation API](https://developers.google.com/search/apis/indexing-api/v3/using-api?hl=ko)
        ```python
        def update_google_search_console_url_index(url):
            SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
            ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

            # service_account_file.json is the private key that you created for your service account.
            JSON_KEY_FILE = "file_name.json"

            credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)

            http = credentials.authorize(httplib2.Http())

            content = """{
            \"url\": \"%s\",
            \"type\": \"URL_UPDATED\"
            }""" % url

            response, content = http.request(ENDPOINT, method="POST", body=content)
        ```

- 전체 코드는 아래 링크에 올려두었습니다. 지난번과 비교했을 때 달라진 내용은 아래와 같습니다.
    - 블로그 내용을 가져올 때, 링크 형태이면 MarkDown에서도 링크 형태로 보여지도록 했습니다.
    - 파일명에 표시되는 날짜도 직접 지정할 수 있게 코드를 수정했습니다.
    - [전체코드](https://reddol18.github.io/dev5min/snippets/naver2github.py)
