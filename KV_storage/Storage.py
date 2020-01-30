import json
import os.path


class Storage:
    _storage = {}

    def add(self, key, value):
        self._storage[key] = value

    def delete(self, key):
        self._storage.pop(key)

    def get(self, key):
        return self._storage[key]

    def load(self):
        if not os.path.exists("storage_file.json"):
            self.save()
        with open("storage_file.json", "r") as read_file:
            self._storage = json.load(read_file)

    def save(self):
        with open("storage_file.json", "w") as write_file:
            json.dump(self._storage, write_file)
