#!/usr/bin/env python
# coding: utf-8

# src/normalize.py
'''
데이터를 표준 스키마로 정제/통일하는 모듈
'''

import pandas as pd

STANDARD_COLS = ['country', 'source', 'date', 'title', 'summary', 'agency', 'url']

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    '''
    컬럼을 STANDARD_COLS 기준으로 맞추고, 불필요한 공백 등을 간단히 정리
    '''
    # df 원본 복사 out에 저장
    out = df.copy()

    # 필요한 컬럼이 없으면 빈 컬럼 추가
    for col in STANDARD_COLS:
        if col not in out.columns:
            out[col] = None

    # 표준 컬럼 형태로 out에 저장
    out = out[STANDARD_COLS]

    # 문자열 컬럼은 양쪽 공백 제거
    for col in ['title', 'summary', 'agency', 'url']:
        out[col] = out[col].astype(str).str.strip()

    return out
