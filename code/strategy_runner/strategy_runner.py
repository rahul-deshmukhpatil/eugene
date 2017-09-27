#/bin/python -B
import os
import sys
import logging
import eugene_logger

os.environ['logger'] = 'main_logger'
eugene_logger.setup_custom_logger()	

import eugene_db
import eugene_commandparser
import eugene_expiries
import eugene_strategy

logger = logging.getLogger(os.environ['logger'])

# main function: 
# initilize db
# start the main iterator function
######################################################################
def main():
	strategy, frequency, start_date, end_date, entry_delta, exit_delta = eugene_commandparser.parse_commandline() 
	cursor=eugene_db.open_db()
	expiries = eugene_expiries.get_expiries(frequency, start_date, end_date)
	logger.info('Running strategy for Expiries : %s', expiries);

	eugene_strategy.runstrategy(cursor, strategy, frequency, expiries, entry_delta, exit_delta)


# Ivoke the main
################################################
main()



