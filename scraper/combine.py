import json
import os
import pprint

myDict = {}
def combineJSON():
    """The webscraper currently outputs the thumbnail image in a seperate row
    as the rest of the track. This function combines them.
    """

    with open('scraper/sc.json', 'r') as r, open('my_app/output.json', 'w') as w:
        data = json.load(r)

        myDict['rows'] = []

        for line in data:
            if not line.has_key('image'):
                myDict['rows'].append(line)
            else: 
                for x in range(len(myDict['rows'])):
                    if myDict['rows'][x]['title'] == line['title']:
                        myDict['rows'][x].update({'image': line['image']})
        
        w.write(json.dumps(myDict, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    combineJSON()