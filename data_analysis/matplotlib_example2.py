# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import redis
import json
from scrapy_redis.utils import bytes_to_str
from data_analysis.redis_example2 import page_result


class MatplotlibExample2():
    def __init__(self):
        # Connection Pools
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.redis_cli = redis.Redis(connection_pool=pool)

    def process_decode(self, item):
        data_str = bytes_to_str(item)
        data = json.loads(data_str)
        company_os_number = data.get('company_os_number')
        company_name = data.get('company_name')
        company_url = data.get('company_url')
        new_data = {'os_number': company_os_number, 'name': company_name, 'url': company_url}
        # print(new_data)
        return new_data

    def parse_dataframe(self, data):
        # 加这行不需要再写plt.show()，直接显示图像出来
        # %matplotlib inline
        top_num = len(data)
        display_columns = ['project_name', 'collect_count']
        df = pd.DataFrame(data, columns=display_columns)
        top_num_data = df.sort_values(by='collect_count', ascending=False)[:top_num]
        top_num_data = top_num_data.reset_index(drop=True)
        print(top_num_data)

        ax = top_num_data.plot(x='project_name', y='collect_count', kind='bar', title="最火开源项目TOP" + str(top_num),
                               figsize=(9, 6))
        ax.set_xlabel("开源项目名称")
        ax.set_ylabel("开源项目火力值")
        ax.legend().set_visible(False)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()))
        plt.show()

    def execute(self):
        # key = "oschina_company_list:items"
        # result = self.redis_cli.lrange(key, 0, 1 << 8)
        list_data = page_result()
        self.parse_dataframe(list_data)


if __name__ == '__main__':
    matplotlibExample2 = MatplotlibExample2()
    matplotlibExample2.execute()
