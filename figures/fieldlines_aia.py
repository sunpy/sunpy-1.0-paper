"""
This example shows how to compute a PFSS solution from pfsspy, trace some field lines, and
overplot the traced field lines on an AIA 171 map.
Adapted from https://pfsspy.readthedocs.io/en/stable/auto_examples/plot_aia_overplotting.html
"""
import os

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.visualization import ImageNormalize, SqrtStretch
import matplotlib.pyplot as plt
import numpy as np
import sunpy.map
import sunpy.io.fits
import pfsspy
import pfsspy.coords

from sunpy_paper import data_dir

import sunpy_paper
# sunpy_paper.setup_plot()

###############################
#  Load GONG and AIA Data     #
###############################

# Load a GONG magnetic field map. The map date is 10/03/2019
[[br, header]] = sunpy.io.fits.read(
    os.path.join(data_dir, '190310t0014gong.fits'))
# The mean is subtracted to enforce div(B) = 0 on the solar surface
br = br - np.mean(br)
# GONG maps have their LH edge at -180deg in Carrington Longitude so roll to get it at 0deg.
br = np.roll(br, header['CRVAL1'] + 180, axis=1)

# Load the corresponding AIA 171 map
aia = sunpy.map.Map(os.path.join(
    data_dir, 'aia_lev1_171a_2019_03_10t00_00_09_35z_image_lev1.fits'))
# Crop to the desired active region
aia_submap = aia.submap(
    SkyCoord(Tx=300*u.arcsec, Ty=100*u.arcsec, frame=aia.coordinate_frame),
    SkyCoord(Tx=650*u.arcsec, Ty=450*u.arcsec, frame=aia.coordinate_frame),
)


###############################
#    Field Extrapolation      #
###############################

# Define the number of grid points in rho
nrho = 100
# And the source surface radius.
rss = 2.5
# Construct an `Input` object that stores this information
pfss_input = pfsspy.Input(br, nrho, rss, dtime=aia_submap.date)
# Compute the PFSS solution from the GONG magnetic field input
pfss_output = pfsspy.pfss(pfss_input)


###############################
#    Field Line Tracing       #
###############################

center_hgc = aia_submap.center.transform_to('heliographic_carrington')
# Construct a grid of seed points to trace some magnetic field lines
# These seed points are grouped about the center of the AR
s, phi = np.meshgrid(
    np.linspace(np.sin(center_hgc.lat)-0.07, np.sin(center_hgc.lat)+0.03, 15),
    np.deg2rad(np.linspace(center_hgc.lon.to(u.deg) - 7*u.deg,
                           center_hgc.lon.to(u.deg)+3*u.deg, 15)),
)
# Trace a field line for every seed point
flines = []
r = 0.01
for _s, _phi in zip(s.ravel(), phi.ravel()):
    x0 = np.array(pfsspy.coords.strum2cart(r, _s, _phi))
    flines.append(pfss_output.trace(x0, atol=1e-9, rtol=1e-5))


###############################
#           Plotting          #
###############################

# Plot the AIA map, along with the traced magnetic field lines. Inside the
# loop the field lines are converted to the AIA observer coordinate frame,
# and then plotted on top of the map.
fig = plt.figure(figsize=(5, 5))
ax = plt.subplot(1, 1, 1, projection=aia_submap)
aia_submap.plot(
    axes=ax,
    title=True,
    norm=ImageNormalize(vmin=0, vmax=2e3, stretch=SqrtStretch())
)
for f in flines:
    f_hpc = f.transform_to(aia_submap.coordinate_frame)
    if (
        np.any(f_hpc.Tx < aia_submap.bottom_left_coord.Tx) or
        np.any(f_hpc.Ty < aia_submap.bottom_left_coord.Ty) or
        np.any(f_hpc.Tx > aia_submap.top_right_coord.Tx) or
        np.any(f_hpc.Ty > aia_submap.top_right_coord.Ty)
    ):
        continue
    ax.plot_coord(f_hpc, alpha=0.4, linewidth=1, color='black')
ax.grid(alpha=0)
lon, lat = ax.coords
# Save figure
fig.savefig('fig_fieldlines_aia.pdf')
