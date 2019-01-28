# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Series
def learn_series():
    s = pd.Series(['a', 'b', 'c'])
    print(s)
    s = pd.Series(['a', 'b', 'c'], index=['x', 'y', 'z'])
    print(s)
    print(s['x'])
    print(s[:2])
    s = pd.Series({1: 'a', 2: 'b', 3: 'c'})
    print(s)


# DataFrame
def learn_dataframe():
    data = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
    }
    df = pd.DataFrame(data)
    print(df)

    df = pd.DataFrame(np.random.randn(6, 4))
    print(df)

    dates = pd.date_range('20130101', periods=6)
    print(dates)

    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print(df)
    print(df.index)
    print(df.columns)
    print(df.values)

    # head() 行
    print(df.head(3))
    # tail() 尾
    print(df.tail(3))

    # 按索引排序
    print(df.sort_index(axis=1, ascending=False))
    print(df.sort_index(axis=0, ascending=False))
    # 按值排序
    # 根据B列的值的升序排列
    print(df.sort_values(by='B'))
    # 先按A的升序排，再按B的降序排
    print(df.sort_values(by=['A', 'B'], ascending=[True, False]))

    # 选择数据
    # <class 'pandas.core.series.Series'>
    print(type(df['A']))
    # <class 'pandas.core.frame.DataFrame'>
    print(type(df[['A', 'B']]))

    # 切片操作
    print(df[0:3])

    # 通过loc、.iloc 高效获取数据
    print(df.loc["2013-01-01":"2013-01-03", ['A', 'B']])
    print(df.iloc[1:4, 0:2])

    # 通过条件过滤数据
    print(df[df.A > 0])

    # 求和
    # <class 'pandas.core.series.Series'>
    print(type(df.sum()))

    # 求平均值
    # <class 'pandas.core.series.Series'>
    print(type(df.mean()))

    # 求最大/小值
    print(df.max())
    print(df.min())

    # 分组 groupby
    print(df.groupby('A').size())

    df['E'] = df.index

    print(df.groupby('E').size())

    print(df.groupby(lambda x: df.E[x].year).size())


if __name__ == '__main__':
    learn_dataframe()
