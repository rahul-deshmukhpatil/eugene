import os 
import logging

def setup_custom_logger():
	name = os.environ['logger']
	formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	handler = logging.FileHandler(filename='strategy.log')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	return logger
