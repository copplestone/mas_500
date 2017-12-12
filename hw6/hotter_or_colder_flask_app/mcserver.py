# python mcserver.py

import ConfigParser, logging, datetime, os, json, requests

import numpy as np

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
weather_key = config.get('auth','api_key')

app = Flask(__name__)

# this tutorial has been pretty helpful https://www.dataquest.io/blog/python-api-tutorial/
@app.route("/")
def home():

    # fetch data from the weather api
    base_url = "http://api.openweathermap.org/data/2.5/forecast?lat=42.37&lon=71.12&APPID=" + weather_key
    print(base_url)
    #parameters = {'lat':42.36,'lon':71.058}
    #response = requests.get(base_url, params=parameters)
    response = requests.get(base_url)
    print('response state = ' + str(response))


    # extract temperature today and tomorrow

    weather_data = response.json()

    date_time1 = weather_data["list"][0]["dt_txt"]
    date_time2 = weather_data["list"][8]["dt_txt"]
    temp_today = weather_data["list"][0]["main"]["temp"]
    temp_tomorrow = weather_data["list"][8]["main"]["temp"]
    print("From " + str(date_time1) + " to " + str(date_time2))
    print("Temperature now " + str(temp_today) + ", temperature tomorrow " + str(temp_tomorrow))


    # use weather data to figure out the change in temperature
    difference = temp_today - temp_tomorrow
    if difference > 0:
        phrase = "colder than"
    elif difference < 0:
        phrase = "hotter than"
    else:
        phrase = "about the same as"
    return render_template("weather-results.html",
                           phrase=phrase,
                           number=9)


@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    now = datetime.datetime.now()
    start = request.form['start']
    end = request.form['end']
    print(start)
    print(end)

    #results = mc.sentenceCount(keywords,
    #                           solr_filter=[mc.publish_date_query( datetime.date(int(start[0:4]), int(start[5:7]),
    # int(start[8:10])), datetime.date(int(end[0:4]), int(end[5:7]), int(end[8:10])) ),
    #                                        'tags_id_media:9139487'],split=true)

    results = mc.sentenceCount(keywords,solr_filter=[mc.publish_date_query( datetime.date(2017,1,1), now ),'tags_id_media:9139487'], split = True, split_start_date = start, split_end_date=end)

    print("results = ")
    print(results)
    clean_data = {}
    sub_dict = results['split']
    sub_dict.pop('end', None)
    sub_dict.pop('gap', None)
    sub_dict.pop('start', None)
    for key in sub_dict:
        f = key.encode('utf-8')
        date = 'Date.UTC('+str(f[0:4])+','+str(f[5:7])+','+str(f[8:10])+')'
        clean_data[date] = sub_dict[key]



    return render_template("search-results.html",
                           keywords=keywords,
                           sentenceCount=results['count'],
                           cleaned_results=json.dumps(clean_data))

if __name__ == "__main__":
    app.debug = True
    app.run()
