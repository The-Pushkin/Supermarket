import logging
from python_logging_loki import LokiHandler

class LokiLogger:
    def __init__(self, service_name, loki_url="http://loki:3100/loki/api/v1/push"):
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.DEBUG)

        self.loki_handler = LokiHandler(
            url=loki_url,
            tags={"service": service_name},
            version="1"
        )

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.loki_handler.setFormatter(formatter)

        self.logger.addHandler(self.loki_handler)

    def get_logger(self):
        return self.logger
