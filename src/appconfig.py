from enum import Enum
from typing import Literal

PassengerType = Literal['ADULT','SENIOR_CITIZEN','KID']

StationType = Literal['AIRPORT','CENTRAL']

class FareRate(Enum):
    ADULT = 200
    SENIOR_CITIZEN =  100
    KID = 50