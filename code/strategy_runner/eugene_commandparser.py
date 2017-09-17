import os 
import sys 
import getopt
import logging 

logger = logging.getLogger(os.environ['logger'])

def usage():
	logger.error(" ****************************************************************************")
	logger.error(" %s usage : " %(sys.argv[0]))
	logger.error(" %s -f <data file> -s <start date> -e <end date>" %(sys.argv[0]))
	logger.error(" -c --config : strategy config file")
	logger.error(" -f --frequency : frequnecy of running strategy daily, weekly, monthly")
	logger.error(" -s --start : start date")
	logger.error(" -e --end : end date")
	logger.error(" ****************************************************************************")
	sys.exit()

def parse_commandline():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:s:e:c:", ["help", "frequency=", "start_date=", "end_date=", "config="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	config = ''
	frequency = ''
	start_date = ''
	end_date = ''

	for o, a in opts:
		if o in ("-f", "--frequency"):
			frequency = a 
		elif o in ("-c", "--config"):
			config = a
		elif o in ("-s", "--start_date"):
			start_date = a
		elif o in ("-e", "--end_date"):
			end_date = a
		elif o in ("-h", "--help"):
			usage()
		else:
			assert False, "unhandled option"

	if not frequency :
		logger.error("frequncy has not been provided with option -f !!!")
		usage()

	if not start_date :
		logger.error("start date has not been provided with option -s !!!")
		usage()

	if not end_date :
		logger.error("end date has not been provided with option -e !!!")
		usage()

	if not config :
		logger.error("config file has not been provided with option -c !!!")
		usage()

	if not os.path.exists(config):
		logger.error("config file %s does not exists !!!", config)
		usage()

	return config, frequency, start_date, end_date

