from airtable import Airtable
import os

class Database:
    def __init__(self, base, table, init=True, api_key=None):
        if api_key is None:
            self.__API_KEY = os.environ.get('AIRTABLE_API_KEY')
        else:
            self.__API_KEY = api_key
        assert self.__API_KEY is not None, "Need Airtable API Key" 
        self.__engine = Airtable(base, table, self.__API_KEY)
        if init:
            self.update()
        
    @property
    def query(self):
        return self.__query
        
    def update(self):
        try:
            self.__query = self.__engine.get_all()
            assert not len(self.__query) == 0, "No data fetched"
        except:
            raise Exception("Fail to find the following database")
        
    def fetch(self, categories, sort_by=None, lastProcess=None):
        data = []
        for row in self.__query:
            row = row['fields']
            temp = {}
            for category in categories:
                try:
                    temp[category] = row[category][0]['url']
                except:
                    temp[category] = row[category]
            data.append(temp)
        result = sorted(list(filter(None, data)), key=lambda k: k[sort_by]) if sort_by is not None else list(filter(None, data)) 
        return lastProcess(result) if lastProcess is not None else result

    def append(self, **data):
        self.__engine.insert(data)