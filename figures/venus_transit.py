import numpy as np
import os

import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord, solar_system_ephemeris

from sunpy import map
from sunpy.coordinates import frames, get_body_heliographic_stonyhurst

import sunpy_paper

# Have Astropy use a JPL ephemeris (~10 MB download)
solar_system_ephemeris.set('de432s')

f = '20120606_040731_UTC.0041.fits'

# get the data of interest and save fits files
map1 = map.Map(os.path.join(sunpy_paper.data_dir, f))

# now get venus position
venus = get_body_heliographic_stonyhurst('venus', map1.date, observer=map1.observer_coordinate)
venus_hpc = venus.transform_to(frames.Helioprojective(observer=map1.observer_coordinate))

fov = 100 * u.arcsec
top_right = SkyCoord(venus_hpc.Tx + fov, venus_hpc.Ty + fov, frame=map1.coordinate_frame)
bottom_left = SkyCoord(venus_hpc.Tx - fov, venus_hpc.Ty - fov, frame=map1.coordinate_frame)
smap = map1.submap(top_right, bottom_left)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=smap)
# now get venus position
smap.plot(axes=ax)
smap.draw_limb()
ax.plot_coord(venus_hpc, 'x', color='white')

wave = str(int(map1.wavelength.value))
time = map1.date.to_datetime().strftime('%Y%m%d_%H%M%S')
plt.savefig(f'fig_venus_transit_{wave}_{time}.pdf', dpi=200)
plt.close(fig)
