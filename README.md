# Claude Code Hello World

이 프로젝트는 간단한 "hello world 함수를 추가한 main.py 파일"로 시작하여 FastAPI 기반의 완전한 웹 API로 발전한 프로젝트입니다. Claude Code와의 대화를 통해 점진적으로 기능을 추가하며 개발되었습니다.

## 개발 과정

1. **시작**: 기본 Hello World 함수
2. **클래스화**: 클래스 구조로 변경 + argparse 추가
3. **FastAPI 전환**: 웹 API로 변환 (POST 제외)
4. **환경 구성**: 가상환경 생성 및 패키지 설치
5. **프로젝트 발전**: 모듈화된 구조로 대규모 개선

## 현재 프로젝트 구조

```
claude_code/
├── app/
│   ├── core/
│   │   ├── config.py        # 환경 설정 관리
│   │   ├── exceptions.py    # 전역 예외 처리
│   │   └── logger.py        # 로깅 시스템
│   ├── models/
│   │   └── user.py          # Pydantic 데이터 모델
│   ├── routers/
│   │   ├── hello.py         # Hello World API 엔드포인트
│   │   └── users.py         # 사용자 관리 CRUD API
│   └── services/
│       ├── hello_service.py # Hello World 비즈니스 로직
│       └── user_service.py  # 사용자 관리 비즈니스 로직
├── venv/                    # Python 가상환경
├── main.py                  # FastAPI 애플리케이션 진입점
├── pyproject.toml           # 프로젝트 설정 및 의존성
├── .env.example            # 환경변수 설정 예시
└── README.md               # 프로젝트 문서
```

## 구현된 기능

### 🎯 Hello World API
- `GET /api/v1/` - 기본 Hello World 메시지 반환
- `GET /api/v1/hello` - 쿼리 파라미터로 커스텀 메시지
- `POST /api/v1/hello` - JSON으로 메시지 전송
- 타임스탬프 포함된 응답

### 👥 사용자 관리 API (완전한 CRUD)
- `POST /api/v1/users/` - 새 사용자 생성 (이름, 이메일, 비밀번호)
- `GET /api/v1/users/` - 사용자 목록 조회 (페이지네이션 지원)
- `GET /api/v1/users/{user_id}` - 특정 사용자 상세 조회
- `PUT /api/v1/users/{user_id}` - 사용자 정보 수정
- `DELETE /api/v1/users/{user_id}` - 사용자 삭제

### 🛠️ 시스템 기능
- **에러 핸들링**: 전역 HTTP 예외 처리
- **로깅 시스템**: 구조화된 로그 출력
- **환경 설정**: .env 파일 기반 설정 관리
- **타입 안전성**: Pydantic 모델로 입출력 검증
- **API 문서**: 자동 생성되는 Swagger/ReDoc 문서

## 빠른 시작

### 1. 환경 준비
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate (Windows)

# 의존성 설치
uv sync
# 또는 pip install -e .
```

### 2. 서버 실행
```bash
python main.py
```

서버가 http://0.0.0.0:8000 에서 실행됩니다.

### 3. API 확인
- **루트 페이지**: http://localhost:8000/
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc

## 사용 예시

### Hello World 테스트
```bash
# 기본 메시지
curl http://localhost:8000/api/v1/

# 커스텀 메시지
curl "http://localhost:8000/api/v1/hello?message=안녕하세요"
```

### 사용자 관리 예시
```bash
# 사용자 생성
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김철수",
    "email": "kim@example.com",
    "password": "secure123"
  }'

# 사용자 목록 조회
curl http://localhost:8000/api/v1/users/

# 특정 사용자 조회
curl http://localhost:8000/api/v1/users/1
```

## 기술 스택

- **FastAPI**: 현대적이고 빠른 웹 프레임워크
- **Pydantic**: 타입 힌트 기반 데이터 검증
- **Uvicorn**: 고성능 ASGI 서버
- **Python 3.10+**: 최신 Python 기능 활용
- **Email-validator**: 이메일 주소 검증

## 개발 히스토리

이 프로젝트는 Claude Code와의 실시간 대화를 통해 다음과 같이 발전했습니다:

1. **기본 함수** → **클래스 구조** → **FastAPI 전환**
2. **단순 API** → **모듈화된 구조** → **완전한 CRUD**
3. **기본 기능** → **에러 처리** → **로깅 및 설정 관리**

각 단계마다 사용자 요청에 따라 점진적으로 기능을 추가하며, 실무에서 사용할 수 있는 수준의 API 서버로 발전했습니다.

---

**💡 참고**: 이 프로젝트는 교육 목적으로 제작되었으며, 실제 프로덕션 환경에서는 데이터베이스 연동, 인증/권한, 보안 설정 등의 추가 구현이 필요합니다.