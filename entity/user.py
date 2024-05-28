import json


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.saved = False

    def save_credentials(self):
        self.saved = True
        with open("files/user_credentials.json", "w") as file:
            json.dump(self.__dict__, file)

    @property
    def credentials_dict(self):
        return {"username": self.username, "password": self.password, "role": self.role, "saved": "true"}
