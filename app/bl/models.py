from dataclasses import dataclass, asdict


@dataclass
class City:
    geonameid: str
    name: str
    asciiname: str
    alternatenames: str
    latitude: str
    longitude: str
    featureclass: str
    featurecode: str
    countrycode: str
    cc2: str
    admin1code: str
    admin2code: str
    admin3code: str
    admin4code: str
    population: str
    elevation: str
    dem: str
    timezone: str
    modificationdate: str

    def object_as_dict(self):
        return asdict(self)
