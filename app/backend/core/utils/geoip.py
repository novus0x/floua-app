########## Modules ##########
import geoip2.database

from pathlib import Path

########## Variables ##########
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MMDB_PATH = BASE_DIR / "db" / "geoip.mmdb"

########## DB ##########
reader = geoip2.database.Reader(str(MMDB_PATH))

########## Get location ##########
def lookup_ip(ip: str):
    try:
        response = reader.city(ip)
        return {
            "country": response.country.name,
            "region": response.subdivisions[0].name if response.subdivisions else None,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
            "continent": response.continent.name,
        }
    except Exception as e:
        print(e)
        return None
