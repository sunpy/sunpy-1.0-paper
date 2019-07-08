import matplotlib.pyplot as plt
import matplotlib
import datetime
from sunpy.timeseries import TimeSeries
from sunpy.net import hek
from sunpy.time import parse_time
client = hek.HEKClient()

goes_file = 'go1520110607.fits'
goes = TimeSeries(goes_file)

flares_hek = client.search(hek.attrs.Time('2011-06-07 00:00', '2011-06-07 23:59'),
                           hek.attrs.FL, hek.attrs.FRM.Name == 'SWPC')

figure = plt.figure()
ax = plt.gca()
plt.plot(goes.data['xrsb'], color='r',label='1-8 $\mathrm{\AA}$')
plt.plot(goes.data['xrsa'], color='b',label='0.5-4 $\mathrm{\AA}$')

ax.set_yscale('log')
ax.set_ylim(1e-9, 1e-3)
ax.set_ylabel('Watts m$^{-2}$')
ax.set_xlabel('Time (UT) 2011-06-07')
ax.set_title('GOES X-ray flux')

ax.axvline(parse_time(flares_hek[0].get('event_peaktime')).to_datetime(), ls='dashed', color='grey', label='Flare peak')

ax.yaxis.grid(True, 'major')
ax.xaxis.grid(False, 'major')
ax.legend()

ax.xaxis.set_tick_params(rotation=30)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
ax.set_xlim('2011-06-07 00:00', '2011-06-07 23:59')
#plt.show()
plt.savefig('timeseries_example.pdf', dpi=200)