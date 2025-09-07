import logging


logging.basicConfig(
    filename="logger.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# import logging
# import os
#
#
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
#
# LOG_FILE = os.path.join(LOG_DIR, "app.log")
#
#
# def get_logger(name: str) -> logging.Logger:
#
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.DEBUG)
#
#     if not logger.handlers:
#         formatter = logging.Formatter(
#             "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
#             datefmt="%Y-%m-%d %H:%M:%S",
#         )
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         logger.addHandler(console_handler)
#
#         # כתיבה לקובץ
#         file_handler = logging.FileHandler(LOG_FILE)
#         file_handler.setFormatter(formatter)
#         logger.addHandler(file_handler)
#
#     return logger