import mediacloud, json, datetime
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("../config/config.ini")
key = config.get('auth','mediacloudkey')
mc = mediacloud.api.MediaCloud('key')
print key