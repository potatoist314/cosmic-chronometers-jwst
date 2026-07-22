J/ApJS/239/27    LEGA-C DR2: galaxies in the COSMOS field    (Straatman+, 2018)
================================================================================
The Large Early Galaxy Astrophysics Census (LEGA-C) data release 2: dynamical
and stellar population properties of z<~1 galaxies in the COSMOS field.
    Straatman C.M.S., van der Wel A., Bezanson R., Pacifici C., Gallazzi A.,
    Wu P.-F., Noeske K., Barisic I., Bell E.F., Brammer G.B., Calhau J.,
    Chauke P., Franx M., van Houdt J., Labbe I., Maseda M.V.,
    Munoz-Mateos J.C., Muzzin A., van de Sande J., Sobral D., Spilker J.S.
   <Astrophys. J. Suppl. Ser., 239, 27-27 (2018)>
   =2018ApJS..239...27S    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Galaxies, spectra; Velocity dispersion; Redshifts;
              Equivalent widths; Surveys; Optical
Mission_Name: ESO
Keywords: catalogs; galaxies: evolution; surveys; techniques: spectroscopic

Abstract:
    We present the second data release of the Large Early Galaxy
    Astrophysics Census (LEGA-C), an ESO 130-night public spectroscopic
    survey conducted with VIMOS on the Very Large Telescope. We release
    1988 spectra with typical continuum S/N~20{AA}^-1^ of galaxies at
    0.6<~z<~1.0, each observed for ~20hr and fully reduced with a
    custom-built pipeline. We also release a catalog with spectroscopic
    redshifts, emission-line fluxes, Lick/IDS indices, and observed
    stellar and gas velocity dispersions that are spatially integrated
    quantities, including both rotational motions and genuine dispersion.
    To illustrate the new parameter space in the intermediate-redshift
    regime probed by LEGA-C, we explore relationships between dynamical
    and stellar population properties. The star-forming galaxies typically
    have observed stellar velocity dispersions of ~150km/s and strong
    H{delta} absorption (H{delta}_A_~5{AA}), while passive galaxies have
    higher observed stellar velocity dispersions (~200km/s) and weak
    H{delta} absorption (H{delta}_A_~0{AA}). Strong [OIII]5007/H{beta}
    ratios tend to occur mostly for galaxies with weak H{delta}_A_ or
    galaxies with higher observed velocity dispersion. Beyond these broad
    trends, we find a diversity of possible combinations of rest-frame
    colors, absorption-line strengths, and emission-line detections,
    illustrating the utility of spectroscopic measurements to more
    accurately understand galaxy evolution.

Description:
    From 2014 December to 2018 March, 20hr deep integrations have been
    obtained for over 4000 targets with the Visible Multi-Object
    Spectrograph (VIMOS) on the Very Large Telescope at Paranal in
    Chile.
    The Large Early Galaxy Astrophysics Census (LEGA-C) survey strategy
    and science goals have been presented by van der Wel+
    (2016ApJS..223...29V), accompanied by a first release of 892 spectra
    and corresponding spectroscopic redshifts. In this paper we present
    Data Release II (DR2).

    The primary targets are chosen from a Ks-band magnitude-selected
    parent sample of ~10000 galaxies with photometric redshifts z=0.6-1
    drawn from the Ultra Deep Survey with the VISTA telescope (UltraVISTA)
    catalog (Muzzin+ 2013, J/ApJS/206/8), which overlaps for the most part
    with the already extensively photometrically covered COSMOS field
    (Figure 1).

    In this release we present the data from masks 1 through 15 out of the
    total 32 masks which were observed during the ESO observing periods 94
    to 98, from 2014 December to 2017 January.

File Summary:
--------------------------------------------------------------------------------
 FileName     Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe           80        .   This file
legacdr2.dat    670     1988   Large Early Galaxy Census (LEGA-C)
                                 spectroscopic survey DR2 catalog
sp/*              .     1988   Individual reduced 1D spectra in FITS format
--------------------------------------------------------------------------------

See also:
 III/250 : The VIMOS VLT deep survey (VVDS-DEEP) (Le Fevre+ 2005)
 J/ApJS/234/21  : Hectospec survey of galaxies in COSMOS (Damjanov+, 2018)
 J/ApJ/830/51   : FourStar galaxy evolution survey (ZFOURGE) (Straatman+, 2016)
 J/ApJ/799/148  : DEIMOS galaxy sample at z~0.7 (Bezanson+, 2015)
 J/ApJ/795/165  : Line ratios in z~2-3 gal. from KBSS-MOSFIRE (Steidel+, 2014)
 J/ApJS/214/24  : 3D-HST+CANDELS catalog (Skelton+, 2014)
 J/MNRAS/442/533  : Recently quenched elliptical gal. in SDSS (McIntosh+, 2014)
 J/ApJ/788/72   : Observed sample of z~0.7 massive galaxies (Gallazzi+, 2014)
 J/ApJ/777/18   : Stellar mass functions of galaxies to z=4 (Muzzin+, 2013)
 J/ApJ/771/85   : Dynamical masses of z~2 quiescent gal. (van de Sande+, 2013)
 J/ApJS/206/8   : COSMOS/UltraVISTA Ks-selected catalogs v4.1 (Muzzin+, 2013)
 J/AJ/145/77    : Imaging and spectroscopy in 3 gal. clusters (Jorgensen+, 2013)
 J/MNRAS/396/818  : Blue early-type galaxies in Galaxy Zoo (Schawinski+, 2009)
 J/A+A/499/47   : Lick indices of EDCSN galaxies (Sanchez-Blazquez+, 2009)
 J/ApJS/172/70  : zCOSMOS-bright catalog (Lilly+, 2007)
 J/ApJ/665/1067 : Velocities in Cl 0024+16 and MS 0451-03 (Moran+, 2007)
 J/ApJ/633/174  : Spheroidals and bulge dominated galaxies (Treu+, 2005)
 J/ApJS/111/377 : H{gamma} + H{delta} absorption features (Worthey+ 1997)
 J/ApJS/94/687  : Old stellar populations. V. (Worthey+, 1994)
 http://www.mpia.de/home/legac/ : LEGA-C survey data releases page

Byte-by-byte Description of file: legacdr2.dat
--------------------------------------------------------------------------------
   Bytes Format Units       Label      Explanations
--------------------------------------------------------------------------------
   1-  6  I6    ---         [MMS2013]  [25061/262197] UltraVISTA ID (OBJECT)
   8- 17  A10   ---         SpID       Unique identifier (mask no.+object ID)
                                        (SPECT_ID)
  19- 27  F9.5  deg         RAdeg      [149.7/150.8] Right ascension (J2000)
                                        (RAJ2000)
  29- 35  F7.5  deg         DEdeg      [1.7/2.9] Declination (J2000) (DECJ2000)
  37- 44  F8.6  ---         z          [0.1/2.5]? Spectroscopic redshift (z)
  46- 71  A26   ---         Filename   FITS file name of the original spectrum
                                        in subdirectory sp (Filename)
  73- 78  F6.1  km/s        sigma*     [0.2/1000]?=- Velocity dispersion of the
                                        stellar component (SIGMA_STARS_PRIME)
  80- 87  E8.3  km/s      e_sigma*     [0/4.7e+12]?=- sigma* uncertainty
                                        (SIGMA_STARS_PRIME_err)
  89- 93  F5.1  km/s        sigmaGas   [1.6/400]? Velocity dispersion of the
                                        gaseous component (SIGMA_GAS_PRIME)
  95- 99  F5.1  km/s      e_sigmaGas   [0.2/587]? sigmaGas uncertainty
                                        (SIGMA_GAS_PRIME_err)
 101-109  F9.6  0.1nm       CN1        [-2.9/0.3]?=- Lick/IDS absorption index
                                        CN1 (LICK_CN1)
 111-120  F10.6 0.1nm     e_CN1        [0.0008/364]?=- CN1 uncertainty
                                        (LICK_CN1_err)
 122-130  F9.6  0.1nm       CN2        [-1.4/0.4]?=- Lick/IDS absorption index
                                        CN2 (LICK_CN2)
 132-139  F8.6  0.1nm     e_CN2        [0.0008/4.6]?=- CN2 uncertainty
                                        (LICK_CN2_err)
 141-150  F10.6 0.1nm       CA4227     [-7.1/445]?=- Lick/IDS absorption index
                                        Ca4227 (LICK_CA4227)
 152-164  F13.6 0.1nm     e_CA4227     [0.0001/933676]?=- CA4227 uncertainty
                                        (LICK_CA4227_err)
 166-175  F10.6 0.1nm       G4300      [-36.5/17.3]?=- Lick/IDS absorption index
                                        G4300 (LICK_G4300)
 177-186  F10.6 0.1nm     e_G4300      [0.0002/140]?=- G4300 uncertainty
                                        (LICK_G4300_err)
 188-197  F10.6 0.1nm       FE4383     [-65/25.5]?=- Lick/IDS absorption index
                                        Fe4383 (LICK_FE4383)
 199-208  F10.6 0.1nm     e_FE4383     [0.0003/282]?=- FE4383 uncertainty
                                        (LICK_FE4383_err)
 210-220  F11.6 0.1nm       CA4455     [-250/24]?=- Lick/IDS absorption index
                                        Ca4455 (LICK_CA4455)
 222-234  F13.6 0.1nm     e_CA4455     [0.0002/291787]?=- CA4455 uncertainty
                                        (LICK_CA4455_err)
 236-246  F11.6 0.1nm       FE4531     [-39.3/1552]?=- Lick/IDS absorption index
                                        Fe4531 (LICK_FE4531)
 248-261  F14.6 0.1nm     e_FE4531     [0.0004/6.5e+06]?=- FE4531 uncertainty
                                        (LICK_FE4531_err)
 263-273  F11.6 0.1nm       C4668      [-229.3/41.1]?=- Lick/IDS absorption
                                        index C4668 (LICK_C4668)
 275-284  F10.6 0.1nm     e_C4668      [0.002/414]?=- C4668 uncertainty
                                        (LICK_C4668_err)
 286-295  F10.6 0.1nm       HB         [-29.4/50]?=- Lick/IDS absorption index
                                        H{beta} (LICK_HB)
 297-306  F10.6 0.1nm     e_HB         [0.0003/128]?=- HB uncertainty
                                        (LICK_HB_err)
 308-317  F10.6 0.1nm       HDA        [-17.5/50.3]?=- Lick/IDS absorption index
                                        H{delta}_A_ (LICK_HD_A)
 319-328  F10.6 0.1nm     e_HDA        [0.0008/409]?=- HDA uncertainty
                                        (LICK_HD_A_err)
 330-339  F10.6 0.1nm       HGA        [-97.1/29.1]?=- Lick/IDS absorption index
                                        H{gamma}_A_ (LICK_HG_A)
 341-350  F10.6 0.1nm     e_HGA        [0.003/550]?=- HGA uncertainty
                                        (LICK_HG_A_err)
 352-361  F10.6 0.1nm       HDF        [-11.5/57.5]?=- Lick/IDS absorption index
                                        H{delta}_F_ (LICK_HD_F)
 363-372  F10.6 0.1nm     e_HDF        [0.0008/138]?=- HDF uncertainty
                                        (LICK_HD_F_err)
 374-383  F10.6 0.1nm       HGF        [-16/18.2]?=- Lick/IDS absorption index
                                        H{gamma}_F_ (LICK_HG_F)
 385-393  F9.6  0.1nm     e_HGF        [0.0002/71]?=- HGH uncertainty
                                        (LICK_HG_F_err)
 395-402  F8.6  0.1nm       D4000N     [0.3/2.8]?=- Lick/IDS absorption index
                                        D4000_n_ (LICK_D4000_N)
 404-411  F8.6  0.1nm     e_D4000N     [0.0003/0.8]?=- D4000N uncertainty
                                        (LICK_D4000_N_err)
 413-422  F10.3 10-22W/m2   FHd        [0.1/114509]?=- H{delta} emission-line
                                        flux (Hd_flux)
 424-432  F9.3  10-22W/m2 e_FHd        [0.006/39719]?=- FHd uncertainty (Hd_err)
 434-440  F7.3  0.1nm       EWHd       [-45.6/-0.001]?=- H{delta} equivalent
                                        width (Hd_EW)
 442-446  F5.3  0.1nm     e_EWHd       [0.002/9]?=- EWHd uncertainty (Hd_EW_err)
 448-456  F9.3  10-22W/m2   FHg        [0.1/19018]?=- H{gamma} emission-line
                                        flux (Hg_flux)
 458-468  F11.3 10-22W/m2 e_FHg        [0.01/9.8e+06]?=- FHg uncertainty
                                        (Hg_err)
 470-476  F7.3  0.1nm       EWHg       [-60.3/-0.01]?=- H{gamma} equivalent
                                        width (Hg_EW)
 478-487  F10.3 0.1nm     e_EWHg       [0.004/172142]?=- EWHg uncertainty
                                        (Hg_EW_err)
 489-496  F8.3  10-22W/m2   FHb        [0.05/4235]?=- H{beta} emission-line
                                        flux (Hb_flux)
 498-505  F8.3  10-22W/m2 e_FHb        [0.02/2182]?=- FHb uncertainty (Hb_err)
 507-513  F7.3  0.1nm       EWHb       [-41.1/-0.001]?=- H{beta} equivalent
                                        width (Hb_EW)
 515-520  F6.3  0.1nm     e_EWHb       [0.005/22.5]?=- EWHb uncertainty
                                        (Hb_EW_err)
 522-530  F9.3  10-22W/m2   FOII3727   [1/25273]?=- [OII] emission-line flux
                                        (OII_3727_flux)
 532-540  F9.3  10-22W/m2 e_FOII3727   [0.2/46099]?=- FOII3727 uncertainty
                                        (OII_3727_err)
 542-549  F8.3  0.1nm       EWOII3727  [-125.1/-0.05]?=- [OII] equivalent width
                                        (OII_3727_EW)
 551-556  F6.3  0.1nm     e_EWOII3727  [0.004/12]?=- EWOII3727 uncertainty
                                        (OII_3727_EW_err)
 558-565  F8.3  10-22W/m2   FOIII4959  [0.07/5612]?=- [OIII]4959 emission-line
                                        flux (OIII_4959_flux)
 567-575  F9.3  10-22W/m2 e_FOIII4959  [0.008/89204]?=- FOIII4959 uncertainty
                                        (OIII_4959_err)
 577-583  F7.3  0.1nm       EWOIII4959 [-58.2/-0.01]?=- [OIII]4959 equivalent
                                        width (OIII_4959_EW)
 585-592  F8.3  0.1nm     e_EWOIII4959 [0.02/1190]?=- EWOIII4959 uncertainty
                                        (OIII_4959_EW_err)
 594-602  F9.3  10-22W/m2   FOIII5007  [0.1/10524]?=- [OIII]5007 emission-line
                                        flux (OIII_5007_flux)
 604-611  F8.3  10-22W/m2 e_FOIII5007  [0.06/3235]?=- FOIII5007 uncertainty
                                        (OIII_5007_err)
 613-619  F7.3  0.1nm       EWOIII5007 [-99.4/-0.03]?=- [OIII]5007 equivalent
                                        width (OIII_5007_EW)
 621-625  F5.3  0.1nm     e_EWOIII5007 [0.002/7]?=- [OIII]5007 uncertainty
                                        (OIII_5007_EW_err)
     627  I1    ---         Fppxf      [0/1] pPXF fit quality flag (0: good fit)
                                        (f_ppxf)
     629  I1    ---       f_z          [0/1] Redshift flag
                                        (0=redshift detected)
     631  I1    ---         Fsp        [0/1] Spectral quality flag
                                        (0=good spectrum) (f_spec)
     633  I1    ---         Fprim      [0/1] Primary source flag
                                        (1=source primary) (f_primary)
     635  I1    ---         Use        [0/1] General quality flag
                                        (1=good to use) (f_use)
     637  I1    ---         Fint       [0/1] Interpretation flag
                                        (0=no issues) (f_int)
 639-646  F8.4  ---         Tcor       [2.9/220.1]? Total completeness
                                        correction
 648-654  F7.1  pix-1       S/N        [0.2/57083]? Overall median S/N (SN)
 656-662  F7.1  pix-1       SN4000     [0/73431]? S/N at rest-frame 4000{AA}
                                        (SN_RF_4000)
 664-670  F7.1  pix-1       SN8030     [0/53043]? S/N at observed frame 8030{AA}
                                        (SN_OBS_8030)
--------------------------------------------------------------------------------

History:
    FITS catalogue downloaded from http://www.eso.org/qi/catalog/show/235/
    Spectra downloaded from http://www.mpia.de/home/legac/

References:
    van der Wel et al.   Paper I.   2016ApJS..223...29V

================================================================================
(End)                                     Emmanuelle Perret [CDS]    18-Feb-2019
