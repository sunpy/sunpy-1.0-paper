import matplotlib.pyplot as plt
import sunpy.map
import sunpy.data.sample
from astropy import units as u
from astropy.coordinates import SkyCoord

my_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

top_right = SkyCoord(1200 * u.arcsec, 0 * u.arcsec, frame=my_map.coordinate_frame)
bottom_left = SkyCoord(500 * u.arcsec, -700 * u.arcsec, frame=my_map.coordinate_frame)
my_submap = my_map.submap(bottom_left, top_right)

fig = plt.figure(figsize=(12, 6))
ax0 = fig.add_subplot(1, 2, 1,  projection=my_map)
my_map.plot(clip_interval=(1, 99.99)*u.percent, axes=ax0)
my_map.draw_rectangle(bottom_left, 700*u.arcsec, 700*u.arcsec)
ax1 = fig.add_subplot(1, 2, 2, projection=my_submap)
my_submap.plot(clip_interval=(1, 99.7)*u.percent, title='', axes=ax1)
my_submap.draw_grid(axes=ax1)
plt.savefig('map_example.pdf', dpi=200)