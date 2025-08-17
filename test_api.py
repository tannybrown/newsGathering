#!/usr/bin/env python3
"""
기업 뉴스 API 테스트 스크립트
"""

import requests
import json

# API 기본 URL (서버가 실행 중인 경우)
BASE_URL = "http://localhost:8000"

def test_health_check():
    """헬스 체크 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"헬스 체크: {response.status_code}")
        print(f"응답: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return False

def test_get_company_news(company_name, display=5):
    """GET 요청으로 기업 뉴스 검색 테스트"""
    try:
        url = f"{BASE_URL}/news/company/{company_name}"
        params = {"display": display, "start": 1}
        
        print(f"\n{company_name} 뉴스 검색 (GET):")
        print(f"URL: {url}")
        print(f"파라미터: {params}")
        
        response = requests.get(url, params=params)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"총 뉴스 수: {data.get('total', 0)}")
            print(f"가져온 뉴스 수: {len(data.get('items', []))}")
            
            # 첫 번째 뉴스 출력
            if data.get('items'):
                first_news = data['items'][0]
                print(f"\n첫 번째 뉴스:")
                print(f"제목: {first_news.get('title', 'N/A')}")
                print(f"설명: {first_news.get('description', 'N/A')[:100]}...")
                print(f"발행일: {first_news.get('pubDate', 'N/A')}")
        else:
            print(f"오류: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("서버에 연결할 수 없습니다.")
        return False
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
        return False

def test_post_company_news(company_name, display=5):
    """POST 요청으로 기업 뉴스 검색 테스트"""
    try:
        url = f"{BASE_URL}/news/company"
        payload = {
            "company_name": company_name,
            "display": display,
            "start": 1
        }
        
        print(f"\n{company_name} 뉴스 검색 (POST):")
        print(f"URL: {url}")
        print(f"페이로드: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(url, json=payload)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"총 뉴스 수: {data.get('total', 0)}")
            print(f"가져온 뉴스 수: {len(data.get('items', []))}")
        else:
            print(f"오류: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("서버에 연결할 수 없습니다.")
        return False
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("=== 기업 뉴스 API 테스트 ===\n")
    
    # 헬스 체크
    if not test_health_check():
        return
    
    # 테스트할 기업들
    companies = ["삼성전자", "LG전자", "현대자동차"]
    
    for company in companies:
        # GET 요청 테스트
        test_get_company_news(company, 3)
        
        # POST 요청 테스트
        test_post_company_news(company, 3)
        
        print("-" * 50)
    
    print("\n테스트 완료!")

if __name__ == "__main__":
    main()
