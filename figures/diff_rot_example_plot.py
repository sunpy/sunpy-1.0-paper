from sunpy import map
from sunpy.physics import differential_rotation
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import os
import sunpy_paper

# get the data of interest and save fits files
map1 = map.Map(os.path.join(sunpy_paper.data_dir, 'aia_lev1_1600a_2014_10_20t00_00_16_13z_image_lev1.fits'))
map2 = map.Map(os.path.join(sunpy_paper.data_dir, ' aia_lev1_1600a_2014_10_22t00_00_16_12z_image_lev1.fits'))

#rotate map at 2014-10-20 to day of 2014-10-22
rotated_map = differential_rotation.diffrot_map(map1, time=map2.date)

#plotting the data
vmin = 50
vmax = 7000

fig = plt.figure(figsize=(8,11))
ax1 = fig.add_subplot(3,1,1, projection=map1)
ax2 = fig.add_subplot(3,1,2, projection=map2, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(3,1,3, projection=rotated_map, sharex=ax1, sharey=ax1)

#plot maps
map1.plot(vmin=vmin, vmax=vmax, axes=ax1, title='AIA 1600 $\mathrm{\AA}$')
map2.plot(vmin=vmin, vmax=vmax, axes=ax2, title='')
rotated_map.plot(vmin=vmin, vmax=vmax, axes=ax3, title='')

#trun off ticklabels for top and middle plot
ax1.tick_params(axis='x',  labelbottom=False)
ax2.tick_params(axis='x',labelbottom=False)

#x and y plotting limits in arcsec
lims_arcsec = ((-1001, 1000)*u.arcsec, (-1000, 0)*u.arcsec)
lims_pix_ax1 = map1.world_to_pixel(SkyCoord(*lims_arcsec, frame=map1.coordinate_frame))
ax1.set_xlim(lims_pix_ax1[0].value)
ax1.set_ylim(lims_pix_ax1[1].value)

for axx in [ax1, ax2, ax3]:
    axx.grid(False)
    axx.set_xlabel('')
    axx.set_ylabel('Arcsec (Y)')

ax3.set_xlabel('Arcsec (X)')

#titles for each subplot
ax1.text(0.03, 0.92, 'a. ' + str(map1.date)[0:10], color='w', fontsize=10, transform=ax1.transAxes)
ax2.text(0.03, 0.92, 'b. ' + str(map2.date)[0:10], color='w', fontsize=10, transform=ax2.transAxes)
ax3.text(0.03, 0.92, 'c. Rotated map a. to time of b.', color='w', fontsize=10, transform=ax3.transAxes)

#define arrow coordinates in pixels
arrows1_pix = map1.world_to_pixel(SkyCoord((-730, -500)*u.arcsec, (450, -400)*u.arcsec, frame=map1.coordinate_frame))
arrows2_pix = map2.world_to_pixel(SkyCoord((-390, -500)*u.arcsec, (780, -400)*u.arcsec, frame=map2.coordinate_frame))
arrows3_pix = rotated_map.world_to_pixel(SkyCoord((-390, -500)*u.arcsec, (780, -400)*u.arcsec, frame=rotated_map.coordinate_frame))

#draw arrows
ax1.arrow(arrows1_pix[0][0].value, arrows1_pix[0][1].value, 0, 180, head_width=30, color='r')
ax1.arrow(arrows1_pix[1][0].value, arrows1_pix[1][1].value, 0, 180, head_width=30, color='w')

ax2.arrow(arrows2_pix[0][0].value, arrows2_pix[0][1].value, 0, 180, head_width=30, color='r')
ax2.arrow(arrows2_pix[1][0].value, arrows2_pix[1][1].value, 0, 180, head_width=30, color='w')

ax3.arrow(arrows3_pix[0][0].value, arrows3_pix[0][1].value, 0, 180, head_width=30, color='r')
ax3.arrow(arrows3_pix[1][0].value, arrows3_pix[1][1].value, 0, 180, head_width=30, color='w')

fig.tight_layout()
fig.subplots_adjust(hspace=0.01, left=0.1, bottom=0.05, right=0.97, top=0.95)
plt.savefig('diff_rot_1600.pdf', dpi=200)


