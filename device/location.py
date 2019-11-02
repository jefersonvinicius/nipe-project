from plyer import gps

class Location:

    def __init__(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except Exception:
            print("Error in start gps")

    def on_location(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'lon':
                self.lon = v
            elif k == 'lat':
                self.lat = v

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon