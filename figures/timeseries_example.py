import matplotlib.pyplot as plt
import matplotlib
import datetime
from sunpy.timeseries import TimeSeries

import matplotlib as mpl

testy = {'font.family' : 'serif',
'font.serif' : 'Computer Modern',
'text.usetex' : True,
'axes.titlesize' : 12,
'axes.labelsize' : 12,
'legend.fontsize' : 12,
'xtick.labelsize' : 12,
'ytick.labelsize' : 12,
'xtick.major.pad' : 3,
'xtick.minor.pad' : 3,
'ytick.major.pad' : 3,
'ytick.minor.pad' : 3,
'xtick.direction' : 'in',
'ytick.direction' : 'in',
'savefig.dpi' : 200,
'savefig.format' : 'pdf',
'savefig.bbox' : 'tight',
'backend': 'TkAgg'}

for key in testy:
    mpl.rcParams[key] = testy[key]

goes_file = 'go1520131028.fits'
goes = TimeSeries(goes_file)

figure = plt.figure()
ax = plt.gca()
plt.plot(goes.data['xrsb'], color='r',label='1-8 $\mathrm{\AA}$')
plt.plot(goes.data['xrsa'], color='b',label='0.5-4 $\mathrm{\AA}$')

ax.set_yscale('log')
ax.set_ylim(1e-9, 1e-3)
ax.set_ylabel('Watts m$^{-2}$')
ax.set_xlabel('Time (UT) 2013-10-28')
ax.set_title('GOES X-ray flux')

ax.yaxis.grid(True, 'major')
ax.xaxis.grid(False, 'major')
ax.legend()


ax.xaxis.set_tick_params(rotation=30)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
ax.set_xlim('2013-10-28 00:00', '2013-10-28 23:59')

plt.savefig('timeseries_example.pdf', dpi=200)