#!/usr/bin/env python3
"""
딥서치 뉴스 API 테스트
"""
import requests
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 기본 URL
BASE_URL = "http://localhost:8000"


def test_deepsearch_news_api():
    """딥서치 뉴스 API 테스트"""
    print("=== 딥서치 뉴스 API 테스트 ===")
    
    # 테스트할 회사명
    company_name = "삼성전자"
    
    # POST 요청으로 딥서치 뉴스 검색
    print(f"\n1. POST /news/deepsearch - {company_name} 뉴스 검색")
    try:
        response = requests.post(
            f"{BASE_URL}/news/deepsearch",
            json={
                "company_name": company_name,
                "limit": 5,
                "days_back": 30
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 성공: {data['total']}개의 뉴스 발견")
            print(f"회사: {data['company']}")
            
            for i, item in enumerate(data['items'][:3], 1):
                print(f"\n뉴스 {i}:")
                print(f"  제목: {item['title']}")
                print(f"  URL: {item['url']}")
                print(f"  설명: {item['description'][:100]}...")
                print(f"  발행일: {item['published_at']}")
                print(f"  소스: {item['source']}")
                if item.get('sentiment'):
                    print(f"  감정: {item['sentiment']}")
                if item.get('company_mentions'):
                    print(f"  기업 언급: {', '.join(item['company_mentions'])}")
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"에러: {response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


def test_deepsearch_news_simple():
    """GET 요청으로 딥서치 뉴스 검색 테스트"""
    print(f"\n=== GET 요청 딥서치 뉴스 API 테스트 ===")
    
    company_name = "LG전자"
    
    print(f"\n2. GET /news/deepsearch/{company_name} - {company_name} 뉴스 검색")
    try:
        response = requests.get(
            f"{BASE_URL}/news/deepsearch/{company_name}",
            params={"limit": 3, "days_back": 14}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 성공: {data['total']}개의 뉴스 발견")
            
            for i, item in enumerate(data['items'], 1):
                print(f"\n뉴스 {i}:")
                print(f"  제목: {item['title']}")
                print(f"  URL: {item['url']}")
                print(f"  발행일: {item['published_at']}")
                print(f"  소스: {item['source']}")
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"에러: {response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


def test_combined_news():
    """통합 뉴스 검색 테스트"""
    print(f"\n=== 통합 뉴스 검색 API 테스트 ===")
    
    company_name = "현대자동차"
    
    print(f"\n3. GET /news/combined/{company_name} - {company_name} 통합 뉴스 검색")
    try:
        response = requests.get(
            f"{BASE_URL}/news/combined/{company_name}",
            params={
                "naver_limit": 3,
                "deepsearch_limit": 3,
                "deepsearch_days_back": 30
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 성공: 총 {data['combined_total']}개의 뉴스 발견")
            print(f"회사: {data['company']}")
            
            print(f"\n네이버 뉴스: {data['naver_news']['total']}개")
            print(f"딥서치 뉴스: {data['deepsearch_news']['total']}개")
            
            # 네이버 뉴스 샘플 출력
            if data['naver_news']['items']:
                print(f"\n네이버 뉴스 샘플:")
                for i, item in enumerate(data['naver_news']['items'][:2], 1):
                    print(f"  {i}. {item['title']}")
            
            # 딥서치 뉴스 샘플 출력
            if data['deepsearch_news']['items']:
                print(f"\n딥서치 뉴스 샘플:")
                for i, item in enumerate(data['deepsearch_news']['items'][:2], 1):
                    print(f"  {i}. {item['title']}")
                    
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"에러: {response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


def test_api_health():
    """API 상태 확인"""
    print("=== API 상태 확인 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API 서버가 정상적으로 작동 중입니다.")
        else:
            print(f"❌ API 서버 상태 이상: {response.status_code}")
    except Exception as e:
        print(f"❌ API 서버에 연결할 수 없습니다: {str(e)}")
        print("서버가 실행 중인지 확인하세요: python main.py")


def main():
    """메인 테스트 함수"""
    print("딥서치 뉴스 API 테스트를 시작합니다...\n")
    
    # API 상태 확인
    test_api_health()
    
    # 딥서치 뉴스 API 테스트
    test_deepsearch_news_api()
    
    # GET 요청 딥서치 뉴스 테스트
    test_deepsearch_news_simple()
    
    # 통합 뉴스 검색 테스트
    test_combined_news()
    
    print("\n=== 테스트 완료 ===")


if __name__ == "__main__":
    main()
