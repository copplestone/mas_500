import mediacloud, json, datetime
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("../config/config.ini")
key = config.get('AUTH','mediacloudkey')
mc = mediacloud.api.MediaCloud('key')