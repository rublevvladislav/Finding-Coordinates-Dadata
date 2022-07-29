from dadata import Dadata


class DadataRequests:
    def __init__(self, api_key, language):
        self.api_key = api_key
        self.language = language
        self.dadata = Dadata(api_key)
        self.addresses = None

    def get_address(self, query):
        self.addresses = self.dadata.suggest('address', query)
        if len(self.addresses) == 0:
            return False
        for idx, data in enumerate(self.addresses):
            print(f'{idx + 1} - {data["value"]}')

        return True

    def get_coordinates(self, idx):
        if not idx.isdigit():
            return False
        if int(idx) > len(self.addresses) or int(idx) < 1:
            return False
        print(f'Адрес: {self.addresses[int(idx) - 1]["value"]}')
        print(f'Широта: {self.addresses[int(idx) - 1]["data"]["geo_lat"]}')
        print(f'Долгота: {self.addresses[int(idx) - 1]["data"]["geo_lon"]}')
        return True
