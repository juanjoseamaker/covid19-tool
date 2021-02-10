#!/usr/bin/python3

# push content to github: git push -u origin main

import http.client
import json
import sys

def connect_api(url, method='GET'):
    conn = http.client.HTTPSConnection('api.covid19api.com', timeout=500)
    conn.request(method, url)
    resp = conn.getresponse()

    if resp.code != 200:
        print('cannot get data from server, server returned code', resp.code)
        print(resp.read())
        sys.exit(1)

    data = json.load(resp)
    conn.close()

    return data

def main():
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], '[summary|search|help] (country) (date)')
        sys.exit(0)

    if sys.argv[1] == 'help':
        print('usage:', sys.argv[0], '[summary|search|help] (country) (date)')
        print('- This program use api.covid19api.com to get the data')

    if sys.argv[1] == 'summary':
        data = connect_api('/summary')

        print('Coronavirus statistics summary')
        print('- Total Confirmed:', "{:,}".format(data['Global']['TotalConfirmed']))
        print('- Total Recovered:', "{:,}".format(data['Global']['TotalRecovered']))
        print('- Total Deaths:', "   {:,}".format(data['Global']['TotalDeaths']))
        print('Today new coronavirus statistics summary')
        print('- New Confirmed:', "{:,}".format(data['Global']['NewConfirmed']))
        print('- New Recovered:', "{:,}".format(data['Global']['NewRecovered']))
        print('- New Deaths:', "   {:,}".format(data['Global']['NewDeaths']))

    elif sys.argv[1] == 'search' and len(sys.argv) > 2:
        data = connect_api('/summary')
        query = sys.argv[2]

        for country in data['Countries']:
            if query.lower() in country['Country'].lower():
                print('Coronavirus', country['Country'], 'statistics summary')
                print('- Total Confirmed:', "{:,}".format(country['TotalConfirmed']))
                print('- Total Recovered:', "{:,}".format(country['TotalRecovered']))
                print('- Total Deaths:', "   {:,}".format(country['TotalDeaths']))
                print('Today new coronavirus', country['Country'], 'statistics summary')
                print('- New Confirmed:', "{:,}".format(country['NewConfirmed']))
                print('- New Recovered:', "{:,}".format(country['NewRecovered']))
                print('- New Deaths:', "   {:,}".format(country['NewDeaths']))

    else:
        print('usage:', sys.argv[0], '[summary|search|help] (country) (date)')

if __name__ == '__main__':
    main()