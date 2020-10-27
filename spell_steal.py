import json
import urllib.request
import re

def get_html(url):
    fp = None
    while fp is None:
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()
            value = mybytes.decode("utf8")
            fp.close()
        except:
            pass
    return value;

def get_clean_level(blurb):
    level = ''
    for i in range(0, len(blurb)):
        pattern = re.compile('(?!$)(Spell( )?\d(\d)?)?(Cantrip( )?\d(\d)?)?(Focus( )?\d(\d)?)?$')
        blurb[i] = blurb[i].replace('&nbsp;', '').strip()
        if pattern.search(blurb[i]):
            level = pattern.search(blurb[i]).group(0)
            blurb[i] = blurb[i].replace(level, '')

    return level


spells = get_html('https://pf2.d20pfsrd.com/spell')
pattern = re.compile('\"https://pf2\.d20pfsrd\.com/spell/.*\"')
spell_urls = pattern.findall(spells)
spells_dict = {}

words = {}


def create_entry(blurb):
    entry = {}
    if blurb:
        entry['Tags'] = blurb[0].split(' ')
        descriptors = ['Traditions', 'Range', 'Duration', 'Area', 'Domain'
                       'Target(s)', 'Mystery', 'Cast', 'Saving Throw', 'Targets']
        end = False
        i = 1
        while i < len(blurb) and end is False:
            line = blurb[i].split(';')
            for j in range(0, len(line)):
                if len(line[j].split(' ')) > 3:
                    first = line[j].split(' ')[0]
                    second = line[j].split(' ')[1]
                    if first in descriptors:
                        entry[first] = ' '.join(line[j].split(' ')[1:])
                    elif first + ' ' + second in descriptors:
                        entry[first + ' ' + second] = ' '.join(line[j].split(' ')[2:])
                    else:
                        end = True
                        break
                else:
                    break
            i += 1
        entry['description'] = blurb[i - 1:]
    return entry


for item in spell_urls[2:]:
    url = str(item).replace("\"", "")
    html = get_html(url)
    start = html.find('<h4 class="spell">')
    end = html.find('<div class="section15">')
    description = html[start:end]
    pattern = re.compile('[<#].*?[>;]')
    cleaned_description = pattern.sub("", description).split('\n')
    level = get_clean_level(cleaned_description)
    name = re.sub('(Spell( )?\d(\d)?)?(Cantrip( )?\d(\d)?)?(Focus( )?\d(\d)?)?',
                  '', cleaned_description[0].replace('&', '\'')).strip()
    cleaned_description = list(filter(lambda i: i != '', cleaned_description))
    spells_dict[name] = create_entry(cleaned_description[1:])
    spells_dict[name]['Level'] = level
    print(name)
    for key, value in spells_dict[name].items():
        print('%s: %s' % (key, value))
    print('\n\n\n')
print(sorted(words.items(), key=lambda x: x[1], reverse=True))
# printy = json.dumps(spells_dict)
# print(printy)
