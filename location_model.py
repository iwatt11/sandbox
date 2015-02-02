# -*- coding: utf-8 -*-#
# !/usr/local/bin/python2.7
import json
import wikipedia
import urllib2
from itertools import izip
from collections import OrderedDict


class GetWikiData:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lon = lng
        self.json_response = None
        self.namespace = self.town_and_state(lat, lng)
        self.structure_data()


    def structure_data(self):
        if self.namespace:
            raw_wiki = self.wiki_work(self.namespace)
            #print raw_wiki
            if raw_wiki:
                text_dict = self.text_cleaning(raw_wiki)
                #To be moved into iPhone application to display section headers
                #sections = []
                #for cat, desc in text_dict.iteritems():
                #    sections.append(cat)
                self.json_response = json.dumps(text_dict)
            else:
                self.json_response = json.dumps("""No record for your location. Try again on down the road.""")
        else:
            self.json_response = json.dumps("""No record for your location. Try again on down the road.""")

    def wiki_work(self, namespace):
        """Get Wiki article associated with Town,_State naming convention. Return dict with sections and text."""
        #  wikipedia.geosearch might be a nice add-on later
        try:
            if len(namespace) > 1:
                place_url = namespace[0]+',_'+namespace[1]
            else:
                place_url = namespace
            raw_wiki = wikipedia.page(place_url).content.encode('utf-8')

            return raw_wiki
        except:
            return False

    def text_cleaning(self, text):
        text = text.replace("====", "%^")
        text = text.replace("===", "~")
        print text
        text_list = text.split('==')
        stripped_list = map(str.strip, text_list)
        stripped_list[:0] = ['Summary']
        text_dict = self.list_to_dict(stripped_list)
        # Create sub dictionary if there are sub-sections present in the dictionary
        text_dict = self.sub_dictionary(text_dict,'~')
        text_dict = self.sub_sub_dictionary(text_dict, '%^')
        text_dict = self.remove_reference_sections(text_dict)

        return text_dict

    def list_to_dict(self, text_list):
        i = iter(text_list)
        text_dict = OrderedDict(zip(i, i))
        #What if there are two blank entries?
        for key, entry in text_dict.iteritems():
            if len(entry)==0:
                text_dict = self.del_dict_item(text_dict, key)

        return text_dict

    def del_dict_item(self, text_dict, key):
        r = OrderedDict(text_dict)
        del r[key]

        return r

    def remove_reference_sections(self, dictionary):
        check = ('Reference', 'reference', 'Link', 'link')
        for key, entry in dictionary.iteritems():
            if any(word in key for word in check):
                dictionary = self.del_dict_item(dictionary, key)

        return dictionary

    def sub_dictionary(self, dictionary, searchFor):
        """Finds if split value exists in dictionary values
        and creates a sub-dictionary."""

        for key, dict_item in dictionary.iteritems():
            if searchFor in dict_item:
                dict_item = dict_item.split(searchFor)
                new_list = [key]+dict_item
                new_list = map(str.strip, new_list)
                sub_dict = self.list_to_dict(new_list)
                dictionary[key] = sub_dict

        return dictionary

    def sub_sub_dictionary(self, dictionary, searchFor):
        for key, value in dictionary.iteritems():
            text_list = value.split(searchFor)
            stripped_list = map(str.strip, text_list)
            dict_items = self.list_to_dict(stripped_list)
            for sub_key, dict_item in dict_items.iteritems():
                if searchFor in dict_item:
                    dict_item = dict_item.split(searchFor)
                    new_list = [sub_key]+dict_item
                    new_list = map(str.strip, new_list)
                    sub_dict = self.list_to_dict(new_list)
                    dictionary[key][sub_key] = sub_dict

        return dictionary

    def get_geonames(self, lat, lng, types):
        """Collect from Google API geographical names along with their types."""
        url = 'http://maps.googleapis.com/maps/api/geocode/json' + \
                '?latlng={},{}&sensor=false'.format(lat, lng)
        json_data = json.load(urllib2.urlopen(url))
        address_comps = json_data['results'][0]['address_components']
        filter_method = lambda x: len(set(x['types']).intersection(types))

        return filter(filter_method, address_comps)

    def town_and_state(self, lat, lng):
        """Obtain long Town and State names."""
        types = ['locality', 'administrative_area_level_1']
        country = ['country']
        namespace = []
        try:
            for country_name in self.get_geonames(lat, lng, country):
                short_name = country_name['short_name']
            if short_name == 'US':
                for geo_name in self.get_geonames(lat, lng, types):
                    name = geo_name['long_name']
                    namespace.append(name)

                return namespace
            else:
                for geo_name in self.get_geonames(lat, lng, types):
                    name = geo_name['long_name']
                    namespace.append(name)

                    return namespace
        except:
            return False
