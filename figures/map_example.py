import matplotlib.pyplot as plt
import sunpy.map
import sunpy.data.sample
from astropy import units as u
from astropy.coordinates import SkyCoord
from sunpy.net import hek
client = hek.HEKClient()


flares_hek = client.search(hek.attrs.Time('2011-06-07 00:00', '2011-06-07 23:59'),
                           hek.attrs.FL, hek.attrs.FRM.Name == 'SWPC')

# position of the flare from HEK
hpc_x, hpc_y = flares_hek[0].get('hpc_x'), flares_hek[0].get('hpc_y')

my_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)
# coordinate of flare from HEK for plotting
hpc_coord = SkyCoord(hpc_x*u.arcsec, hpc_y*u.arcsec, frame = my_map.coordinate_frame)

top_right = SkyCoord(1200 * u.arcsec, 0 * u.arcsec, frame=my_map.coordinate_frame)
bottom_left = SkyCoord(500 * u.arcsec, -700 * u.arcsec, frame=my_map.coordinate_frame)
my_submap = my_map.submap(bottom_left, top_right)

# plot the figure
fig = plt.figure(figsize=(12, 6))
plt.gcf().subplots_adjust(right=0.9)

ax0 = fig.add_subplot(1, 2, 1,  projection=my_map)
my_map.plot(clip_interval=(1, 99.99)*u.percent, axes=ax0)
ax0.plot_coord(hpc_coord, markersize = 6, marker = 'x', color = 'k', label = 'Flare location')
ax0.legend(loc='lower right') 

my_map.draw_rectangle(bottom_left, 700*u.arcsec, 700*u.arcsec)


ax1 = fig.add_subplot(1, 2, 2, projection=my_submap)
my_submap.plot(clip_interval=(1, 99.95)*u.percent, title='', axes=ax1)
my_submap.draw_grid(axes=ax1)
my_submap.draw_limb(axes=ax1)
cbar_ax = plt.gcf().add_axes([0.92, 0.145, 0.02, 0.7])
plt.colorbar(cax=cbar_ax)
plt.savefig('map_example.pdf', dpi=200)
