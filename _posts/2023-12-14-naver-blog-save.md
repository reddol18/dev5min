---
layout: post
title: "네이버 블로그를 백업해보자 - 1편"
description: "파이썬을 이용해서 네이버 블로그에 있는 내용과 이미지를 가져와 보겠습니다"
date: 2023-12-13
feature_image: /images/default-thumbnail.jpg
author: "김민석"
categories: [Data and Api]
tags: [naver,naverblog,blog,backup]
---
- 저는 깃헙블로그를 기술블로그로 운영하고 있지만, 일상적인 이야기는 네이버 블로그를 이용하고 있어요.
- 그런데 네이버 블로그는 백업을 하기가 까다롭더군요. 아래의 방법이 있지만 매우 느리고 유연하지 못한 방법이에요.
  - [내 블로그 글 PDF로 백업 받기](https://blog.naver.com/dolja21/223110917870)
- 그래서 오늘부터 네이버 블로그 백업해서 깃헙블로그에 복사하는 방법을 연재해 보고자 합니다.
- 첫번째 시간으로 간단하게 글과 이미지를 가져와 보는 코드를 공유합니다.


```python
import requests
from bs4 import BeautifulSoup

post_url = 'https://blog.naver.com/PostView.naver?blogId={내블로그ID}&logNo={포스트ID}&redirect=Dlog&widgetTypeCall=true&directAccess=true'
html_text = requests.get(post_url).text
soup = BeautifulSoup(html_text, 'html.parser')

for span in soup.select('span, img'):
    has_text = False
    if span.attrs.get("class"):
        for classItem in span.attrs.get("class"):
            if str(classItem).count("se-f") > 0:
                has_text = True
            elif str(classItem).count("se-image-resource") > 0:
                has_text = True
        if has_text:
            print(span)
```

- 위 코드에서 내블로그ID는 자신의 블로그ID를 입력하면 되구요, 포스트ID는 해당 포스트의 ID를 입력하면 됩니다. 
- 예를들어 포스트의 URL이 https://blog.naver.com/dolja21/223110917870 이라고 하면
  - 블로그ID는 dolja21
  - 포스트ID는 223110917870 가 됩니다.
- 코드를 실행해 보면 결과는 아래와 같이 나옵니다.  
```html
<span class="se-fs-fs26 se-ff-nanumbarungothic" id="SE-271e61f1-fa30-11ed-96bc-f715872ef018" style=""><!-- -->내 블로그 글 PDF로 백업 받기<!-- --></span>
<span class="se-fs- se-ff-" id="SE-271e61f2-fa30-11ed-96bc-ff77ccbc6ff1" style="">안녕하세요~ 오늘은 내 블로그에 있는 글 </span>
<span class="se-fs- se-ff-" id="SE-271e61f3-fa30-11ed-96bc-0344045d3f34" style="">백업하는 법을 공유해 볼까 해요.</span>
<span class="se-fs- se-ff-" id="SE-271e61f4-fa30-11ed-96bc-b727f1be4047" style="">네이버 블로그는 PDF 형태로</span>
<span class="se-fs- se-ff-" id="SE-271e61f5-fa30-11ed-96bc-29db5f6a06a8" style="">블로그의 글을 백업 받게 해주는데요.</span>
<img alt="" class="se-image-resource" data-height="569" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMTIx/MDAxNjg0OTMwODg5NDcy.217x4BWCVwyEJ6NHO4FjisvnXM-7C-TWZdmo9NNxppMg.xW7hOm5QIUwEzBJ6A8773ApqOtC-ZIItye6HwgaX_0Ig.PNG.dolja21/SE-b86bbbf7-18eb-43af-a75c-20699064c08a.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMTIx/MDAxNjg0OTMwODg5NDcy.217x4BWCVwyEJ6NHO4FjisvnXM-7C-TWZdmo9NNxppMg.xW7hOm5QIUwEzBJ6A8773ApqOtC-ZIItye6HwgaX_0Ig.PNG.dolja21/SE-b86bbbf7-18eb-43af-a75c-20699064c08a.png?type=w80_blur">
</img>
<span class="se-fs- se-ff-" id="SE-271e8906-fa30-11ed-96bc-fdc795602469" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271e8907-fa30-11ed-96bc-f12f3c68a539" style="">먼저 관리 페이지에서 </span>
<span class="se-fs- se-ff-" id="SE-271e8908-fa30-11ed-96bc-638cbc24ffc0" style="color:#00a84b;"><b>[메뉴-글-동영상 관리]</b></span>
<span class="se-fs- se-ff-" id="SE-271e8909-fa30-11ed-96bc-1b1ad05e6de1" style="">를 클릭</span>
<span class="se-fs- se-ff-" id="SE-271e890a-fa30-11ed-96bc-4b79ecd4bc3c" style="">거기서 좌측 </span>
<span class="se-fs- se-ff-" id="SE-271e890b-fa30-11ed-96bc-eb7db23bd8c8" style="color:#00a84b;"><b>[글 저장]</b></span>
<span class="se-fs- se-ff-" id="SE-271e890c-fa30-11ed-96bc-6d4c65b956f1" style=""> 클릭을 하면</span>
<span class="se-fs- se-ff-" id="SE-271e890d-fa30-11ed-96bc-4123eb26c24b" style="">위와 같은 화면이 나옵니다.</span>
<span class="se-fs- se-ff-" id="SE-271e890e-fa30-11ed-96bc-679cbc592b54" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271e890f-fa30-11ed-96bc-7992fb388d69" style="">​</span>
<img alt="" class="se-image-resource" data-height="845" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMTY1/MDAxNjg0OTI5NjAwMTcy.vw8tmVGhCUxTfDp0XIs-KxhYc_2LvTOqCLHS9tNHDDIg.mS1WDSQzRHip8a-9b6wWIAyk8uz6ukRBEx6x8TbuCOog.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMTY1/MDAxNjg0OTI5NjAwMTcy.vw8tmVGhCUxTfDp0XIs-KxhYc_2LvTOqCLHS9tNHDDIg.mS1WDSQzRHip8a-9b6wWIAyk8uz6ukRBEx6x8TbuCOog.PNG.dolja21/image.png?type=w80_blur">
</img>
<span class="se-fs- se-ff-" id="SE-271eb020-fa30-11ed-96bc-bfec46d803c8" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271eb021-fa30-11ed-96bc-c5772ebcf4dc" style="">10개씩 끊어가면서 선택할 수 있나 보네요</span>
<span class="se-fs- se-ff-" id="SE-271eb022-fa30-11ed-96bc-9b5ab33dadb5" style="">최대 100개까지 할 수 있다고 하니까</span>
<span class="se-fs- se-ff-" id="SE-271eb023-fa30-11ed-96bc-a9e3a3096d5c" style="">쭉~ 체크해서 추가해 봅시다...</span>
<span class="se-fs- se-ff-" id="SE-271eb024-fa30-11ed-96bc-0beec4178f92" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271eb025-fa30-11ed-96bc-9d449aa0c132" style="">​</span>
<img alt="" class="se-image-resource" data-height="428" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjc1/MDAxNjg0OTI5NjQzMDc0.IK9MRfZHkZDBSVsqqdNlzIG_pqDUKx5s4aGBI9gC80Eg.9aB2Nh15vbSsGQbNtfeT6mu8LBSwkJHcW81zbroIK_Ig.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjc1/MDAxNjg0OTI5NjQzMDc0.IK9MRfZHkZDBSVsqqdNlzIG_pqDUKx5s4aGBI9gC80Eg.9aB2Nh15vbSsGQbNtfeT6mu8LBSwkJHcW81zbroIK_Ig.PNG.dolja21/image.png?type=w80_blur">
</img>
<span class="se-fs- se-ff-" id="SE-271eb026-fa30-11ed-96bc-fdf3b925463a" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271ed737-fa30-11ed-96bc-fbcacaf4b263" style="">엥! 하고 보니 500MB 넘어버렸네요.</span>
<span class="se-fs- se-ff-" id="SE-271ed738-fa30-11ed-96bc-f354a3113514" style="">어쩔 수 없이 몇 개 지워서 용량을 맞춰줍니다.</span>
<img alt="" class="se-image-resource" data-height="432" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjYg/MDAxNjg0OTI5ODg2NzU5.3BXeBk1pkWhGnQgRyV5u_pgBN7mw90X4pGgMMNAB20Qg.5rHBicO91PXhre_UpPDtU_ps9UOQXgUWNuFFSChkflkg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjYg/MDAxNjg0OTI5ODg2NzU5.3BXeBk1pkWhGnQgRyV5u_pgBN7mw90X4pGgMMNAB20Qg.5rHBicO91PXhre_UpPDtU_ps9UOQXgUWNuFFSChkflkg.PNG.dolja21/image.png?type=w80_blur">
</img>
<span class="se-fs- se-ff-" id="SE-271ed739-fa30-11ed-96bc-797189129099" style="">파일 제목까지 지정해서 </span>
<span class="se-fs- se-ff-" id="SE-271ed73a-fa30-11ed-96bc-d9636da97eb1" style="color:#ffffff;background-color:#00a84b;"><b>[만들기]</b></span>
<span class="se-fs- se-ff-" id="SE-271ed73b-fa30-11ed-96bc-2b7f15a0e16f" style=""> 버튼을 클릭!</span>
<span class="se-fs- se-ff-" id="SE-271ed73c-fa30-11ed-96bc-9b76263b0446" style="">그러자 저장 목록에 만들어지고 있는</span>
<span class="se-fs- se-ff-" id="SE-271ed73d-fa30-11ed-96bc-23507015ac76" style="">PDF가 1개 뜹니다. 바로 만들어지는 게 아니군요.</span>
<img alt="" class="se-image-resource" data-height="734" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfNTcg/MDAxNjg0OTI5OTQ3MzQ2.9LGudydN-nOGCM4VeY-flb_0VnGBOxc6zZ1fT9Qyo0gg.0y9kYAfjIe2L_o_zZRmr0ajbzsAWPvThf-8n_eGPVREg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfNTcg/MDAxNjg0OTI5OTQ3MzQ2.9LGudydN-nOGCM4VeY-flb_0VnGBOxc6zZ1fT9Qyo0gg.0y9kYAfjIe2L_o_zZRmr0ajbzsAWPvThf-8n_eGPVREg.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271ed73e-fa30-11ed-96bc-3b8a4cadf8df" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271ed73f-fa30-11ed-96bc-33c94fa61b1d" style="">이런 식으로 계속 추가해서 110개까지</span>
<span class="se-fs- se-ff-" id="SE-271efe50-fa30-11ed-96bc-a9590b9abe30" style="">PDF로 백업할 수 있게 되었고요.</span>
<span class="se-fs- se-ff-" id="SE-271efe51-fa30-11ed-96bc-d580699d9f81" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271efe52-fa30-11ed-96bc-6b9cdbc6ac2e" style="">​</span>
<img alt="" class="se-image-resource" data-height="666" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjQ4/MDAxNjg0OTI5OTcyNTc5.gKXKMDwrFSt9LnjqNdPLnSON4kEPiVonzVGYuf15M3Mg.0_ZmSSrKx-6vvCUQxd1riZdRPzPcC2L5GTy7ovjT3Psg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjQ4/MDAxNjg0OTI5OTcyNTc5.gKXKMDwrFSt9LnjqNdPLnSON4kEPiVonzVGYuf15M3Mg.0_ZmSSrKx-6vvCUQxd1riZdRPzPcC2L5GTy7ovjT3Psg.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271efe53-fa30-11ed-96bc-0be54f4b969f" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271efe54-fa30-11ed-96bc-2f000004d9bb" style="">그런데 중간에 실수로 만들다가 취소한 게</span>
<span class="se-fs- se-ff-" id="SE-271efe55-fa30-11ed-96bc-e5258f3c9d99" style="">있었거든요?</span>
<span class="se-fs- se-ff-" id="SE-271f2566-fa30-11ed-96bc-57ca5d07aeb6" style="">그랬더니 아직 1.2GB 안 만들었는데도</span>
<span class="se-fs- se-ff-" id="SE-271f2567-fa30-11ed-96bc-11bdbdcb0700" style="">아래와 같은 경고 창이 뜨면서</span>
<span class="se-fs- se-ff-" id="SE-271f2568-fa30-11ed-96bc-03504cb22b96" style="">더 못 만든다고 합니다. ㅠㅠ</span>
<span class="se-fs- se-ff-" id="SE-271f2569-fa30-11ed-96bc-014e87ba0ace" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f256a-fa30-11ed-96bc-ef499117afc5" style="">​</span>
<img alt="" class="se-image-resource" data-height="320" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjU1/MDAxNjg0OTI5ODUyOTA1.uELAkHLmB8hbeQDU-KHNXaEHbJJ99fHjPErAaEr8uQog.Xmmav4Zb3iaaol07N0UPKQFtkBg86TZSRyCwqxc86zsg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjU1/MDAxNjg0OTI5ODUyOTA1.uELAkHLmB8hbeQDU-KHNXaEHbJJ99fHjPErAaEr8uQog.Xmmav4Zb3iaaol07N0UPKQFtkBg86TZSRyCwqxc86zsg.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271f256b-fa30-11ed-96bc-37f666aa2c9f" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f256c-fa30-11ed-96bc-35387927453b" style="">이미 완성된 거라도 다운로드해 보겠습니다.</span>
<span class="se-fs- se-ff-" id="SE-271f256d-fa30-11ed-96bc-4186daf47fbc" style="">과연 어떻게 만들어질까요??</span>
<span class="se-fs- se-ff-" id="SE-271f256e-fa30-11ed-96bc-278b2f87edf2" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f256f-fa30-11ed-96bc-4b094a1489bd" style="">​</span>
<img alt="" class="se-image-resource" data-height="738" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjEz/MDAxNjg0OTMwMDExMTI1.mgmPbXaoyQWQ-LFwPuY94psL5W_RAeT2oJvcr0kWZz0g.pzv5lVsH1iwxrQR5D6gwcmiIWmCRFBUedY1xWX-r0mMg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjEz/MDAxNjg0OTMwMDExMTI1.mgmPbXaoyQWQ-LFwPuY94psL5W_RAeT2oJvcr0kWZz0g.pzv5lVsH1iwxrQR5D6gwcmiIWmCRFBUedY1xWX-r0mMg.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271f4c80-fa30-11ed-96bc-55f45f0ceb32" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f4c81-fa30-11ed-96bc-7f5ad3a4a2fc" style="">만들어진 PDF는 이런 식입니다.</span>
<span class="se-fs- se-ff-" id="SE-271f4c82-fa30-11ed-96bc-c74ecc067b4d" style="">스타일이 블로그와 똑같이 반영되지 않고요</span>
<span class="se-fs- se-ff-" id="SE-271f4c83-fa30-11ed-96bc-db1a31e8c372" style="">정렬도 안되는듯합니다.</span>
<span class="se-fs- se-ff-" id="SE-271f4c84-fa30-11ed-96bc-c9d29b42717d" style="">동영상은 당연히 안 나오고요.</span>
<span class="se-fs- se-ff-" id="SE-271f4c85-fa30-11ed-96bc-ebe918b8e564" style="">썸네일로도 안 나와요.</span>
<span class="se-fs- se-ff-" id="SE-271f4c86-fa30-11ed-96bc-dda57657e726" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f4c87-fa30-11ed-96bc-6fb982464769" style="">​</span>
<img alt="" class="se-image-resource" data-height="673" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjc1/MDAxNjg0OTMwMjk1MzMy.MxDUTqumhs3Jdk68xLSwlctGoJ8olJ52urRKNaEGXJMg.Fq59PbcqwKO_D-bhW9t5r_qO18GowFSsoex_uE4nIpwg.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjc1/MDAxNjg0OTMwMjk1MzMy.MxDUTqumhs3Jdk68xLSwlctGoJ8olJ52urRKNaEGXJMg.Fq59PbcqwKO_D-bhW9t5r_qO18GowFSsoex_uE4nIpwg.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271f4c88-fa30-11ed-96bc-d5a4053da33f" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f4c89-fa30-11ed-96bc-41551f4ba3c0" style="">그런데 신기하게도</span>
<span class="se-fs- se-ff-" id="SE-271f739a-fa30-11ed-96bc-b553cb24cb6b" style="">시간이 좀 지난 다음에 아까 저장 페이지로</span>
<span class="se-fs- se-ff-" id="SE-271f739b-fa30-11ed-96bc-971709d7db2c" style="">다시 가보니까, 용량이 줄어들어 있고</span>
<span class="se-fs- se-ff-" id="SE-271f739c-fa30-11ed-96bc-e91cca1fc07a" style="">더 추가할 수가 있었어요.</span>
<span class="se-fs- se-ff-" id="SE-271f739d-fa30-11ed-96bc-a530d3c861ab" style="">그런데! 백업은 이렇게 받는다 치지만</span>
<span class="se-fs- se-ff-" id="SE-271f739e-fa30-11ed-96bc-235faf6e2120" style="">복구는 어떻게 하죠???</span>
<span class="se-fs- se-ff-" id="SE-271f739f-fa30-11ed-96bc-33de0b64c3e8" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f73a0-fa30-11ed-96bc-db8cba914246" style=""><a class="se-link" href="https://www.sedaily.com/NewsView/26CDWOIA4H" target="_blank">https://www.sedaily.com/NewsView/26CDWOIA4H</a></span>
<span class="se-fs- se-ff-" id="SE-271f99b1-fa30-11ed-96bc-dd04877a62cb" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f99b2-fa30-11ed-96bc-951cec50d3b9" style="">네이버에서 이런 일 벌어지면 어떡해야 하죠?</span>
<span class="se-fs- se-ff-" id="SE-271f99b3-fa30-11ed-96bc-717350db3d32" style="">PDF 파일 보면서 새로 다시 써??</span>
<span class="se-fs- se-ff-" id="SE-271f99b4-fa30-11ed-96bc-05246710bc69" style="">네이버 블로그 고객센터에서 오피셜로</span>
<span class="se-fs- se-ff-" id="SE-271f99b5-fa30-11ed-96bc-49ffc1a2c28c" style="">알려주네요...</span>
<span class="se-fs- se-ff-" id="SE-271f99b6-fa30-11ed-96bc-493136557a84" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271f99b7-fa30-11ed-96bc-cbe7168d41c8" style="">​</span>
<img alt="" class="se-image-resource" data-height="256" data-lazy-src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjE3/MDAxNjg0OTMwNTM3NTgy.y_OeLKUalQfUsKWz2Uo_YipA8q8tKaG9YU4dldoQzOIg.7DKkuxkWbh1RlhsWLsXpbxCV7f8WJmubwTQsMEErAK4g.PNG.dolja21/image.png?type=w773" data-width="693" src="https://postfiles.pstatic.net/MjAyMzA1MjRfMjE3/MDAxNjg0OTMwNTM3NTgy.y_OeLKUalQfUsKWz2Uo_YipA8q8tKaG9YU4dldoQzOIg.7DKkuxkWbh1RlhsWLsXpbxCV7f8WJmubwTQsMEErAK4g.PNG.dolja21/image.png?type=w80_blur"/>
<span class="se-fs- se-ff-" id="SE-271f99b8-fa30-11ed-96bc-3307bfc504e5" style="">​</span>
<span class="se-fs- se-ff- se-decoration-unset" id="SE-271fc0c9-fa30-11ed-96bc-c3ad06c5f127" style="color:#000000;background-color:#ffd300;"><b>백업만 가능하지 복원은 불가능...</b></span>
<span class="se-fs- se-ff-" id="SE-271fc0ca-fa30-11ed-96bc-430052911247" style="">물론 PDF 파일이 아닌 방식으로 백업을 해주는</span>
<span class="se-fs- se-ff-" id="SE-271fc0cb-fa30-11ed-96bc-bdd6035145cb" style="">사설 프로그램들도 있긴 합니다.</span>
<span class="se-fs- se-ff-" id="SE-271fc0cc-fa30-11ed-96bc-87ccd5bc85b8" style="">그러나 자동으로 글을 써주는 시스템이</span>
<span class="se-fs- se-ff-" id="SE-271fc0cd-fa30-11ed-96bc-cd145a1a3e7b" style="">네이버에는 없기 때문에</span>
<span class="se-fs- se-ff-" id="SE-271fc0ce-fa30-11ed-96bc-11b36f5ddf2f" style="">사실상 복원은 어떤 방법으로도 불가능합니다.</span>
<span class="se-fs- se-ff-" id="SE-271fc0cf-fa30-11ed-96bc-43c0ef3ae725" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271fc0d0-fa30-11ed-96bc-45bff40e8618" style=""><a class="se-link" href="https://blog.naver.com/blogpeople/221893702144" target="_blank">https://blog.naver.com/blogpeople/221893702144</a></span>
<span class="se-fs- se-ff-" id="SE-271fc0d1-fa30-11ed-96bc-cd600989112c" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271fc0d2-fa30-11ed-96bc-af5dabbdd8ba" style="">예전에는 API를 이용해서 </span>
<span class="se-fs- se-ff-" id="SE-271fe7e3-fa30-11ed-96bc-cfb79f1291a0" style="">글쓰기가 가능했다고 하는데</span>
<span class="se-fs- se-ff-" id="SE-271fe7e4-fa30-11ed-96bc-17280f13607d" style="">지금은 종료된 기능이라고 해요.</span>
<span class="se-fs- se-ff-" id="SE-271fe7e5-fa30-11ed-96bc-3f4ad6e94201" style="">백업을 하려면 사람이 직접 글 쓰는 건 어렵고</span>
<span class="se-fs- se-ff-" id="SE-271fe7e6-fa30-11ed-96bc-55426668ce9f" style="">컴퓨터가 자동으로 써줘야 하는데...</span>
<span class="se-fs- se-ff-" id="SE-271fe7e7-fa30-11ed-96bc-09704bbf5363" style="">그게 안된다는 거예요.</span>
<span class="se-fs- se-ff-" id="SE-271fe7e8-fa30-11ed-96bc-277222900e05" style="">그래도 저는 일단 216개의 글을 모두</span>
<span class="se-fs- se-ff-" id="SE-271fe7e9-fa30-11ed-96bc-1d060b0fcc8c" style="">PDF로 백업은 받아놨어요.</span>
<span class="se-fs- se-ff-" id="SE-271fe7ea-fa30-11ed-96bc-01442b3e75f1" style="">방법이 까다롭지만 여러분도 한번 해보세요~</span>
<span class="se-fs- se-ff-" id="SE-271fe7eb-fa30-11ed-96bc-031601695b9e" style="">​</span>
<span class="se-fs- se-ff-" id="SE-271fe7ec-fa30-11ed-96bc-a58b3124634e" style="">이상 직업병 때문에 백업/복원 방법을</span>
<span class="se-fs- se-ff-" id="SE-271fe7ed-fa30-11ed-96bc-c92c0ff3b721" style="">알아본 어흥아빠호박집사 였습니다~</span>
<span class="se-fs- se-ff-" id="SE-271fe7ee-fa30-11ed-96bc-1b5d4f1b3fab" style="">​</span>
<span class="se-fs- se-ff-" id="SE-27200eff-fa30-11ed-96bc-3b4127ff804b" style="">​</span>
<img alt="" class="se-image-resource" src="https://storep-phinf.pstatic.net/cafe_001/original_5.gif?type=pa50_50"/>
<span class="se-fs-fs15 se-ff-nanumdasisijaghae se-style-unset" id="SE-27200f00-fa30-11ed-96bc-7dd274f932bf" style="color:#ff9300;background-color:#ffffff;">공감과 선플은 큰 힘이 됩니다~</span>
<span class="se-fs-fs15 se-ff-nanumdasisijaghae se-style-unset" id="SE-27200f01-fa30-11ed-96bc-75d82e93ba9b" style="color:#ff9300;background-color:#ffffff;">이웃님이 공감 눌러주시면</span>
<span class="se-fs-fs15 se-ff-nanumdasisijaghae se-style-unset" id="SE-27200f02-fa30-11ed-96bc-31e9903c2647" style="color:#ff9300;background-color:#ffffff;">공감+광클로 보답해요~</span>
<span class="se-fs-fs15 se-ff-nanumdasisijaghae se-style-unset" id="SE-27200f03-fa30-11ed-96bc-ab459fa64321" style="color:#ff9300;">​</span>
<span class="se-fs-fs15 se-ff-nanumdasisijaghae se-style-unset" id="SE-27200f04-fa30-11ed-96bc-0121d08a2fe8" style="color:#ff9300;">​</span>
```
- 다음시간에는 가져온 내용에서 이미지를 다운로드 하고, 깃헙API를 이용해서 파일을 추가하는 내용을 올려보도록 하겠습니다.