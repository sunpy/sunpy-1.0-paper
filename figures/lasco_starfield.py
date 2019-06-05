from astropy import coordinates
from astroquery.vizier import Vizier
import sunpy.map
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames
import astropy.units as u
from astropy.time import Time

import sunpy_paper
sunpy_paper.setup_plot()

# image from helioviewer
f = '../data/2000_02_27__07_42_05_810__SOHO_LASCO_C3_white-light.jp2'

lasco = sunpy.map.Map(f)
sun = SkyCoord(0*u.deg, 0*u.deg, 0*u.km, obstime=lasco.date,
               frame=frames.HeliographicStonyhurst)
sun.transform_to('gcrs')

# look up stars in a star catalog

# gaia
vv = Vizier(columns=['**'], row_limit=-1, column_filters={'Gmag': '<7'})
vv.ROW_LIMIT = -1
result = vv.query_region(SkyCoord(ra=sun.transform_to('gcrs').ra, dec=sun.transform_to(
    'gcrs').dec, unit=(u.deg, u.deg), frame='icrs'), radius=6*u.deg, catalog='I/345/gaia2')

# the following information is missing from the header
correct_lasco_observer = SkyCoord(359.81847756 * u.deg, -7.15574196 *
                                  u.deg, 1.46871806e+08 * u.km, frame=frames.HeliographicStonyhurst)

hpc_coords = []
source = []

for this_object in result[0]:
    tbl_crds = coordinates.SkyCoord(
        this_object['RAJ2000'] * u.deg, this_object['DEJ2000'] * u.deg, 1e12 * u.km, frame='icrs', obstime=lasco.date)
    source.append(this_object['Source'])
    hpc_coords.append(tbl_crds.transform_to(
        frames.Helioprojective(observer=correct_lasco_observer)))

fig = plt.figure(figsize=(20, 20))
ax1 = fig.add_subplot(1, 1, 1, projection=lasco)
lasco.plot(axes=ax1)
lasco.draw_limb()
for this_coord in hpc_coords:
    ax1.plot_coord(SkyCoord(this_coord.Tx, this_coord.Ty, obstime=lasco.date,
                            frame=frames.Helioprojective), 'o', color='red', fillstyle='none')
ax1.plot_coord(sun, 'x')
plt.savefig('lasco_starfield.pdf')
