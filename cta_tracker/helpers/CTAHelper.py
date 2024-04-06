import requests
import os

class CTAHelper:
    def get_locations_response(self):
        key = os.getenv("api_key")
        url = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={key}&rt=red,blue,brn,g,org,p,pink,y&outputType=JSON"
        cta_response = requests.get(url)
        response_json = cta_response.json()
        return response_json["ctatt"]["route"]

    def get_train_id(self, route_name, train_json):
        try:
            return "-".join([route_name,
                         train_json["trDr"],
                         train_json["rn"]])
        except Exception as e:
            print(train_json)
            print(e)
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
            "delayed": train_json["isDly"]
        }