# 딥서치 뉴스 API 설정 가이드

## 개요

딥서치 뉴스 API는 고급 뉴스 분석 및 감정 분석 기능을 제공하는 서비스입니다. 이 가이드를 통해 딥서치 뉴스 API를 설정하고 사용할 수 있습니다.

## 딥서치 뉴스 API 특징

- **고급 뉴스 검색**: AI 기반 뉴스 검색 및 분석
- **감정 분석**: 뉴스의 감정적 톤 분석 (긍정/부정/중립)
- **기업 언급 추적**: 특정 기업이 언급된 뉴스 추적
- **시간 기반 필터링**: 특정 기간 내 뉴스 검색
- **다국어 지원**: 한국어를 포함한 다국어 뉴스 지원

## API 키 발급 과정

### 1. 딥서치 계정 생성
1. [딥서치 공식 웹사이트](https://deepsearch.com/)에 접속
2. "Sign Up" 또는 "회원가입" 클릭
3. 이메일, 비밀번호 등 기본 정보 입력
4. 이메일 인증 완료

### 2. API 키 발급
1. 로그인 후 대시보드 접속
2. "API Keys" 또는 "API 키" 메뉴 클릭
3. "Generate New API Key" 또는 "새 API 키 생성" 클릭
4. API 키 이름 입력 (예: "뉴스 검색 API")
5. 생성된 API 키 복사하여 안전한 곳에 보관

### 3. API 사용 신청
1. "API Services" 또는 "API 서비스" 메뉴 접속
2. "News Search API" 또는 "뉴스 검색 API" 선택
3. 사용량 계획 선택 (무료 플랜부터 시작 가능)
4. 사용 신청 제출

## 환경 변수 설정

### .env 파일에 API 키 추가

```env
# 기존 네이버 API 설정
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here

# 딥서치 뉴스 API 설정
DEEPSEARCH_API_KEY=your_actual_deepsearch_api_key_here

# 서버 설정
HOST=0.0.0.0
PORT=8000
```

### API 키 보안 주의사항

- API 키를 소스 코드에 직접 하드코딩하지 마세요
- .env 파일을 .gitignore에 추가하여 Git에 커밋되지 않도록 하세요
- API 키를 공개 저장소나 공개 채널에 노출하지 마세요

## API 사용 예시

### 기본 뉴스 검색

```bash
# POST 요청으로 뉴스 검색
curl -X POST "http://localhost:8000/news/deepsearch" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "삼성전자",
    "limit": 10,
    "days_back": 30
  }'
```

### GET 요청으로 뉴스 검색

```bash
# GET 요청으로 뉴스 검색
curl "http://localhost:8000/news/deepsearch/삼성전자?limit=5&days_back=14"
```

### 통합 뉴스 검색

```bash
# 네이버와 딥서치 뉴스를 모두 가져오기
curl "http://localhost:8000/news/combined/삼성전자?naver_limit=5&deepsearch_limit=5"
```

## 응답 데이터 구조

### 딥서치 뉴스 응답

```json
{
  "company": "삼성전자",
  "total": 15,
  "items": [
    {
      "title": "삼성전자 실적 전망 긍정적",
      "url": "https://example.com/news/article1",
      "description": "분석가들은 삼성전자의 실적 전망을 긍정적으로 평가...",
      "published_at": "2024-01-01T10:00:00Z",
      "source": "deepsearch",
      "company_mentions": ["삼성전자", "삼성"],
      "sentiment": "positive"
    }
  ]
}
```

### 필드 설명

- `title`: 뉴스 제목
- `url`: 뉴스 원문 URL
- `description`: 뉴스 요약 또는 설명
- `published_at`: 발행일시 (ISO 8601 형식)
- `source`: 뉴스 소스 (항상 "deepsearch")
- `company_mentions`: 기업명이 언급된 형태들
- `sentiment`: 감정 분석 결과 (positive, negative, neutral)

## 모의 데이터 모드

딥서치 API 키가 설정되지 않은 경우, 시스템은 자동으로 모의 데이터를 반환합니다. 이는 개발 및 테스트 목적으로 유용합니다.

### 모의 데이터 특징

- 실제 API 호출 없이 테스트 가능
- 다양한 감정 분석 결과 포함
- 랜덤한 발행일시 생성
- 실제 기업명을 포함한 맞춤형 뉴스 제목

## 에러 처리

### 일반적인 에러 코드

- `500`: 서버 내부 오류
- `400`: 잘못된 요청 파라미터
- `401`: 인증 실패 (API 키 문제)
- `429`: 요청 한도 초과

### 에러 응답 예시

```json
{
  "detail": "딥서치 API 호출 중 오류가 발생했습니다: 401 Unauthorized"
}
```

## 성능 최적화 팁

1. **적절한 limit 설정**: 한 번에 너무 많은 뉴스를 요청하지 마세요
2. **days_back 최적화**: 필요한 기간만큼만 설정하세요
3. **캐싱 활용**: 동일한 검색 결과는 캐싱하여 재사용하세요
4. **비동기 처리**: 대량의 뉴스 검색 시 비동기 처리를 고려하세요

## 지원 및 문의

- **공식 문서**: [딥서치 API 문서](https://docs.deepsearch.com/)
- **개발자 포럼**: [딥서치 개발자 커뮤니티](https://community.deepsearch.com/)
- **기술 지원**: support@deepsearch.com

## 라이선스 및 사용 약관

딥서치 뉴스 API 사용 시 딥서치의 서비스 약관 및 개인정보 처리방침을 준수해야 합니다. 자세한 내용은 공식 웹사이트를 참조하세요.
