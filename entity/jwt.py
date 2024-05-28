import json


class JWT:
    def __init__(self, jwt_as_json):
        jwt_as_dict = json.loads(jwt_as_json)
        self.access_token = jwt_as_dict["accessToken"]
        self.token_type = jwt_as_dict["tokenType"]
        self.scope = jwt_as_dict["scope"]
