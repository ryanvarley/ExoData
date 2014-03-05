""" Temp module until astro units are added to quantities
"""
import quantities as pq
from quantities.unitquantity import UnitConstant, UnitQuantity, UnitLength, UnitMass, UnitTime

L_s = solar_luminosity = UnitQuantity(
    'solar_luminosity',
    3.839*(10**26)*pq.W
)

R_s = solar_radius = UnitLength(
    'solar_radius',
    6.995 * (10**8) * pq.m,
    aliases=['solar_radii']
)

R_e = earth_radius = UnitLength(
    'earth_radius',
    6.371 * (10**6) * pq.m,
    aliases=['earth_radii']
)

R_j = jupiter_radius = UnitLength(
    'jupiter_radius',
    6.9911 * (10**7) * pq.m,
    aliases=['jupiter_radii']
)

M_s = solar_mass = UnitMass(
    'solar_mass', 1.99*(10**30)*pq.kg,
    aliases=['solar_masses']
)

M_e = earth_mass = UnitMass(
    'earth_mass', 5.97219*(10**24)*pq.kg,
    aliases=['earth_masses']
)

M_j = jupiter_mass = UnitMass(
    'jupiter_mass', 1.8986*(10**27)*pq.kg,
    aliases=['jupiter_masses']
)

Gyear = giga_year = UnitTime(
    'giga_year', 10**9*pq.year,
)

JulianDay = julian_day = JD = UnitTime(
    'julian_day', pq.day,
)
""" Note while quantities doesnt directly support units with an offset in most cases Julian Days are treated like days.
It is useful then to know if your working in Julian Days, MJD, BJD etc"""

ModifiedJulianDate = modified_julian_day = MJD = UnitTime(
    'modified_julian_day', pq.day,
)