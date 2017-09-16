#/bin/python
import os
import sys
import logging
import getopt
import eugene_logger

os.environ['logger'] = 'main_logger'
eugene_logger.setup_custom_logger()	

import eugene_db

def usage():
    logger.error(" ****************************************************************************")
    logger.error(" %s usage : " %(argv[0]))
    logger.error(" %s -f <data file> -s <start date> -e <end date>" %(argv[0]))
    logger.error(" -f --frequency : frequnecy of running strategy daily, weekly, monthly")
    logger.error(" -s --start : start date")
    logger.error(" -e --end : end date")
    logger.error(" ****************************************************************************")

# main function: 
# initilize db
# start the main iterator function
######################################################################
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:s:e:", ["help", "frequency=", "start_date=", "end_date="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ("-f", "--frequency"):
			frequency = a 
		elif o in ("-s", "--start_date"):
			start_date = a
		elif o in ("-e", "--end_date"):
			end_date = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			assert False, "unhandled option"

	cursor=eugene_db.open_db()


# Ivoke the main
################################################
main()



