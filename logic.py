# -*- coding: utf-8 -*-

import pandas as pd


def get_hedge_fund_details(df) -> pd.DataFrame:
    df = df.iloc[2:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df.drop(columns=['数量','单位成本','停牌信息'],inplace=True)
    df = df[
        (df['科目代码'].astype(str).str.startswith('11090601') & (df['科目代码'] != '11090601')) |
        (df['科目代码'].astype(str).str.startswith('11090501') & (df['科目代码'] != '11090501'))
    ]
    df.drop(columns=['科目代码'],inplace=True)
    df['收益率(%)'] = df['估值增值'] / df['成本'] * 100
    df.sort_values(by='收益率(%)',ascending=False,inplace=True)
    df['成本'] = df['成本'] / 10000
    df['市值'] = df['市值'] / 10000
    df['估值增值'] = df['估值增值'] / 10000
    df.rename(columns={'成本':'成本(万元)','市值':'市值(万元)','估值增值':'估值增值(万元)'},inplace=True)
    df.reset_index(drop=True,inplace=True)
    df['序号'] = df.index + 1
    cols = ['序号'] + [col for col in df.columns if col != '序号']
    df = df[cols]
    df.drop(columns=['市价'],inplace=True)
    # 除“科目名称”列以外，其它列均转为数字格式
    for col in df.columns:
        if col != '科目名称':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df