# AI 에이전트와 함께하는 실시간 서비스 모니터링

> "지금 서비스 잘 돌아가고 있나요?"라는 질문에 답하는 데 걸리는 시간을 줄이는 방법

---

## 들어가며

서비스를 운영하다 보면 종종 이런 순간이 온다.

> "지금 이 시각 몇 명이나 쓰고 있지?"  
> "혹시 에러 나고 있는 건 아니겠지?"  
> "저 사용자들은 지금 무슨 상황인데 갑자기 접속자가 많아졌지?"

예전에는 이 질문 하나를 풀려면 GA 대시보드를 열고, Cloud Run 콘솔에 들어가고, DB 클라이언트를 실행하고, 로그를 grep하는 과정을 각각 따로 거쳐야 했다. 오늘은 AI 에이전트가 이 과정을 어떻게 바꿨는지 실제 사례를 통해 공유한다.

---

## 환경 구성

```
사용자 (자연어 질문)
    ↓
Claude Code (AI 에이전트)
    ↓
┌──────────────────────────────────────┐
│  PostgreSQL (Cloud SQL)              │
│  Cloud Run 로그 (gcloud logging)     │
│  GitHub Issues                       │
└──────────────────────────────────────┘
```

- **런타임**: Node.js + pg 드라이버로 DB 직접 쿼리
- **로그**: `gcloud logging read`로 Cloud Run 로그 조회
- **에이전트**: Claude Code (CLI)

---

## 시나리오 1 — 특정 콘텐츠를 보고 있는 사용자 파악

GA에서 특정 페이지에 약 20명이 동시 접속 중인 것을 확인했다. URL 경로에 콘텐츠 ID가 포함되어 있었고, 자연어로 물었다.

```
"지금 이 콘텐츠 보고 있는 사용자들 어느 그룹이야?"
```

에이전트는 다음 순서로 동작했다.

**1단계 — 최근 활동 사용자 그룹 집계**

콘텐츠 ID를 기준으로 최근 3시간 내 활동 기록을 조회해 어느 그룹에서 접속 중인지 파악했다.

```sql
SELECT group_name, status, COUNT(*) AS count
FROM activity_log
JOIN user_profiles ON activity_log.uid = user_profiles.uid
JOIN groups ON user_profiles.group_id = groups.id
WHERE content_id = $1
  AND updated_at >= NOW() - INTERVAL '3 hours'
GROUP BY group_name, status
ORDER BY count DESC
```

결과: 특정 그룹 사용자 15명이 현재 콘텐츠를 작성 중.

**2단계 — 왜 지금 이 콘텐츠를 보는지 맥락 파악**

해당 그룹의 이번 주 일정을 조회해 접속 급증의 맥락을 파악했다.

```sql
SELECT title, start_date
FROM group_schedules
WHERE group_id = $1
  AND start_date BETWEEN $2 AND $3
ORDER BY start_date
```

결과: 해당 그룹이 4월 22일~27일 시험 기간이었고, 오늘(4/29)이 시험 종료 다음 날이었음. 목요일은 그룹 자체 휴일, 금요일은 노동절로 연속 휴일. **시험 끝나고 연휴 전에 몰아서 콘텐츠를 작업하러 들어온 것.**

GA 숫자만 봤을 때는 "갑자기 왜 접속이 많지?"였는데, 그룹 일정과 교차하니 맥락이 바로 잡혔다.

![시나리오1 흐름도](/assets/images/blog-scenario1.png)

---

## 시나리오 2 — 로그에서 이상 신호 포착

"서비스 잘 돌아가고 있나?" 확인 요청에 에이전트가 Cloud Run 로그를 조회했다.

```bash
gcloud logging read \
  'resource.type="cloud_run_revision"
   resource.labels.service_name="api-prd"
   httpRequest.status>=400' \
  --limit 20 --format=json
```

결과: **동일한 3개의 콘텐츠 ID에 대해 특정 API 엔드포인트에서 404가 반복** 발생 중.

```
2026-04-29T00:06:32Z  404  /api/content/d8288d91-...
2026-04-29T00:04:42Z  404  /api/content/d8288d91-...
2026-04-29T00:03:56Z  404  /api/content/d8288d91-...
...
```

에이전트는 여기서 멈추지 않고 코드와 DB를 함께 교차 분석했다.

**코드 분석**

```js
// 콘텐츠 상세 페이지
if (data.hasRecord) {
  const res = await apiFetch(`/api/content/${id}`);
  // ...
}
```

`hasRecord=false`이면 호출 자체를 안 하는 구조. **404가 발생한다는 건 API가 "기록 있음"을 반환했는데 실제 레코드는 없는 케이스.**

**DB 교차 확인**

콘텐츠 상태 플래그와 실제 레코드 존재 여부를 조인해서 불일치 건수를 확인했다.

```sql
SELECT COUNT(*) AS inconsistent_count
FROM content_items c
LEFT JOIN activity_records r
  ON r.content_id = c.id AND r.uid = $1
WHERE c.id = $2
  AND c.status IN ('in_progress', 'submitted')
  AND r.id IS NULL
```

결과: 0건. 데이터 정합성 문제는 아님.

**최종 판단**

실사용자 경험에 직접적인 영향은 없으나, API 단건 조회의 상태 플래그 판단 로직에서 불일치 케이스가 존재함. 재현 조건은 추가 분석 필요.

에이전트가 바로 GitHub 이슈를 등록했다.

```
[BE] 콘텐츠 단건 조회 후 기록 조회 404 반복 발생
- 현상: 동일 콘텐츠 ID에 대해 404 30건 이상 반복
- 영향: 사용자 경험 영향 없음
- 완료 조건: 재현 경로 특정 및 불일치 원인 수정
```

![시나리오2 흐름도](/assets/images/blog-scenario2.png)

---

## 달라진 점

| 항목 | 이전 | 이후 |
|------|------|------|
| 접속자 맥락 파악 | GA + 별도 DB 쿼리 + 일정 수동 대조 | 자연어 질문 1개 |
| 로그 이상 감지 | 콘솔 직접 확인 | 에이전트가 자동 교차 분석 |
| 이슈 등록 | 분석 후 직접 작성 | 분석 결과 기반 자동 초안 |
| 컨텍스트 전환 | 도구 4~5개 | 대화창 1개 |

핵심은 **도구를 덜 쓰는 게 아니라, 도구 전환 비용이 없어진다**는 것이다. GA → DB → 로그 → 코드 → 이슈 트래커를 오가는 맥락 전환이 사라지고, 질문 하나로 연결된 흐름이 만들어진다.

---

## 주의할 점

이 워크플로우를 구성하면서 몇 가지 설계 원칙이 중요했다.

**1. DB 접근 도구를 명시적으로 제한한다**  
에이전트가 사용할 수 있는 DB 도구가 여러 개이면 자동으로 잘못된 걸 선택하는 경우가 생긴다. 지침 문서에 사용할 DB와 접근 방식을 명시적으로 지정했다.

```markdown
## DB 접근
반드시 PostgreSQL만 사용.
다른 DB 클라이언트 도구 절대 사용 금지.
Proxy가 꺼져 있으면 직접 백그라운드로 실행할 것.
```

**2. 에이전트가 인프라도 직접 조작하게 한다**  
"DB Proxy 실행해줘" 같은 사전 준비 작업을 사람이 하면 마찰이 생긴다. 에이전트가 상태를 확인하고 필요하면 직접 띄우도록 했다.

**3. 읽기와 쓰기를 분리한다**  
로그 조회, DB 조회는 자동으로 허용하되, 이슈 등록이나 배포 같은 외부 영향 작업은 사람이 확인하는 흐름을 유지했다.

---

## 마치며

"AI가 코드를 써준다"는 것보다 **"AI가 여러 시스템을 넘나들며 맥락을 연결해준다"** 는 것이 실제 운영에서 더 체감되는 변화다.

서비스 모니터링은 단일 도구로 끝나는 일이 아니다. 로그, DB, 코드, 이슈 트래커가 연결될 때 비로소 "지금 무슨 일이 일어나고 있는가"를 답할 수 있다. 에이전트는 그 연결 고리를 대신 잡아준다.

---

*이 글에서 사용한 쿼리와 로그 조회 패턴은 서비스 특성에 맞게 변형하여 적용 가능합니다.*
