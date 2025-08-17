# 기업 뉴스 API 서비스

네이버 API와 딥서치 뉴스 API를 활용하여 특정 기업에 대한 최신 뉴스 데이터를 제공하는 FastAPI 백엔드 서비스입니다.

## 🚀 주요 기능

- **네이버 뉴스 API**: 특정 기업명으로 뉴스 검색
- **딥서치 뉴스 API**: 고급 뉴스 분석 및 감정 분석
- **통합 뉴스 검색**: 두 API의 결과를 결합하여 제공
- **스마트 폴백**: API 키가 없을 때 자동으로 모의 데이터 제공
- 최신 뉴스 순으로 정렬
- 페이징 지원 (display, start 파라미터)
- CORS 지원
- 자동 API 문서 생성 (Swagger UI)

## 🏗️ 프로젝트 구조

```
comp_news/
├── app/                          # 메인 애플리케이션 패키지
│   ├── __init__.py
│   ├── main.py                   # 애플리케이션 진입점
│   ├── api/                      # API 라우터
│   │   ├── __init__.py
│   │   ├── v1/                   # API 버전 1
│   │   │   ├── __init__.py
│   │   │   ├── api.py            # API 라우터 연결
│   │   │   └── endpoints/        # 엔드포인트 구현
│   │   │       ├── __init__.py
│   │   │       ├── health.py     # 헬스 체크
│   │   │       └── news.py       # 뉴스 관련 API
│   ├── core/                     # 핵심 설정
│   │   ├── __init__.py
│   │   ├── config.py             # 애플리케이션 설정
│   │   └── settings.py           # 환경 변수 관리
│   ├── models/                   # 데이터 모델
│   │   ├── __init__.py
│   │   └── news.py               # 뉴스 관련 모델
│   ├── services/                 # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── naver_news.py         # 네이버 뉴스 서비스
│   │   └── deepsearch_news.py    # 딥서치 뉴스 서비스
│   └── utils/                    # 유틸리티
│       └── __init__.py
├── tests/                        # 테스트 파일
│   ├── test_naver_news.py
│   └── test_deepsearch_news.py
├── .env                          # 환경 변수 (gitignore에 추가)
├── .env.example                  # 환경 변수 예시
├── requirements.txt              # 의존성 목록
└── README.md                     # 프로젝트 문서
```

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`env.example` 파일을 참고하여 `.env` 파일을 생성하고 API 키를 설정하세요:

```bash
cp env.example .env
```

`.env` 파일에 다음 내용을 추가하세요:

```env
# 네이버 API 설정
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here

# 딥서치 뉴스 API 설정
DEEPSEARCH_API_KEY=your_deepsearch_api_key_here

# 서버 설정
HOST=0.0.0.0
PORT=8000
```

### 3. API 키 발급

#### 네이버 API
1. [네이버 개발자 센터](https://developers.naver.com/)에 접속
2. 애플리케이션 등록
3. "뉴스 검색" API 사용 신청
4. Client ID와 Client Secret 발급

#### 딥서치 뉴스 API
1. [딥서치](https://deepsearch.com/)에 접속
2. 계정 생성 및 로그인
3. API 키 발급
4. 뉴스 검색 API 사용 신청

### 4. 서버 실행

```bash
# 기존 구조로 실행
python main.py

# 또는 새로운 구조로 실행 (개발 중)
python -m app.main

# 또는 uvicorn으로 직접 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔌 API 사용법

### 기본 엔드포인트

- `GET /`: 서비스 정보
- `GET /health`: 서비스 상태 확인
- `GET /docs`: Swagger UI (API 문서)

### 네이버 뉴스 검색 API

#### POST /news/company

```bash
curl -X POST "http://localhost:8000/news/company" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "삼성전자",
    "display": 10,
    "start": 1
  }'
```

#### GET /news/company/{company_name}

```bash
curl "http://localhost:8000/news/company/삼성전자?display=10&start=1"
```

### 딥서치 뉴스 검색 API

#### POST /news/deepsearch

```bash
curl -X POST "http://localhost:8000/news/deepsearch" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "삼성전자",
    "limit": 10,
    "days_back": 30
  }'
```

#### GET /news/deepsearch/{company_name}

```bash
curl "http://localhost:8000/news/deepsearch/삼성전자?limit=10&days_back=30"
```

### 통합 뉴스 검색 API

#### GET /news/combined/{company_name}

```bash
curl "http://localhost:8000/news/combined/삼성전자?naver_limit=5&deepsearch_limit=5"
```

## 📊 응답 데이터 구조

### 네이버 뉴스 응답

```json
{
  "company": "삼성전자",
  "total": 1000,
  "start": 1,
  "display": 10,
  "items": [
    {
      "title": "삼성전자, 새로운 반도체 기술 발표",
      "originallink": "https://example.com/news1",
      "link": "https://news.naver.com/news1",
      "description": "삼성전자가 혁신적인 반도체 기술을 발표했습니다...",
      "pubDate": "Mon, 01 Jan 2024 10:00:00 +0900",
      "source": "naver"
    }
  ]
}
```

### 딥서치 뉴스 응답

```json
{
  "company": "삼성전자",
  "total": 15,
  "items": [
    {
      "title": "삼성전자 실적 전망 긍정적",
      "url": "https://example.com/news2",
      "description": "삼성전자의 실적 전망이 긍정적으로 평가되고 있습니다...",
      "published_at": "2024-01-01T10:00:00Z",
      "source": "deepsearch",
      "company_mentions": ["삼성전자", "삼성"],
      "sentiment": "positive"
    }
  ]
}
```

### 통합 뉴스 응답

```json
{
  "company": "삼성전자",
  "naver_news": {
    "total": 10,
    "items": [...]
  },
  "deepsearch_news": {
    "total": 15,
    "items": [...]
  },
  "combined_total": 25
}
```

## ⚙️ 파라미터 설명

### 네이버 뉴스 API
- `company_name`: 검색할 기업명 (필수)
- `display`: 한 번에 가져올 뉴스 개수 (기본값: 10, 최대: 100)
- `start`: 시작 위치 (기본값: 1)

### 딥서치 뉴스 API
- `company_name`: 검색할 기업명 (필수)
- `limit`: 가져올 뉴스 개수 (기본값: 10, 최대: 100)
- `days_back`: 몇 일 전까지의 뉴스를 검색할지 (기본값: 30, 최대: 365)

### 통합 뉴스 API
- `company_name`: 검색할 기업명 (필수)
- `naver_limit`: 네이버에서 가져올 뉴스 개수 (기본값: 5)
- `deepsearch_limit`: 딥서치에서 가져올 뉴스 개수 (기본값: 5)
- `deepsearch_days_back`: 딥서치 검색 기간 (기본값: 30)

## 🧪 테스트

### 기존 네이버 API 테스트

```bash
python test_api.py
```

### 딥서치 뉴스 API 테스트

```bash
python test_deepsearch_api.py
```

### API 직접 테스트

```bash
# 헬스 체크
curl http://localhost:8000/health

# 딥서치 뉴스 검색
curl -X POST "http://localhost:8000/news/deepsearch" \
  -H "Content-Type: application/json" \
  -d '{"company_name": "삼성전자", "limit": 3}'

# 통합 뉴스 검색
curl "http://localhost:8000/news/combined/삼성전자?naver_limit=2&deepsearch_limit=2"
```

## 🏗️ FastAPI 구조 설계 원칙

### 1. 계층 분리 (Layered Architecture)
- **API Layer**: HTTP 요청/응답 처리
- **Service Layer**: 비즈니스 로직
- **Model Layer**: 데이터 구조 정의
- **Core Layer**: 설정 및 공통 기능

### 2. 의존성 주입 (Dependency Injection)
- FastAPI의 `Depends`를 활용한 서비스 주입
- 테스트 용이성 및 코드 재사용성 향상

### 3. 모델 검증 (Model Validation)
- Pydantic을 활용한 자동 데이터 검증
- API 문서 자동 생성

### 4. 에러 처리 (Error Handling)
- 일관된 HTTP 상태 코드 반환
- 상세한 에러 메시지 제공

### 5. 설정 관리 (Configuration Management)
- 환경 변수를 통한 설정 분리
- 개발/운영 환경별 설정 관리

## 🔧 개발 환경

- **Python**: 3.8+
- **FastAPI**: 0.104.1+
- **Uvicorn**: 0.24.0+
- **Pydantic**: 2.5.0+
- **Requests**: 2.31.0+
- **Python-dotenv**: 1.0.0+

## 📚 추가 문서

- [딥서치 뉴스 API 설정 가이드](DEEPSEARCH_SETUP.md)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)

## 🚀 향후 개선 계획

- [ ] 데이터베이스 연동 (뉴스 캐싱)
- [ ] 사용자 인증 및 권한 관리
- [ ] 뉴스 알림 서비스
- [ ] 대시보드 웹 인터페이스
- [ ] 뉴스 분석 리포트 생성
- [ ] API 사용량 모니터링

## 📄 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
