from pydantic import BaseModel
from typing import TypedDict, Literal, Dict
from src.MetroCard import MetroCard

# types 
class CardInfoMap(TypedDict):
    card_id: str
    card_balance: int
    passenger_type: Literal['ADULT','KID', 'SENIOR_CITIZEN',None]
    travel_record: list[Literal['AIRPORT','CENTERAL']]

CardInfoMapDict = Dict[str, CardInfoMap]

class PassengerTypeSummary(TypedDict):
    ADULT: int
    SENIOR_CITIZEN: int
    KID: int

class StationMetrics(TypedDict):
    amount_collected: int
    discount_given: int
    passenger_type_summary: PassengerTypeSummary

class TotalCollection(TypedDict):
            CENTRAL: StationMetrics 
            AIRPORT: StationMetrics
    


class CheckInSystem(BaseModel):
    fileInput: list[str]
    
    @property
    def card_info_map(self) -> CardInfoMapDict:
        card_info_map: CardInfoMapDict= {} 
        
        for str in self.fileInput:
            if str.find('BALANCE') != -1:
                _, card_id, card_balance = str.split()
                card_balance = int(card_balance)

                if card_id not in card_info_map:
                    card_info_map[card_id] = {
                        'card_balance':card_balance,
                        'card_id':card_id,
                        'passenger_type':None,
                        'travel_record':[]
                        }
        
        for str in self.fileInput:
            if str.find('CHECK_IN') != -1:
                _, card_id, passenger_type, destination = str.split()
               
                if card_id in card_info_map:
                    card_info_map[card_id]['passenger_type'] = passenger_type
                    card_info_map[card_id]['travel_record'].append(destination)
        
        return card_info_map
    
    @property
    def metrics_summary_obj(self) -> TotalCollection:

        total_collection: TotalCollection = {
             'AIRPORT':{
                  'amount_collected':0,
                  'discount_given':0,
                  'passenger_type_summary':{
                       'ADULT':0,
                       'KID':0,
                       'SENIOR_CITIZEN':0
                  }
             },
             'CENTRAL':{
                  'amount_collected':0,
                  'discount_given': 0,
                  'passenger_type_summary': {
                       'ADULT':0,
                       'KID':0,
                       'SENIOR_CITIZEN':0
                  }
             }
        }

        filtered_data = {k: v for k, v  in self.card_info_map.items() if v['passenger_type'] != None}

        for key, obj in filtered_data.items():
        
            #creating the metro card
            metro_card = MetroCard(card_id=key, card_balance= obj['card_balance'],passenger_type=obj['passenger_type'],travel_count= 0)

            #now calculating the total transcactions done through the card

            for travel_record in obj['travel_record']:
                
                # entering the passenger metrics
                total_collection[travel_record]['passenger_type_summary'][obj['passenger_type']] += 1
                
                amount_spent, discont_given =metro_card.check_in(travel_record)
                
                # entering the discount metrics
                total_collection[travel_record]['discount_given'] += discont_given

                #entering the amount collected metrics
                total_collection[travel_record]['amount_collected'] += amount_spent

        return total_collection
    
    def print_summary(self,station:Literal['AIRPORT','CENTRAL']) -> None:
        
        formatted_output = f"TOTAL_COLLECTION    {station}  {self.metrics_summary_obj[station]['amount_collected']}  {self.metrics_summary_obj[station]['discount_given']}"
        print(formatted_output)
        print("PASSENGER_TYPE_SUMMARY")

        #removing the unwanted keys value < 0
        filtered_data = {k: v for k, v in self.metrics_summary_obj[station]['passenger_type_summary'].items() if v > 0}
        
        #sorted the data in descending order
        sorted_items = sorted(filtered_data.items(), key=lambda item: item[1], reverse=True)

        for key, value in sorted_items:
            formatted_str = f"{key}  {value}"
            print(formatted_str)

