import mediacloud
import datetime
import ConfigParser
import matplotlib.pyplot as plt
import numpy as np

config = ConfigParser.ConfigParser()
config.read("../config/config.ini")
key = config.get('auth','mediacloudkey')
mc = mediacloud.api.MediaCloud(key)

clinton = mc.sentenceCount('( clinton)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
trump = mc.sentenceCount('( trump)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
hilary_clinton = mc.sentenceCount('( hilary AND clinton)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
hilary = mc.sentenceCount('( hilary)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
donald_trump = mc.sentenceCount('( donald AND trump)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
donald = mc.sentenceCount('( donald)', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])

# taken from example here https://matplotlib.org/examples/api/barchart_demo.html
ind = np.arange(6)
width = 0.35
fig = plt.figure(figsize=(15,7))
ax = fig.add_subplot(111)
ax.set_ylabel('Words')
ax.set_title('Number of sentences containing words in Sept 2016')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('hilary', 'clinton', 'hiliary clinton', 'donald', 'trump', 'donald trump'))

words = [hilary.values()[0], clinton.values()[0], hilary_clinton.values()[0], donald.values()[0], trump.values()[0], donald_trump.values()[0]]
print words
rects1 = ax.bar(ind, words, width, color='r')
plt.show()