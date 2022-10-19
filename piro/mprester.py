import contextlib

from pymatgen.core import Structure
from pymatgen.ext.matproj import _MPResterLegacy, MPRester
from pymongo import MongoClient

from piro.settings import settings


@contextlib.contextmanager
def get_mprester():
    if settings.use_mapi_db:
        with MongoMPRester(settings.mongodb_uri) as mpr:
            yield mpr
    else:
        with MPRester() as mpr:
            yield mpr


class MongoMPRester(_MPResterLegacy):
    """
    this subclass of pymatgen.ext.matproj.MPRester class queries a MongoDB instead of Materials Project API
    """

    def __init__(self, mongodb_uri: str):
        """

        :param mongodb_uri: the uri has this format: mongodb://{username}:{password}@{host}:{port}/{database}
        """
        super().__init__(notify_db_version=False)
        self.client = MongoClient(mongodb_uri)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        super().__exit__(exc_type, exc_val, exc_tb)

    def query(
        self,
        criteria,
        properties,
        chunk_size=500,
        max_tries_per_chunk=5,
        mp_decode=True,
    ):
        """
        Arguments are the same as superclass. See the superclass's docs for info.

        Our mongo db only has 'material_id' so 'task_id' will just be copied over.

        :param criteria: converted to a mongo query for mongo find()
        :param properties: converted to a mongo projection for mongo find()
        :param chunk_size: currently unsupported
        :param max_tries_per_chunk: currently unsupported
        :param mp_decode: only supported for the 'structure' field
        :return:
        """
        query = dict(**criteria)
        if 'task_id' in query:
            query['material_id'] = query.pop('task_id')

        projection = {p: True for p in properties}
        projection['_id'] = False  # we don't want mongo's id in the result
        if 'task_id' in projection:
            projection.pop('task_id')
            projection['material_id'] = True

        results = []
        for r in self.client.piro.mp.find(query, projection):
            if properties and 'task_id' in properties:
                r['task_id'] = r['material_id']
            if mp_decode and 'structure' in r:
                r['structure'] = Structure.from_dict(r['structure'])
            results.append(r)

        return results
