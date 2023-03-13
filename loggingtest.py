import logging

logging.basicConfig(level=logging.INFO, filename="phraselogging.log",filemode="w",
                    format="%(asctime)s  %(message)s")
logging.info("Test log")
logging.info("Test log2")