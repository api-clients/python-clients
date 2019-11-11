import logging


class InternalStorageError(Exception):
    pass


class Method:
    name = ''
    type_ = ''
    collection = ''
    projection = None  # Filter for MongoDB
    query = None

    def __init__(self, query=None, projection=None):
        self.query = query
        self.projection = projection

    @staticmethod
    def response_process(resp):
        return resp


class Clean(Method):
    name = 'clean all'
    type_ = 'clean'


class Client:
    """
    This client implements http-client

    :param driver: pymongo-driver (4.2 and more, less may be not working)
    :param db_name: mongodb's database
    """
    def __init__(self, driver, db_name):
        logging.info(f'client\'s storage db_name: {db_name}')
        self.__driver = driver
        self.db_name = db_name

    def __args(self, method):
        p = method.projection
        q = method.query
        c = method.collection
        logging.info(f'mongodb client. name: {method.name}. query: {q}. projection: {p}')
        return p, c, q

    def get_cursor(self, method):
        proj, col, query = self.__args(method)
        if method.type_ == 'find':
            for item in self.__driver[self.db_name][col].find(query, proj):
                yield method.response_process([item])
        else:
            raise NotImplemented('this method is not implemented')

    def request(self, method):
        proj, col, query = self.__args(method)
        if method.type_ == 'find':
            try:
                resp = []
                for item in self.__driver[self.db_name][col].find(query, proj):
                    resp.append(item)
            except Exception as e:
                logging.error(e)
                raise InternalStorageError()
        elif method.type_ == 'insert':
            try:
                resp = self.__driver[self.db_name][col].insert(query)
            except Exception as e:
                logging.error(e)
                raise InternalStorageError()
        elif method.type_ == 'update_one':
            try:
                resp = self.__driver[self.db_name][col].update_one(proj, update=query)
            except Exception as e:
                logging.error(e)
                raise InternalStorageError()
        elif method.type_ == 'db_lists':
            resp = self.__driver.list_database_names()
        elif method.type_ == 'drop_database':
            resp = self.__driver.drop_database(self.db_name)
        elif method.type_ == 'delete_many':
            resp = self.__driver[self.db_name][col].delete_many(query)
        elif method.type_ == 'delete_collection':
            resp = self.__driver[self.db_name].drop_collection(col)
        elif method.type_ == 'collection_names':
            resp = self.__driver[self.db_name].collection_names(col)
        elif method.type_ == 'aggregation':
            resp = self.__driver[self.db_name][col].aggregate(query)
        elif method.type_ == 'clean':
            names = self.__driver[self.db_name].collection_names(col)
            for name in names:
                if name != 'admin':
                    _ = self.__driver[self.db_name].collection_names(name)
            resp = {}
        else:
            raise NotImplemented('this method is not implemented')
        return method.response_process(resp)
