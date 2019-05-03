import numpy as np
from sunpy import map
from sunpy.coordinates import frames

from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import os
from sunpy.coordinates import get_body_heliographic_stonyhurst
import sunpy_paper

files = ['aia.lev1.131A_2012-06-05T23_30_09.62Z.image_lev1.fits',
         'aia.lev1.193A_2012-06-05T23_30_07.84Z.image_lev1.fits',
         'aia.lev1.335A_2012-06-05T23_30_03.62Z.image_lev1.fits',
         'aia.lev1.1700A_2012-06-05T23_30_07.71Z.image_lev1.fits',
         'aia.lev1.4500A_2012-06-05T23_30_22.90Z.image_lev1.fits',
         'aia.lev1.4500A_2012-06-05T23_30_34.90Z.image_lev1.fits',
         'aia.lev1.171A_2012-06-05T23_30_12.34Z.image_lev1.fits',
         'aia.lev1.211A_2012-06-05T23_30_12.62Z.image_lev1.fits']

#files = ['aia.lev1.131A_2012-06-05T23_30_09.62Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.171A_2012-06-05T23_30_12.34Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.193A_2012-06-05T23_30_07.84Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.211A_2012-06-05T23_30_12.62Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.335A_2012-06-05T23_30_03.62Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.1700A_2012-06-05T23_30_07.71Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.4500A_2012-06-05T23_30_22.90Z.image_lev1.5.use_pnt_file.fits',
#         'aia.lev1.4500A_2012-06-05T23_30_34.90Z.image_lev1.5.use_pnt_file.fits']


for f in files:

    # get the data of interest and save fits files
    map1 = map.Map(os.path.join(sunpy_paper.data_dir, f))

    # now get venus position
    venus = get_body_heliographic_stonyhurst('venus', map1.date, observer=map1.observer_coordinate)
    venus_hpc = venus.transform_to(frames.Helioprojective(observer=map1.observer_coordinate))

    fig = plt.figure(figsize=(8, 11))

    ax1 = fig.add_subplot(1, 2, 1, projection=map1)
    map1.plot(axes=ax1, vmin=0)
    #print(f'{map1.data.min()} {map1.data.max()}')
    #print(map1.plot_settings)
    map1.draw_limb()

    #x and y plotting limits in arcsec
    lims_arcsec = ((-800, 200)*u.arcsec, (00, 1000)*u.arcsec)
    lims_pix_ax1 = map1.world_to_pixel(SkyCoord(*lims_arcsec, frame=map1.coordinate_frame))
    ax1.set_xlim(lims_pix_ax1[0].value)
    ax1.set_ylim(lims_pix_ax1[1].value)

    ax1.plot_coord(venus_hpc, 'x', color='white', fillstyle='none')
    #plt.colorbar()

    ax2 = fig.add_subplot(1, 2, 2, projection=map1)

    #x and y plotting limits in arcsec
    lims_arcsec = (((venus_hpc.Tx.value - 50, venus_hpc.Tx.value + 50)) * u.arcsec,
                   ((venus_hpc.Ty.value - 50, venus_hpc.Ty.value + 50) * u.arcsec))
    #print(lims_arcsec)
    lims_pix_ax1 = map1.world_to_pixel(SkyCoord(*lims_arcsec, frame=map1.coordinate_frame))
    ax2.set_xlim(lims_pix_ax1[0].value)
    ax2.set_ylim(lims_pix_ax1[1].value)
    map1.plot(axes=ax2, vmin=0)

    venus_hpc_pixel = map1.world_to_pixel(SkyCoord(venus_hpc.Tx, venus_hpc.Ty, frame=map1.coordinate_frame))
    #print(venus_hpc_pixel)

    ax2.plot_coord(venus_hpc, 'x', color='white', fillstyle='none', label='predicted')

    venus_radius = 6052 * u.km

    venus_angle = np.arctan(venus_radius / (map1.observer_coordinate.radius - venus.radius)).to('arcsec')

    adjust_xy = (4.5, -1.6)
    circle1 = plt.Circle((venus_hpc_pixel.x.value, venus_hpc_pixel.y.value),
                         venus_angle.value, color='white', fill=None)

    fit_x = venus_hpc_pixel.x.value + adjust_xy[0]
    fit_y = venus_hpc_pixel.y.value + adjust_xy[1]
    circle2 = plt.Circle((fit_x, fit_y),
                         47, color='red', fill=None)

    ax2.plot([fit_x], [fit_y], 'x', color='red',
             label=f'fit {adjust_xy[0]}, {adjust_xy[1]}')

    ax2.add_artist(circle1)
    ax2.add_artist(circle2)
    plt.legend()

    wave = str(int(map1.wavelength.value))
    time = map1.date.to_datetime().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'venus_transit_{wave}_{time}_prep.pdf', dpi=200)
    plt.close(fig)
