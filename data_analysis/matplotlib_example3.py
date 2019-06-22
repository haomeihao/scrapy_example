# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import redis
import json
from scrapy_redis.utils import bytes_to_str
from data_analysis.redis_example3 import page_result


class MatplotlibExample3():
    def __init__(self):
        # Connection Pools
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.redis_cli = redis.Redis(connection_pool=pool)

    def parse_dataframe(self, stars, data):
        # 加这行不需要再写plt.show()，直接显示图像出来
        # %matplotlib inline
        top_num = len(data)
        display_columns = ['language', 'count']
        df = pd.DataFrame(data, columns=display_columns)
        top_num_data = df.sort_values(by='count', ascending=False)[:top_num]
        top_num_data = top_num_data.reset_index(drop=True)
        print(top_num_data)

        # bar barh
        ax = top_num_data.plot(x='language', y='count', kind='bar',
                               title="Github各大编程语言stars>{0}k仓库数量排行榜".format(str(int(stars/1000))),
                               figsize=(9, 6))
        ax.set_xlabel("Github各大编程语言")
        ax.set_ylabel("stars>{0}k仓库数量".format(str(int(stars/1000))))
        ax.legend().set_visible(False)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()))
        plt.show()

    def execute(self):
        for stars in [30000, 10000]:
            list_data = page_result(stars)
            self.parse_dataframe(stars, list_data)


if __name__ == '__main__':
    matplotlibExample3 = MatplotlibExample3()
    matplotlibExample3.execute()
