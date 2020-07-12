import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from weather.weather_model import ProcessDate

data = pd.read_csv('maxmin1.csv', parse_dates=['date'])
dta = data['tmin']
dtaa = data['tmax']
dta_year = data['date']

# 得到开始年份和结束年份
begin_year = dta_year[0:1].dt.year  # index value
end_year = dta_year[-1:].dt.year  # dt.year是获取year对象年份，Python支持L[-1]取倒数第一个元素，[0:1]第一个索引第一个元素
print(begin_year)
print(end_year)
# 设置数据类型
dta = np.array(dta, dtype=np.float)  # 设置dta的类型，dta是最小值数组，这里要转下数据类型，不然运行会报错
dta = pd.Series(dta)  # 转化为series类型的一维数组，竖着的一维数组
dta.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))  # 索引为年份
print(dta['1981'])  # 输出1981-12-31   69.0，年份输出为一年最后一天，可能因为日期未定吧
print('索引值')
dta.plot(figsize=(12, 8))  # 画最小值的折线图
plt.show()  # 显示结果，在Scala IDE要输入这个命令才能显示图片
# ARIMA 模型对时间序列的要求是平稳型。因此，当你得到一个非平稳的时间序列时，首先要做
# 的即是做时间序列的差分，直到得到一个平稳时间序列。如果你对时间序列做d次差分才能得到
# 一个平稳序列，那么可以使用ARIMA(p,d,q)模型，其中d是差分次数

# 进行一阶差分
data_diff = dta.diff(1)
data_diff = data_diff.dropna()
plt.figure(figsize=(12, 8))
plt.title('First order difference')
plt.plot(data_diff)
plt.show()

# 已经平稳，自相关和偏相关图，默认阶数为30阶
acf = sm.graphics.tsa.plot_acf(data_diff, lags=30)
plt.title('ACF')
acf.show()

pacf = sm.graphics.tsa.plot_pacf(data_diff, lags=30, method='ywm')
plt.title('PACF')
pacf.show()

# 1. ARMA(0,1)模型：即自相关图在滞后1阶之后缩小为0，且偏自相关缩小至0，则是一个阶数q=1的移动平均模型；
# 2. ARMA(7,0)模型：即偏自相关图在滞后7阶之后缩小为0，且自相关缩小至0，则是一个阶层p=3的自回归模型；
# 3. ARMA(7,1)模型：即使得自相关和偏自相关都缩小至零。则是一个混合模型
print('查看哪个模型比较好，aic，bic，hqic越小越好')


print('8，0')
arma_mod80 = sm.tsa.ARMA(dta, (8, 0)).fit(disp=False)
print(arma_mod80.aic, arma_mod80.bic, arma_mod80.hqic)
print('结束')

# 使用ARMA（8，0）模型


resid = arma_mod80.resid
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)  # 2行， 第1列，第1个起始位置
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
ax2 = fig.add_subplot(212)  # 2行，第1列，第2个起始位置
fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)
plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)
plt.show()

# 未来10年同天的预测 数据
predict_year = 10
predict_end_year = end_year.values[0] + predict_year
predict_dta = arma_mod80.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
print(predict_dta)
plt.plot(dta)
plt.plot(predict_dta)
plt.show()

print('传输文件')
p = ProcessDate(data, 10, 'min')
p.process_minmax()
print('传输完毕')
