import matplotlib.pyplot as plt
import sunpy.map
import sunpy.data.sample
from astropy import units as u
from astropy.coordinates import SkyCoord

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

my_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

top_right = SkyCoord(1200 * u.arcsec, 0 * u.arcsec, frame=my_map.coordinate_frame)
bottom_left = SkyCoord(500 * u.arcsec, -700 * u.arcsec, frame=my_map.coordinate_frame)
my_submap = my_map.submap(bottom_left, top_right)

fig = plt.figure(figsize=(12, 6))
plt.gcf().subplots_adjust(right=0.9)

ax0 = fig.add_subplot(1, 2, 1,  projection=my_map)
my_map.plot(clip_interval=(1, 99.99)*u.percent, axes=ax0)
my_map.draw_rectangle(bottom_left, 700*u.arcsec, 700*u.arcsec)
ax1 = fig.add_subplot(1, 2, 2, projection=my_submap)
my_submap.plot(clip_interval=(1, 99.95)*u.percent, title='', axes=ax1)
my_submap.draw_grid(axes=ax1)
my_submap.draw_limb(axes=ax1)
cbar_ax = plt.gcf().add_axes([0.92, 0.145, 0.02, 0.7])
plt.colorbar(cax=cbar_ax)
plt.savefig('map_example.pdf', dpi=200)
#plt.show()