import os
import matplotlib.pyplot as plt
import sunpy.map
from sunpy.coordinates import get_body_heliographic_stonyhurst, frames

# look up stars in a star catalog
from astroquery.vizier import Vizier
from astropy import coordinates
import astropy.units as u
from astropy.coordinates import SkyCoord

from sunpy_paper import data_dir

f = '2014_05_15__07_54_00_005__STEREO-A_SECCHI_COR2_white-light.jp2'

path = os.path.join(data_dir, f)
map1 = sunpy.map.Map(path)

# finding the correct pointing location for the Sun as seen from STEREO
sun = SkyCoord(0*u.deg, 0*u.deg, 0*u.km, obstime=map1.date,frame=frames.HeliographicStonyhurst, observer='Earth')
stereo_icrs = map1.observer_coordinate.transform_to('icrs')
sun_icrs = sun.transform_to('icrs')
diff = sun_icrs.cartesian - stereo_icrs.cartesian
search_coord = SkyCoord(diff, frame='icrs')

vv=Vizier(columns=['**'], row_limit=-1, column_filters={'Gmag':'<7'}, timeout=1200)
vv.ROW_LIMIT = -1
result = vv.query_region(search_coord, radius=4 * u.deg, catalog='I/345/gaia2')

hpc_coords = []

for this_object in result[0]:
    tbl_crds = coordinates.SkyCoord(this_object['RA_ICRS'] * u.deg, this_object['DE_ICRS'] * u.deg, 1e12 * u.km, frame='icrs', obstime=map1.date)
    hpc_coords.append(tbl_crds.transform_to(frames.Helioprojective(observer=map1.observer_coordinate)))

# get the location of mars
mars = get_body_heliographic_stonyhurst('mars', map1.date, observer=map1.observer_coordinate)
mars_hpc = mars.transform_to(frames.Helioprojective(observer=map1.observer_coordinate))

# now plot
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1, projection=map1)

map1.plot(axes=ax1, vmin=0, vmax=400)

ax1.plot_coord(mars_hpc, 's', color='white', fillstyle='none', markersize=12, label='Mars')
for i, this_coord in enumerate(hpc_coords):
    ax1.plot_coord(this_coord, 'o', color='white', fillstyle='none')

plt.legend()
plt.savefig('coronagraph_starfield.pdf')
