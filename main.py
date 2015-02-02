#!/usr/local/bin/python2.7
"""Script to score the Roubini Country Insights Model"""
import sys
import location_model as lm

def main():
    lat = 53.235833
    lng = -1.4275
    instance = lm.GetWikiData(lat, lng)

    print instance.json_response

if __name__ == '__main__':
    sys.exit(main())
