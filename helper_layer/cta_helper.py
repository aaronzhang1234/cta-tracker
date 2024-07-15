import requests
import os
import datetime
import uuid
from stations import route_order, station_dict

class CTAHelper:
    def get_locations_response(self):
        key = os.getenv("API_KEY")
        url = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={key}&rt=red,blue,brn,g,org,p,pink,y&outputType=JSON"
        cta_response = requests.get(url)
        return cta_response.json()

    def get_train_id(self, route_name, train_json):
        primary_key = "-".join([route_name,
                     train_json["trDr"]])
        hash_key = str(uuid.uuid4())
        return primary_key, hash_key

    def get_next_train_station(self, train_json):
        return train_json["nextStaId"], train_json["arrT"]

    def create_train_item(self, route_name, train):
        train_identifier, train_uuid = self.get_train_id(route_name, train)
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        nextStaId, arrivalTime = self.get_next_train_station(train)
        train_schedule = {
            self.get_first_station(train_identifier): current_datetime.isoformat(),
            nextStaId: arrivalTime
        }
        return {
            "train_identifier": train_identifier,
            "train_uuid": train_uuid,
            "route_name": route_name,
            "direction_code": train["trDr"],
            "route_number": train["rn"],
            "train_date": current_date,
            "train_schedule": train_schedule,
            "delayed": train["isDly"],
            "created_timestamp": current_datetime.isoformat(),
            "last_updated_date": current_datetime.isoformat(),
            "last_updated_epoch": current_datetime.strftime("%s")
        }
    def get_first_station(self, route):
        return route_order[route][0]

    def get_route_order(self, route):
        return route_order[route]


