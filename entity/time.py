class Time:
    @staticmethod
    def get_attribute_string(attribute, isSeconds=False, isMinutes=False):
        if attribute == 0:
            if isMinutes:
                value = f"00:"
            elif isSeconds:
                value = "00"
            else:
                value = ""

        else:
            if attribute <= 9:
                value = f"0{attribute}"
            else:
                value = attribute

            if not isSeconds:
                value += ':'
        return value

    def __init__(self, value):
        self.hour = int(value // 3600)
        self.minutes = int((value % 3600) // 60)
        self.seconds = int((value % 3600) % 60)

    def __str__(self):
        return f"{Time.get_attribute_string(self.hour)}{Time.get_attribute_string(self.minutes, isMinutes=True)}{Time.get_attribute_string(self.seconds, isSeconds=True)}"

    def __repr__(self):
        return str(self)

    def get_seconds_value(self):
        return self.seconds + self.minutes * 60 + self.hour * 3600
