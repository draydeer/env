
class StorageRoute:

    driver = None
    projection = None

    def __init__(self, driver, projection=None):
        self.driver = driver
        self.projection = projection
