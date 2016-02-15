"""
    Registrar
    ~~~~~

    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

This file is part of Registrar.

    Registrar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Registrar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Registrar. If not, see <http://www.gnu.org/licenses/>.
"""

import os
from .config import SERVER_MODE


class TinyDBConvertor(object):

    def __init__(self, collection_name):

        self.local_db = TinyDB(LOCAL_DB_FULLPATH)
        self.collection_name = collection_name

    def find(self):

        query = Query()
        return self.local_db.search(query.type == self.collection_name)

    def find_one(self, entry):
        query = Query()
        return self.local_db.search((query.type == self.collection_name) &
                                    (query.fqu == entry['fqu']))

    def save(self, new_entry):

        new_entry['type'] = self.collection_name
        self.local_db.insert(new_entry)

    def remove(self, entry):
        query = Query()
        return self.local_db.remove((query.type == self.collection_name) &
                                    (query.fqu == entry['fqu']))

if SERVER_MODE:

    from pymongo import MongoClient

    from .config import QUEUE_DB_URI

    c = MongoClient()
    state_diff = c['namespace'].state_diff

    queue_db = MongoClient(QUEUE_DB_URI)['registrar']
    preorder_queue = queue_db.preorder_queue
    register_queue = queue_db.register_queue
    update_queue = queue_db.update_queue
    transfer_queue = queue_db.transfer_queue

    pending_queue = queue_db.pending_queue

    # to-do: rename this from 'migration'
    registrar_users = c['migration'].migration_users
    registrar_addresses = c['migration'].registrar_addresses

else:
    from tinydb import TinyDB, Query

    from .config import LOCAL_DB_FULLPATH, LOCAL_DIR

    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    preorder_queue = TinyDBConvertor('preorder')
    register_queue = TinyDBConvertor('register')
    update_queue = TinyDBConvertor('update')
    transfer_queue = TinyDBConvertor('transfer')

    pending_queue = TinyDBConvertor('pending')
