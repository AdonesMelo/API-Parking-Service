from dj_rql.filter_cls import AutoRQLFilterClass

from parking.models import ParkingRecord, ParkingSpot


class ParkingFilterClass(AutoRQLFilterClass):
    MODEL = ParkingRecord


class ParkingSpotFilterClass(AutoRQLFilterClass):
    MODEL = ParkingSpot
    FILTERS = (
        'a_field',
        {
            'filter': 'license_plate',
            'source': 'vehicle__license_plate',
        },
    )
