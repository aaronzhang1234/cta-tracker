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
        route_name, train_uuid = self.get_train_id(route_name, train)
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        next_sta_id, arrival_time = self.get_next_train_station(train)
        train_schedule = {
            self.get_previous_station(route_name, next_sta_id): current_datetime,
            next_sta_id: arrival_time
        }
        return {
            "train_identifier": route_name,
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

    def get_previous_station(self, route_name, next_sta_id):
        sta_route_order = route_order[route_name]
        station_index = sta_route_order.index(next_sta_id)
        if station_index == 0:
            return sta_route_order[0]
        return sta_route_order[station_index-1]

    def get_route_order(self, route):
        return route_order[route]


