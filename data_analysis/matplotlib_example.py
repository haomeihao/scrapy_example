# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import redis
import json
from scrapy_redis.utils import bytes_to_str


class MatplotlibExample():
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
        top_num = 50
        display_columns = ['os_number', 'name', 'url']
        df = pd.DataFrame(data, columns=display_columns)
        top_num_data = df.sort_values(by='os_number', ascending=False)[:top_num]
        top_num_data = top_num_data.reset_index(drop=True)
        print(top_num_data)

        ax = top_num_data.plot(x='name', y='os_number', kind='bar', title="开源公司TOP" + str(top_num), figsize=(9, 6))
        ax.set_xlabel("开源公司名称")
        ax.set_ylabel("开源项目数量")
        ax.legend().set_visible(False)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()))
        plt.show()

    def execute(self):
        key = "oschina_company_list:items"
        result = self.redis_cli.lrange(key, 0, 1 << 8)
        list_data = [self.process_decode(item) for item in result]
        self.parse_dataframe(list_data)


if __name__ == '__main__':
    matplotlibExample = MatplotlibExample()
    matplotlibExample.execute()
