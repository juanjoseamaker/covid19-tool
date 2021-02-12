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
        print('cannot get', url, 'data from server, server returned code', resp.code)
        print(resp.read().decode())
        sys.exit(1)

    data = json.load(resp)
    conn.close()

    return data

def main():
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], '[summary|search|help|top|graph] (country) (arg)')
        sys.exit(0)

    if sys.argv[1] == 'help':
        print('usage:', sys.argv[0], '[summary|search|help|top|graph] (country) (arg)')
        print('- This program use api.covid19api.com to get the data')
        print('- This program does not take responsibility about the data showed')

    elif sys.argv[1] == 'summary':
        data = connect_api('/summary')

        print('Coronavirus statistics summary')
        print('- Total Confirmed:', "{:,}".format(data['Global']['TotalConfirmed']))
        print('- Total Recovered:', "{:,}".format(data['Global']['TotalRecovered']))
        print('- Total Deaths:', "   {:,}".format(data['Global']['TotalDeaths']))
        print('Today new coronavirus statistics summary')
        print('- New Confirmed:', "{:,}".format(data['Global']['NewConfirmed']))
        print('- New Recovered:', "{:,}".format(data['Global']['NewRecovered']))
        print('- New Deaths:', "   {:,}".format(data['Global']['NewDeaths']))
        print('Statistics date:', data['Date'])

    elif sys.argv[1] == 'search' and len(sys.argv) > 2:
        data = connect_api('/summary')
        query = sys.argv[2].lower()

        for country in data['Countries']:
            if query in country['Country'].lower():
                print('Coronavirus', country['Country'], 'statistics summary')
                print('- Total Confirmed:', "{:,}".format(country['TotalConfirmed']))
                print('- Total Recovered:', "{:,}".format(country['TotalRecovered']))
                print('- Total Deaths:', "   {:,}".format(country['TotalDeaths']))
                print('Today new coronavirus', country['Country'], 'statistics summary')
                print('- New Confirmed:', "{:,}".format(country['NewConfirmed']))
                print('- New Recovered:', "{:,}".format(country['NewRecovered']))
                print('- New Deaths:', "   {:,}".format(country['NewDeaths']))
                print('Statistics date:', country['Date'])

    elif sys.argv[1] == 'top' and len(sys.argv) > 3:
        top_list = []
        top_len = int(sys.argv[2])
        query = sys.argv[3].lower()
        max_e = 0

        if query == "global":
            data = connect_api('/summary')

            for _ in range(top_len):
                for i in range(len(data['Countries'])):
                    if data['Countries'][i]['TotalConfirmed'] > data['Countries'][max_e]['TotalConfirmed']:
                        max_e = i

                try:
                    top_list.append(data['Countries'].pop(max_e))
                except IndexError:
                    print('top argument is greater than the number of territories')

                max_e = 0

            print('Global top by confirmed cases')
            for country in top_list:
                print('-', "{:,}".format(country['TotalConfirmed']), '\t', country['Country'])

    elif sys.argv[1] == 'graph' and len(sys.argv) > 3:
        graph_len = int(sys.argv[2])
        query = sys.argv[3].lower()
        data = connect_api('/summary')

        for country in data['Countries']:
            if query in country['Country'].lower():
                country_data = connect_api('/country/' + country['Slug'])

                print(country['Country'], 'confirmed cases graph')
                for day in country_data:
                    bar_len = int(day["Confirmed"]/graph_len)
                    if bar_len == 0:
                        continue

                    print(day['Date'], day['Confirmed'], '\t\t', '|'*bar_len)

    else:
        print('usage:', sys.argv[0], '[summary|search|help|top|graph] (country) (arg)')

if __name__ == '__main__':
    main()
