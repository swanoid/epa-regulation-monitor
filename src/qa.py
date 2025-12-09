#!/usr/bin/env python
# coding: utf-8

# src/qa.py
'''
데이터 품질을 간단히 체크하고 Markdown 리포트로 저장하는 모듈
'''

import pandas as pd
from datetime import datetime

# 매개변수 df 타입은 데이터프레임 형태고, 도출은 dict 형태로!
def basic_qa(df: pd.DataFrame) -> dict:
    '''
    결측, 중복, 날짜 형식 등 기본 품질 지표 계산
    '''
    report = {}

    # 행 개수
    report['rows'] = len(df)
    # 전체 컬럼 결측치 개수
    report['missing_by_col'] = {c: int(df[c].isna().sum()) for c in df.columns}
    # 제목 컬럼 중복치 개수
    report['duplicate_titles'] = int(df['title'].duplicated().sum())

    # 날짜 파싱 시도
    parsed_dates = pd.to_datetime(df['date'], errors='coerce')
    # 날짜 결측치 개수
    report['invalid_dates'] = int(parsed_dates.isna().sum())

    # summary 길이 체크 (너무 짧은 요약)
    lengths = df['summary'].fillna('').astype(str).str.len()
    # summary 길이 20 이하 개수
    report['short_summaries(<20)'] = int((lengths < 20).sum())

    return report




# 매겨변수 report 타입은 dict 형태, path 타입은 str 형태, 도출(return)은 없어!
def write_qa_markdown(report: dict, path: str) -> None:
    '''
    QA 결과를 Markdown 파일로 저장
    '''
    lines = []
    lines.append('# QA Report')
    lines.append('')
    lines.append(f"- Generated: {datetime.utcnow().isoformat()}Z")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
    lines.append(f"- Duplicate titles: **{report.get('duplicate_titles', 0)}**")
    lines.append(f"- Invalid dates: **{report.get('invalied_dates', 0)}**")
    lines.append(f"- Short summaries (<20 chars): **{report.get('short_summaries(<20)', 0)}**")
    lines.append('')
    lines.append('## Missing by Column')
    for col, cnt in report.get('missing_by_col', {}).items():
        lines.append(f"- {col}: {cnt}")

    # lines 리스트에 줄바꿈 각각 넣기 cf) join은 문자열의 함수임
    content = '\n'.join(lines)

    # with: 파일 열고 자동 닫기, as f: 열린 파일 객체 f 변수 이름으로
    # w: 쓰기 모드, f.write(content): content를 f 파일에 적어라
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
