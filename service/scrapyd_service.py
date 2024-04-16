from scrapyd_api import ScrapydClient
from model.scrapyd_node import ScrapydNode
from utils.logger import logger

class Client:
    def __init__(self, id, name, address, instance):
        self.id = id
        self.name = name
        self.address = address
        self.instance = instance


records = ScrapydNode.select().dicts()
clients = []

for record in records:
    try:
        client_instance = ScrapydClient(record['address'])
        print(client_instance.daemon_status())
        clients.append(Client(record['id'], record['name'], record['address'], client_instance))
    except Exception as e:
        print(f"Failed to connect to the scrapyd node: {record['name']}, {record['address']}: {e}")

if __name__ == '__main__':
    pass
