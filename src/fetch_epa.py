#!/usr/bin/env python
# coding: utf-8

# src/fetch_epa.py
'''
EPA(환경보호청)의 Proposed Rule 데이터를 Federal Register API에서 가져오는 모듈
'''

import requests, pandas as pd
from datetime import datetime, timedelta

# federal Register 검색 기본 URL 저장
BASE_URL = 'http://www.federalregister.gov/api/v1/documents.json'

# 수집 함수 생성
def fetch_epa_proposed_rules(days: int = 365, per_page: int = 100) -> pd.DataFrame:
    '''
    최근 days일 동안의 EPA Proposed Rule 문서를 가져와서 DataFrame으로 반환
    '''
    # 1) 시작 날짜 계산 (YYYY-MM-DD 형식의 문자열)
    start_date = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

    # 2) API 요청에 사용할 파라미터 구성
    params = {
        'per_page': per_page,
        'order': 'newest',
        # 조건 필터
        'conditions[agencies][]': 'environmental-protection-agency', # EPA
        'conditions[type]': 'PRORULE', # Proposed Rule
        'conditions[publication_date][gte]': start_date, # 최근 days일
    }

    # 3) 페이지네이션 + 요청 보내기
    all_results = []
    page = 1

    while True:
        params['page'] = page
        resp = requests.get(BASE_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        results = data.get('results', [])
        if not results:
            # 이 페이지에 결과가 없으면 종료
            break

        all_results.extend(results)

        # total_pages 정보가 있으면, 마지막 페이지까지 오면 종료
        total_pages = data.get('total_pages')
        if total_pages is not None and page >= total_pages:
            break

        page += 1

    # 한 건도 없으면 빈 DataFrame 반환
    if not all_results:
        return pd.DataFrame()

    # 4) DataFrame으로 변환
    df = pd.json_normalize(all_results)

    # 5) 필요한 컬럼만 골라서 이름 정리
    keep_cols = ['publication_date', 'title', 'abstract', 'html_url', 'agencies']
    # df에 keep_cols 내용을 포함하고 있는 걸로 keep_cols 다시 저장
    keep_cols = [c for c in keep_cols if c in df.columns]
    # df 컬럼명 표준화, 통일하기
    df = df[keep_cols].rename(
        columns={
            'publication_date': 'date',
            'abstract': 'summary',
            'html_url': 'url',
            'agencies': 'agency'
        }
    )

    # agency가 리스트 형태일 수 있으니 문자열로 변환
    df['agency'] = df['agency'].astype(str)

    # 6) 메타 정보 컬럼 추가
    df['country'] = 'US'
    df['source'] = 'Federal Register'

    # 컬럼 순서 정리
    cols = ['country', 'source', 'date', 'title', 'summary', 'agency', 'url']
    df = df[cols]

    return df




# 이 파일 직접 실행했을 때만 코드 실행
if __name__ == '__main__':
    # 함수 테스트 실행
    df_test = fetch_epa_proposed_rules()
    print(df_test.head())
    print('rows:', len(df_test))
