"""
==============================================
Overplotting the position of the Venus transit
==============================================

How to accurately plot the position of Venus as it transitted in front
of the Sun as observed by SDO/AIA.
"""
import matplotlib.pyplot as plt
import numpy as np

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import solar_system_ephemeris
from astropy.utils.data import download_file

import sunpy.map
from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.visualization.wcsaxes import SphericalCircle

###############################################################################
# Let's download an image of the Venus transit.
f = download_file(
    "http://jsoc.stanford.edu/data/events/Venus_AIA24s_1600/Out/fits/20120606_040731_UTC.0041.fits"
)
aiamap = sunpy.map.Map(f)

###############################################################################
# For this example, we require high precision ephemeris information. The built-in
# ephemeris provided by astropy are not accurate enough. This requires jplephem
# to be installed.
solar_system_ephemeris.set("jpl")
venus_radius = 6051.8 * u.km
###############################################################################
# Now we get the position of venus and convert it into the SDO/AIA coordinates.
venus = get_body_heliographic_stonyhurst(
    "venus", aiamap.date, observer=aiamap.observer_coordinate
)
venus_hpc = venus.transform_to(aiamap.coordinate_frame)

earth = get_body_heliographic_stonyhurst(
    "earth", aiamap.date, observer=aiamap.observer_coordinate
)

venus_angular_extent = np.arctan(venus_radius / (earth.radius - venus.radius)).to(
    "arcsec"
)

###############################################################################
# Let's crop the image with Venus at it's center.
fov = 100 * u.arcsec
top_right = SkyCoord(
    venus_hpc.Tx + fov, venus_hpc.Ty + fov, frame=aiamap.coordinate_frame
)
bottom_left = SkyCoord(
    venus_hpc.Tx - fov, venus_hpc.Ty - fov, frame=aiamap.coordinate_frame
)
smap = aiamap.submap(top_right, bottom_left)

###############################################################################
# Let's plot the results.
ax = plt.subplot(111, projection=smap)
smap.plot()
smap.draw_limb()
ax.grid(False)
ax.plot_coord(venus_hpc, "x", color="deepskyblue", label="Venus")

r = SphericalCircle(
    (venus_hpc.Tx, venus_hpc.Ty),
    venus_angular_extent,
    edgecolor="deepskyblue",
    facecolor="none",
    transform=ax.get_transform("world"),
)
ax.add_patch(r)
plt.legend()
plt.savefig("fig_venus_transit.pdf", dpi=200)
plt.close()
