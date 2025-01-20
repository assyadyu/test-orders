import logging

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

order_logger = logging.getLogger("orders")
order_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
order_logger.addHandler(file_handler)
