from dataclasses import dataclass
from llama_index import (
    load_index_from_storage,
    SimpleDirectoryReader,
    VectorStoreIndex,
    Response
)
from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from llama_index.storage import StorageContext
from openssm.core.backend.base_backend import BaseBackend


@dataclass
class Backend(BaseBackend):
    index: BaseIndex = None
    _query_engine: BaseQueryEngine = None

    @property
    def query_engine(self) -> BaseQueryEngine:
        if self._query_engine is None:
            if self.index is None:
                return None
            self._query_engine = self.index.as_query_engine()
        return self._query_engine

    def __init__(self):
        super().__init__()

    # pylint: disable=unused-argument
    def query2(self, user_input: list[dict], conversation_id: str = None) -> tuple[list[dict], Response]:
        """
        Query the index with the user input.

        Returns a tuple comprising (a) the response dicts and (b) the response object, if any.
        """
        response = None
        if self.query_engine is None:
            result = {"response": "I'm sorry, I don't have an index to query. Please load something first."}
        else:
            query = next((i['content'] for i in user_input if i['role'] == 'user'), None)
            response: Response = self.query_engine.query(query)
            result = {"response": response.response}

        return ([result], response)

    # pylint: disable=unused-argument
    def query(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        Query the index with the user input.

        Returns the response dicts.
        """
        # pylint: disable=unused-variable
        result, response = self.query2(user_input, conversation_id)
        return result

    def read_directory(self, directory_path: str):
        documents = SimpleDirectoryReader(directory_path).load_data()
        self.index = VectorStoreIndex(documents)

    def save(self, storage_dir: str):
        if self.index is not None:
            self.index.storage_context.persist(persist_dir=storage_dir)
        return super().save(storage_dir)

    def load(self, storage_dir: str):
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
        self.index = load_index_from_storage(storage_context)
        return super().load(storage_dir)
