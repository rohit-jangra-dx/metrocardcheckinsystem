from enum import Enum
from pydantic import BaseModel
from typing import Literal, Tuple

class FareRate(Enum):
    ADULT = 200
    SENIOR_CITIZEN =  100
    KID = 50

FareRate

class MetroCard(BaseModel):
    card_id: str
    card_balance: int
    passenger_type: Literal['ADULT','SENIOR_CITIZEN','KID']
    travel_count: int
    
    @property
    def one_way_fare(self) -> int:
        return FareRate[self.passenger_type].value
    
    def check_in(self, travel_to: Literal['AIRPORT','CENTRAL']) -> Tuple[int, int]:
        
        # amount that is cut for the travel/ including the service fee
        amount_to_deduct = self.one_way_fare

        # values that are to be returned
        total_amount_of_transcation = amount_to_deduct
        discount_given = 0

        self.travel_count += 1

        if self.travel_count == 2:
            amount_to_deduct =  self.one_way_fare / 2
            discount_given = amount_to_deduct
            total_amount_of_transcation = amount_to_deduct

        # checking for the balance
        balance_after_deduction = self.card_balance - amount_to_deduct

        if  balance_after_deduction < 0:
            self.card_balance += abs(balance_after_deduction) 
            total_amount_of_transcation += 2 *(abs(balance_after_deduction) / 100)

        self.card_balance -= abs(balance_after_deduction)


        return int(total_amount_of_transcation), int(discount_given)