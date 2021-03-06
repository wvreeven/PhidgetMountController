from reeven.van.astro.math import alignment_error_util
from astropy import units as u
from astropy.coordinates import (
    AltAz,
    Angle,
    EarthLocation,
    Longitude,
    Latitude,
    SkyCoord,
)
from astropy.time import Time
from unittest import TestCase


class Test(TestCase):
    def test_compute_alignment_error(self):
        lat = Angle((42 + (40 / 60)) * u.deg)
        s1 = SkyCoord(ra=3 * u.hourangle, dec=48 * u.degree)
        s2 = SkyCoord(ra=23 * u.hourangle, dec=45 * u.degree)
        err_ra = Angle(-12 * u.arcmin)
        err_dec = Angle(-21 * u.arcmin)
        delta_e, delta_a = alignment_error_util.compute_alignment_error(
            lat, s1, s2, err_ra, err_dec
        )
        self.assertAlmostEqual(delta_e.radian, Angle(7.3897 * u.arcmin).radian)
        self.assertAlmostEqual(delta_a.radian, Angle(32.2597 * u.arcmin).radian)

    def test_get_altaz_in_rotated_frame(self):
        delta_alt = Angle(7.3897 * u.arcmin)
        delta_az = Angle(32.2597 * u.arcmin)
        location = EarthLocation.from_geodetic(
            lon=Longitude("-71d14m12.5s"),
            lat=Latitude("-29d56m29.7s"),
            height=110.0 * u.meter,
        )
        sirius = SkyCoord.from_name("Sirius")
        time = Time("2020-04-15 20:49:48.560642")
        sirius_altaz = sirius.transform_to(AltAz(obstime=time, location=location))
        sirius_tel = alignment_error_util.get_altaz_in_rotated_frame(
            delta_alt=delta_alt,
            delta_az=delta_az,
            time=time,
            location=location,
            altaz=sirius_altaz,
        )
        self.assertAlmostEqual(sirius_tel.lon.deg, 50.36605878470352)
        self.assertAlmostEqual(sirius_tel.lat.deg, 70.33162741801904)
