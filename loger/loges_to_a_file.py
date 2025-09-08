import logging
from elasticsearch import Elasticsearch
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

es_host_url = os.getenv("ELASTIC_URL")
index_name = os.getenv("INDEX_LOGGIN_NAME")

class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, index=index_name, es_host=es_host_url, name="logger_name"
        , level=logging.INFO):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            es = Elasticsearch(es_host)
            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={
                        "timestamp": datetime.utcnow().isoformat(),
                        "level": record.levelname,
                        "logger": record.name,
                        "message": record.getMessage()
                        })
                        print("insert the logs !!!!!")
                    except Exception as e:
                        print(f"ES log failed: {e}")
            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger