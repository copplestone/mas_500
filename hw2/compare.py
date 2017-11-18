import mediacloud
import datetime
import ConfigParser
import numpy as np
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Commencing beautiful detailed helpful log")
config = ConfigParser.ConfigParser()
config.read("../config/inputs.ini")

def fetch_input():
	# write the search terms into config.ini
	cfgfile = open("../config/inputs.ini",'w')
	word1_input = sys.argv[1]
	word2_input = sys.argv[2]
	config.set('query','word1',str(word1_input))
	config.set('query','word2',str(word2_input))
	logger.info("Wrote input words to config.ini")
	
	# get timespan as input in the command line
	start_date = input("Enter start date (enter 4 for April rather than 04) [yyyy,m,d] :")
	end_date = input("Enter end date (enter 4 for April rather than 04) [yyyy,m,d] :")

	config.set('timespan','year1',start_date[0])
	config.set('timespan','month1',start_date[1])
	config.set('timespan','day1',start_date[2])
	config.set('timespan','year2',end_date[0])
	config.set('timespan','month2',end_date[1])
	config.set('timespan','day2',end_date[2])

	config.write(cfgfile)
	cfgfile.close()


def fetch_data():
	config.read("../config/config.ini")
	key = config.get('auth','mediacloudkey')
	config.read("../config/inputs.ini")
	year1 = config.get('timespan','year1')
	month1 = config.get('timespan','month1')
	day1 = config.get('timespan','day1')
	year2 = config.get('timespan','year2')
	month2 = config.get('timespan','month2')
	day2 = config.get('timespan','day2')
    
	word1 = config.get('query','word1')
	word2 = config.get('query','word2')

	mc = mediacloud.api.MediaCloud(key)
	word1_count = mc.sentenceCount(word1, solr_filter=[mc.publish_date_query( datetime.date( int(year1),int(month1),int(day1)), datetime.date( int(year2),int(month2),int(day2))), 'tags_id_media:1' ])
	if word1_count.values()[0] > 0:
		logger.info("Successfully called MediaCloud")
	else:
		logger.info("Didn't call MediaCloud correctly")
	word2_count = mc.sentenceCount(word2, solr_filter=[mc.publish_date_query( datetime.date( int(year1),int(month1),int(day1)), datetime.date( int(year2),int(month2),int(day2))), 'tags_id_media:1' ])
	logger.info("Inputs received = " + str(word1_count) + ' ,' + str(word2_count))
	return word1_count

fetch_input()
output = fetch_data()
