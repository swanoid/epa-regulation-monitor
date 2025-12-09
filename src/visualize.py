#!/usr/bin/env python
# coding: utf-8

# src/visualize.py
'''
EPA Proposed Rule 데이터의 기본 트렌드를 시각화하는 모듈
'''

import pandas as pd
import matplotlib.pyplot as plt

# 내부 함수라는 뜻으로 앞에 '_' 붙여줌
def _make_daily_counts(df: pd.DataFrame) -> pd.Series:
    '''
    date 컬럼을 기반으로 하루 단위 카운트를 세는 시리즈 생성
    '''
    dates = pd.to_datetime(df['date'], errors='coerce')
    # dates를 인덱스로 설정, 1을 값으로 채우는 시리즈로 변환
    s = pd.Series(1, index=dates)
    # 하루 단위 합계를 구하고, 결측치는 0으로 채움
    daily_counts = s.resample('D').sum().fillna(0)
    # 시리즈 반환
    return daily_counts




# 일자별 개수(선 그래프: matplotlib 사용)
def plot_daily(df: pd.DataFrame, out_dir: str, filename: str = 'trend_daily.png') -> str:
    daily_counts = _make_daily_counts(df)

    plt.figure(figsize=(10, 4))
    # matplotlib은 x축: .index y축: .values 등 다 지정해줘야 함
    plt.plot(daily_counts.index, daily_counts.values, label='Daily Count')
    plt.title('EPA Proposed Rules per Day')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.tight_layout()

    # 저장 경로 지정
    out_path = f"{out_dir}/{filename}"
    # 그래프 저장 경로에 저장
    plt.savefig(out_path)
    # 그래프 종료
    plt.close()
    # 저장 경로 반환: 확인용
    return out_path




# 일자별 + 7일 이동평균 개수(matplotplib 그래프 사용)
def plot_daily_smooth(df: pd.DataFrame, out_dir: str, filename: str = 'trend_daily_smooth.png', window: int = 7) -> str:
    daily_counts = _make_daily_counts(df)

    plt.figure(figsize=(10, 4))
    # matplotlib 선 그래프, alpha 연하게
    plt.plot(daily_counts.index, daily_counts.values, alpha=0.4, label='Daily Count')
    plt.plot(daily_counts.rolling(window).mean(), linewidth=3, label=f"{window}-Day Rolling Avg")
    plt.title('EPA Proposed Rules (Daily + Rolling Average)')
    plt.xlabel('Date')
    plt.ylabel('Count')
    # label 지정해준 거 범례 표시
    plt.legend()
    plt.tight_layout()

    out_path = f"{out_dir}/{filename}"
    plt.savefig(out_path)
    plt.close()
    return out_path




# 주별 개수(matplotlib 막대 그래프 사용)
def plot_weekly(df: pd.DataFrame, out_dir: str, filename: str = 'trend_weekly.png') -> str:

    daily_counts = _make_daily_counts(df)
    weekly = daily_counts.resample('W').sum()

    plt.figure(figsize=(10, 4))
    # matplotlib 막대 그래프 사용, 판다스 방식도 가능: weekly.plot(kind='bar')
    plt.bar(weekly.index, weekly.values, width=5)
    plt.title('EPA Proposed Rules per Week')
    plt.xlabel('Week')
    plt.ylabel('Count')
    plt.tight_layout()

    out_path = f"{out_dir}/{filename}"
    plt.savefig(out_path)
    plt.close()
    return out_path




# 월별 개수(pandas 막대 그래프 사용)
def plot_monthly(df: pd.DataFrame, out_dir: str, filename: str = 'trend_monthly.png', months: int = 12) -> str:

    daily_counts = _make_daily_counts(df)
    monthly = daily_counts.resample('ME').sum().tail(months)

    # x축을 'YYYY-MM' 문자열로 변환
    monthly.index = monthly.index.strftime('%Y-%m')
    
    plt.figure(figsize=(10, 4))
    # Pandas 방식으로 막대 그래프: matplotlib 방식보다 간편하고 수준 높음 cf) 선 그래프는 kind='line'
    monthly.plot(kind='bar')
    plt.title(f"EPA Proposed Rules per Month (Last {months} Months)")
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.tight_layout()
    
    out_path = f"{out_dir}/{filename}"
    plt.savefig(out_path)
    plt.close()
    return out_path




# '..'은 한 단계 위 폴더 지칭
def run_all_plots(df: pd.DataFrame, base_dir: str = '..') -> dict:
    '''
    전체 시각화를 한 번에 실행하는 함수, 시각화 이미지 파일들의 경로를 dict로 반환
    '''
    # out_dir에 들어갈 경로 설정
    visuals_dir = f"{base_dir}/visuals"

    # 빈 딕서녀리 설정
    paths = {}
    paths['daily'] = plot_daily(df, visuals_dir)
    paths['daily_smooth'] = plot_daily_smooth(df, visuals_dir)
    paths['weekly'] = plot_weekly(df, visuals_dir)
    paths['monthly'] = plot_monthly(df, visuals_dir)
    
    # 경로 반환
    return paths
