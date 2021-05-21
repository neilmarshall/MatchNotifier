import json


class Config():
    def __init__(self, filename='local.settings.json'):
        with open(filename) as f:
            self.parameters = json.load(f)['Values']

    def get_connection_string(self):
        conn_str = self.parameters['AzureWebJobsStorage']
        if conn_str == "UseDevelopmentStorage=true":
            conn_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
        return conn_str
