import pymongo


class DataBase:
    def __init__(self, connection_url, db_name, collection_name):
        self.connection_url = connection_url
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(connection_url)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def add(self, data, multiple=False):
        if multiple:
            return self.collection.insert_many(data).inserted_ids
        else:
            return self.collection.insert_one(data).inserted_id

    def find(self, data, multiple=False):
        if multiple:
            return [x for x in self.collection.find(data)]
        else:
            return self.collection.find_one(data)

    def delete(self, data, multiple=False):
        if multiple:
            return self.collection.delete_many(data).deleted_count
        else:
            return self.collection.delete_one(data).deleted_count

    def update(self, old_data, new_data, multiple=False):
        if multiple:
            return self.collection.update_many(old_data, {"$set": new_data}).modified_count
        else:
            return self.collection.update_one(old_data, {"$set": new_data}).modified_count
