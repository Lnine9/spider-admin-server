from scrapyd_api import ScrapydClient
from model.scrapyd_node import ScrapydNode
from utils.logger import logger
from model.task import Task
from constants.index import TaskStatus
from setting import SCRAPY_PROJECT


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
        cls.connect_nodes()

    @classmethod
    def connect_nodes(cls):
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
        cls.connect_nodes()
        return node

    @classmethod
    def delete_node(cls, id):
        node = ScrapydNode.get(ScrapydNode.id == id)
        node.delete_instance()
        cls.connect_nodes()
        return True

    @classmethod
    def get_node_by_id(cls, id):
        for c in clients:
            if str(c.id) == str(id):
                return c
        return None

    @classmethod
    def get_least_busy_node(cls):
        least_busy = None
        for c in clients:
            if c.instance is not None:
                try:
                    if c.instance.daemon_status().get('status') != 'ok':
                        continue
                    data = c.instance.list_projects()
                    if least_busy is None or len(data) < least_busy:
                        least_busy = c
                except Exception as e:
                    pass
        return least_busy

    @classmethod
    def execute_task(cls, task_id, node_id):
        print(task_id,node_id)
        task = Task.get(Task.id == task_id)
        if task is None:
            return
        if task.status == TaskStatus.RUNNING or task.status == TaskStatus.COMPLETED:
            return

        if node_id is not None:
            node = cls.get_node_by_id(node_id)
            if node is not None:
                try:
                    node.instance.schedule(project=SCRAPY_PROJECT['NAME'], spider=task.spider_id, **task)
                    task.status = TaskStatus.RUNNING
                    task.job_id = task_id
                    task.node_address = node.address
                    task.save()
                except Exception as e:
                    logger.error(f"Failed to execute task {task_id} on node {node_id}: {e}")
        else:
            node = cls.get_least_busy_node()
            if node is not None:
                try:
                    node.instance.schedule(project=SCRAPY_PROJECT['NAME'], spider='BASE_SPIDER', **task.__data__)
                    task.status = TaskStatus.RUNNING
                    task.job_id = task_id
                    task.node_address = node.address
                    task.save()
                except Exception as e:
                    logger.error(f"Failed to execute task {task_id} on node {node.id}: {e}")


# scheduler.add_job(
#             func=ScrapydService.connect_nodes,
#             trigger='cron',
#             second=30,
#             replace_existing=True,
#         )

