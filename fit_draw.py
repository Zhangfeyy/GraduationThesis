import inline as inline
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import xlrd

data_excel = xlrd.open_workbook('./search_UPuser/Pop&Samp.xls')
table = data_excel.sheets()[0]
fans = table.col_values(6, start_rowx=1, end_rowx=None)

res_freq = stats.relfreq(fans, numbins=50) # numbins 是统计一次的间隔(步长)是多大
pdf_value = res_freq.frequency
cdf_value = np.cumsum(res_freq.frequency)
x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
plt.bar(x, pdf_value, width=res_freq.binsize)
plt.plot(x, cdf_value)
plt.show()