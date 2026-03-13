# 멀티페이지 문서 아키텍처 (Multi-Page Documentation)

단일 페이지로 다루기 어려운 주제는 폴더 구조로 분리한다. 이 파일은 폴더 구조, 분리 기준, 크로스링크 패턴을 다룬다.

---

## 권장 폴더 구조

```
docs/
├── overview.md              # 전체 문서 집합의 진입점
├── get-started.md           # 빠른 시작 (설치 → 첫 실행)
├── tutorials/               # 학습 중심: 목표 결과물이 있는 단계별 실습
│   ├── tutorial-a.md
│   └── tutorial-b.md
├── how-tos/                 # 문제 해결: 특정 작업 달성 절차
│   ├── how-to-a.md
│   └── how-to-b.md
├── explanations/            # 개념·원리·배경 설명
│   ├── concept-a.md
│   └── concept-b.md
├── reference/               # API·함수·설정 스펙
│   ├── api-overview.md
│   ├── function-a.md
│   └── function-b.md
├── troubleshooting.md       # 자주 발생하는 오류 진단·해결
└── glossary.md              # 용어 정의
```

**디자인 원칙**: 각 폴더는 독자의 목적에 대응한다. 독자가 "배우고 싶다" → tutorials/, "해결하고 싶다" → how-tos/, "이해하고 싶다" → explanations/, "확인하고 싶다" → reference/.

---

## 분리 기준 (When to Split)

아래 조건 중 하나라도 해당하면 페이지를 분리한다:

1. **헤딩 깊이 초과**: 현재 페이지에 `####` 이상의 헤딩이 필요할 때
2. **복수 목적**: 독자가 이 페이지에 두 가지 다른 이유로 방문할 때
   (예: "개념 이해"와 "설치 방법" 모두를 찾아오는 경우)
3. **스크롤 부하**: 페이지가 500 단어를 넘고 목차 없이는 탐색이 어려울 때
4. **독립 재사용**: 다른 문서에서 이 섹션을 단독으로 링크해야 할 때

**분리하지 말아야 할 경우**: 단계가 순서대로 실행되어야 하는 튜토리얼 — 페이지를 쪼개면 맥락이 끊긴다.

---

## 크로스링크 패턴 (Cross-Linking)

문서 유형 간 연결은 독자의 다음 목적을 안내한다.

### 학습 → 심화

튜토리얼 말미에 개념 설명과 레퍼런스로 연결:
```markdown
## 다음 단계

- 원리를 깊이 이해하려면 → [JWT 인증 원리](../explanations/jwt.md)
- 전체 API 스펙은 → [`createToken` API](../reference/create-token.md)
```

### 참조 → 예제

레퍼런스 페이지에서 실제 사용 예제로 연결:
```markdown
## 관련 튜토리얼

실제 적용 방법은 [FastAPI 인증 튜토리얼](../tutorials/fastapi-auth.md)을 참고하십시오.
```

### 문제 해결 → 원인 설명

트러블슈팅에서 에러 원인의 배경 설명으로 연결:
```markdown
이 오류가 발생하는 이유는 [CORS 정책 설명](../explanations/cors.md)을 참고하십시오.
```

---

## 내비게이션 계층 설계

- `overview.md`는 전체 문서 집합의 목차 역할을 한다
- 각 폴더의 `index.md`(또는 `README.md`)는 해당 섹션의 목차다
- 브레드크럼(breadcrumb)은 독자에게 현재 위치를 알려준다:
  `Docs > Tutorials > FastAPI 컨테이너화`
- 관련 페이지는 "관련 문서" 섹션으로 페이지 하단에 모은다

---

## 체크리스트

- [ ] 각 페이지는 한 가지 독자 목적만 다루는가?
- [ ] `overview.md`에서 전체 구조를 한눈에 파악할 수 있는가?
- [ ] 크로스링크가 독자의 다음 목적을 안내하는가?
- [ ] 헤딩 깊이가 H4를 초과하는 페이지가 없는가?
