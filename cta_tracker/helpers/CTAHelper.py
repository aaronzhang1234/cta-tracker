import requests
import os
import datetime
import time

class CTAHelper:
    def get_locations_response(self):
        key = os.getenv("API_KEY")
        url = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={key}&rt=red,blue,brn,g,org,p,pink,y&outputType=JSON"
        cta_response = requests.get(url)
        return cta_response.json()

    def get_train_id(self, route_name, train_json):
        return "-".join([route_name,
                     train_json["trDr"],
                     train_json["rn"],
                     time.strftime("%Y%m%d")])

    def get_next_train_station(self, train_json):
        return train_json["nextStaId"], train_json["arrT"]

    def create_train_item(self, primary_key, route_name, train_json):
        nextStaId, arrivalTime = self.get_next_train_station(train_json)
        return {
            "train_identifier": primary_key,
            "route_name": route_name,
            "direction_code": train_json["trDr"],
            "route_number": train_json["rn"],
            "train_schedule": {nextStaId: arrivalTime},
            "delayed": train_json["isDly"],
            "created_timestamp": datetime.datetime.now().isoformat()
        }
