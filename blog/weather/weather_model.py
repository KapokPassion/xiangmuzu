
import pandas as pd
import numpy as np
from pandas import Series
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

from weather.file_transfer import SendFile
import weather.process_json

class ProcessDate:
    def __init__(self, data, predict_year, data_type):
        self.data = data
        self.predict_year = predict_year
        self.data_type = data_type

    def process_minmax(self):
        if self.data_type == 'max':
            max_data = self.data['tmax']
        elif self.data_type == 'min':
            max_data = self.data['tmin']
        data_year = self.data['date']
        begin_year = data_year[0:1].dt.year
        end_year = data_year[-1:].dt.year
        print(begin_year)
        print('成功')
        predict_month = data_year[0:1].dt.month
        predict_day = data_year[0:1].dt.day
        max_data = np.array(max_data, dtype=np.float)
        # 转换为一维数组
        max_data = pd.Series(max_data)
        max_data.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))

        arma_mod80 = sm.tsa.ARMA(max_data, (8, 0)).fit()
        predict_end_year = end_year.values[0] + self.predict_year
        predict_dta = arma_mod80.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
        print(predict_dta)
        predict_dta.to_json(self.data_type + '.json', date_format='iso')
        #原文是fjd  不知道啥意思fjd，现在改为predict_dta

        json_date = weather.process_json.format_json(self.data_type + '.json', str(predict_month.values[0]), str(predict_day.values[0]))
        print(json_date)

        predict_dta = arma_mod80.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
        plt.plot(predict_dta)

        # fig=plt.gcf()
        # plt.show()
        plt.savefig(self.data_type + '.png', dpi=100)

        # send file
        send = SendFile(fileName=self.data_type + '.png')
        send.send()
