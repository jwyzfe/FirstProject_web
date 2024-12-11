# 0. https://esg.krx.co.kr/contents/02/02020000/ESG02020000.jsp 타겟 웹 사이트
# 1. ```#gridtableeccbc87e4b5ce2fe28308fd9f2a7baf3 > colgroup``` 태그를 사용
# 2. ```#pagenavia87ff679a2f3e71d9181a67b7542122c > ul > li.next``` 태그를 사용 스크래핑

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_esg_data():
    # 기본 URL
    base_url = "https://esg.krx.co.kr/contents/02/02020000/ESG02020000.jsp"
    
    try:
        # 세션 생성
        session = requests.Session()
        
        # 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 첫 페이지 요청
        response = session.get(base_url, headers=headers)
        response.raise_for_status()  # HTTP 오류 체크
        
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 데이터를 저장할 리스트
        all_data = []
        
        # 페이지 순회
        page = 1
        while True:
            print(f"Scraping page {page}...")
            
            # 테이블 데이터 추출
            table = soup.select_one('#gridtableeccbc87e4b5ce2fe28308fd9f2a7baf3')
            if not table:
                print("Table not found")
                break
                
            # 행 데이터 추출
            rows = table.select('tr')
            for row in rows[1:]:  # 헤더 제외
                cols = row.select('td')
                if cols:
                    row_data = [col.text.strip() for col in cols]
                    all_data.append(row_data)
            
            # 다음 페이지 버튼 확인
            next_button = soup.select_one('#pagenavia87ff679a2f3e71d9181a67b7542122c > ul > li.next')
            if not next_button or 'disabled' in next_button.get('class', []):
                print("No more pages")
                break
                
            # 다음 페이지 요청
            page += 1
            
            # 페이지 파라미터 설정
            params = {
                'currentPage': page,
                # 필요한 경우 추가 파라미터 설정
            }
            
            # 다음 페이지 요청
            response = session.get(base_url, params=params, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 요청 간 딜레이
            time.sleep(1)
            
        # 데이터프레임 생성
        columns = ['종목코드', '종목명', 'ESG등급', '환경등급', '사회등급', '지배구조등급']  # 실제 컬럼명으로 수정 필요
        df = pd.DataFrame(all_data, columns=columns)
        
        # CSV 파일로 저장
        df.to_csv('esg_data.csv', index=False, encoding='utf-8-sig')
        print("Data successfully saved to esg_data.csv")
        
        return df
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    scrape_esg_data()