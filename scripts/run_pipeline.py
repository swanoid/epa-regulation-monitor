#!/usr/bin/env python
# coding: utf-8

# scripts/run_pipeline.py
'''
전체 파이프라인 실행
1) EPA Proposed Rule 데이터 수집
2) 표준 스키마로 정제
3) 품질검증(QA) 후 리포트 작성
4) 트렌드 그래프 생성
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 이렇게 하면 프로젝트 루트가 import 경로에 추가됨

import pandas as pd
from src.fetch_epa import fetch_epa_proposed_rules
from src.normalize import normalize
from src.qa import basic_qa, write_qa_markdown
from src.visualize import run_all_plots

def main():
    # 현재 스크립트는 프로젝트 루트(epa-regulation-monitor/)에서 python scripts/run_pipeline.py로 실행된다고 가정
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('visuals', exist_ok=True)

    # 1) 수집
    df_raw = fetch_epa_proposed_rules()
    raw_path = 'data/raw/epa_prorule_raw.csv'
    df_raw.to_csv(raw_path, index=False)
    print(f"[OK] Raw data saved -> {raw_path} ({len(df_raw)} rows)")

    if df_raw.empty:
        print('[WARN] No data. No next step.')
        return

    # 2) 정제/표준화
    df_norm = normalize(df_raw)
    processed_path = 'data/processed/epa_prorule_normalized.csv'
    df_norm.to_csv(processed_path, index=False)
    print(f"[OK] Normalized data saved -> {processed_path}")

    # 3) QA
    report = basic_qa(df_norm)
    qa_path = 'reports/qa_report.md'
    write_qa_markdown(report, qa_path)
    print(f"[OK] QA report saved -> {qa_path}")

    # 4) 시각화
    # 이 스크립트는 프로젝트 루트에서 실행되니까 base_dir='.' 으로 지정
    plot_paths = run_all_plots(df_norm, base_dir='.')
    for name, path in plot_paths.items():
        print(f"[OK] {name} plot saved -> {path}")

if __name__ == '__main__':
    main()
