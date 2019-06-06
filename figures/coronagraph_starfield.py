import os
import matplotlib.pyplot as plt

from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord, get_body_barycentric

import sunpy.map
from sunpy.coordinates import get_body_heliographic_stonyhurst, frames

import sunpy_paper
#sunpy_paper.setup_plot()

f = '2014_05_15__07_54_00_005__STEREO-A_SECCHI_COR2_white-light.jp2'
path = os.path.join(sunpy_paper.data_dir, f)
map1 = sunpy.map.Map(path)

# finding the correct pointing location for the Sun as seen from STEREO
stereo = map1.observer_coordinate.transform_to('icrs').cartesian
sun = get_body_barycentric('sun', time=map1.date)
diff = sun - stereo
search_coord = SkyCoord(diff, frame='icrs')

# look up stars in a star catalog
vv = Vizier(columns=['**'], row_limit=-1,
            column_filters={'Gmag': '<7'}, timeout=1200)
vv.ROW_LIMIT = -1
result = vv.query_region(search_coord, radius=4 * u.deg, catalog='I/345/gaia2')

hpc_coords = []
for this_object in result[0]:
    tbl_crds = SkyCoord(this_object['RA_ICRS'] * u.deg, this_object['DE_ICRS'] * u.deg,
                        1e12 * u.km, frame='icrs', obstime=map1.date)
    hpc_coords.append(tbl_crds.transform_to(
        frames.Helioprojective(observer=map1.observer_coordinate)))

# get the location of mars
mars = get_body_heliographic_stonyhurst(
    'mars', map1.date, observer=map1.observer_coordinate)
mars_hpc = mars.transform_to(
    frames.Helioprojective(observer=map1.observer_coordinate))

# now plot
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection=map1)

map1.plot(axes=ax, vmin=0, vmax=600)

ax.plot_coord(mars_hpc, 's', color='white',
              fillstyle='none', markersize=12, label='Mars')
for this_coord in hpc_coords:
    ax.plot_coord(this_coord, 'o', color='white', fillstyle='none')

map1.draw_limb()
map1.draw_grid()

lon, lat = ax.coords
lon.set_major_formatter('d.dd')
lat.set_major_formatter('d.dd')

ax.legend()
plt.savefig('fig_coronagraph_starfield.pdf')
