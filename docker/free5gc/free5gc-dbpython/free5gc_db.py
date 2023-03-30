

from pymongo import MongoClient
import bson

subscriber_collections = [
    'subscriptionData.provisionedData.smfSelectionSubscriptionData',
    'subscriptionData.provisionedData.smData',
    'policyData.ues.smData',
    'policyData.ues.amData',
    'subscriptionData.provisionedData.amData',
    'subscriptionData.authenticationData.authenticationSubscription'
    ]


class Free5gc:
    def __init__(self, server_ip, server_port):
        self.mongo_server_uri = f'mongodb://{server_ip}:{server_port}/'

    def get_subscribers(self):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        subscribers_data = {}
        for col_name in subscriber_collections:
            col = fgcore_db[col_name]
            subscribers_data[col_name] = list(col.find())
        return subscribers_data

    def get_subscriber(self, imsi):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        _query = {'ueId': f'imsi-{imsi}'}
        subscriber_data = {}
        for col_name in subscriber_collections:
            col = fgcore_db[col_name]
            subscriber_data[col_name] = list(col.find(_query))
        return subscriber_data

    def add_subscriber(self, subscriber_data):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        for col_name, col_content in subscriber_data.items():
            col = fgcore_db[col_name]
            for item in col_content:
                item['_id'] = bson.ObjectId()
                # item['_id'] = subscriber_data['policyData.ues.smData'][0]['ueId']
            result = col.insert_many(col_content)
        return True

    def update_subscriber(self, imsi, subscriber_data):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        _query = {'ueId': f'imsi-{imsi}'}
        for col_name, col_content in subscriber_data.items():
            newvalues = {'$set': col_content}
            col = fgcore_db[col_name]
            result = col.update_one(_query, newvalues)

    def delete_subscriber(self, imsi):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        _query = {'ueId': f'imsi-{imsi}'}
        for col_name in subscriber_collections:
            col = fgcore_db[col_name]
            result = col.delete_many(_query)
        return result.deleted_count

    def delete_all_subscribers(self):
        _client = MongoClient(self.mongo_server_uri)
        fgcore_db = _client['free5gc']
        for col_name in subscriber_collections:
            col = fgcore_db[col_name]
            result = col.drop()
