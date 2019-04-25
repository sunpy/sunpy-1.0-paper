from sunpy import map
from sunpy.coordinates import frames

from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import os
from sunpy.coordinates import get_body_heliographic_stonyhurst
import sunpy_paper

sunpy_paper.setup_plot()

# get the data of interest and save fits files
map1 = map.Map(os.path.join(sunpy_paper.data_dir, 'aia.lev1.4500A_2012-06-05T23_30_34.90Z.image_lev1.fits'))

# now get venus position
venus = get_body_heliographic_stonyhurst('venus', map1.date, observer=map1.observer_coordinate)

venus_hpc = venus.transform_to(frames.Helioprojective(observer=map1.observer_coordinate))
fig = plt.figure(figsize=(8, 11))
ax1 = fig.add_subplot(1, 1, 1, projection=map1)
map1.plot(axes=ax1)
map1.draw_limb()

#x and y plotting limits in arcsec
lims_arcsec = ((-800, 200)*u.arcsec, (00, 1000)*u.arcsec)
lims_pix_ax1 = map1.world_to_pixel(SkyCoord(*lims_arcsec, frame=map1.coordinate_frame))
ax1.set_xlim(lims_pix_ax1[0].value)
ax1.set_ylim(lims_pix_ax1[1].value)

ax1.plot_coord(venus_hpc, 'x', color='white', fillstyle='none')


plt.savefig('venus_transit.pdf', dpi=200)


