from mongo.mongo import Mongo


class MongoQueue:

    __QUEUE: list[str] = None

    @classmethod
    def init(cls):
        cls.__QUEUE = []

        for _ in range(2):
            cls.generate_new_guid()

    @classmethod
    def pop(cls) -> str:
        cls.generate_new_guid()
        return cls.__QUEUE.pop()

    @classmethod
    def generate_new_guid(cls):
        guid: str = Mongo.insert_browser_guid_document()
        cls.__QUEUE.append(guid)
