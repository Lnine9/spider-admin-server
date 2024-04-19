from scrapyd_api import ScrapydClient
from model.scrapyd_node import ScrapydNode
from utils.id import generate_uuid
from utils.logger import logger


class Client:
    def __init__(self, id, name, address, instance):
        self.id = id
        self.name = name
        self.address = address
        self.instance = instance


clients = []


class ScrapydService:

    @classmethod
    def init(cls):
        global clients
        records = ScrapydNode.select().dicts()
        clients = []

        for record in records:
            try:
                client_instance = ScrapydClient(record['address'])
                print(f"Connected to the scrapyd node: {record['name']}, {record['address']}")
                print(client_instance.daemon_status())
                clients.append(Client(record['id'], record['name'], record['address'], client_instance))
            except Exception as e:
                print(f"Failed to connect to the scrapyd node: {record['name']}, {record['address']}: {e}")
                clients.append(Client(record['id'], record['name'], record['address'], None))

    @classmethod
    def list_scrapyd_node(cls):
        result = []
        for c in clients:
            status = 0
            if c.instance is not None:
                try:
                    deamon_status = c.instance.daemon_status()
                    if deamon_status.get('status') == 'ok':
                        status = 1
                except Exception as e:
                    status = 0

            result.append({
                'id': c.id,
                'name': c.name,
                'address': c.address,
                'status': status
            })

        return {
            'list': result,
            'total': len(result)
        }

    @classmethod
    def get_node_detail(cls, id):
        for c in clients:
            if str(c.id) == str(id):
                if c.instance is not None:
                    try:
                        data = c.instance.daemon_status()
                        data.update({
                            'id': c.id,
                            'name': c.name,
                            'address': c.address,
                            'status': 1,
                        })
                        return data
                    except Exception as e:
                        pass
                return {
                    'id': c.id,
                    'name': c.name,
                    'address': c.address,
                    'status': 0,
                }
        return None

    @classmethod
    def add_node(cls, node):
        ScrapydNode.create(**node)
        cls.init()
        return node

    @classmethod
    def delete_node(cls, id):
        node = ScrapydNode.get(ScrapydNode.id == id)
        node.delete_instance()
        cls.init()
        return True
