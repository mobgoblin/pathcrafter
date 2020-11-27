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
    # Example: Spell 2 --> level = 2, class = Spell
    classification = ''
    level = ''
    for i in range(0, len(blurb)):
        pattern = re.compile('(?!$)(Spell( )?\d(\d)?)?(Cantrip( )?\d(\d)?)?(Focus( )?\d(\d)?)?$')
        blurb[i] = blurb[i].replace('&nbsp;', '').strip()
        if pattern.search(blurb[i]):
            found = pattern.search(blurb[i]).group(0)
            classification = re.sub('[\d ]', '', found)
            level = re.sub('[\D ]', '', found)
            blurb[i] = blurb[i].replace(found, '')
    return [classification, level]


def create_descriptors(blurb, entry):
    descriptors = ['Traditions', 'Range', 'Duration', 'Area', 'Domain',
                   'Target(s)', 'Mystery', 'Cast', 'Saving Throw', 'Targets',
                   'Trigger', 'Requirements', 'Cost']
    for i in range(1, len(blurb)):
        line = blurb[i].split(';')
        for j in range(0, len(line)):
            split = line[j].strip().split(' ')
            if len(split) > 3:
                first = split[0]
                second = split[1]
                if first in descriptors:
                    entry[first] = ' '.join(split[1:])
                elif first + ' ' + second in descriptors:
                    entry[first + ' ' + second] = ' '.join(split[2:])
                else:
                    entry['Description'] = blurb[i:]
                    return

def create_entry(blurb):
    entry = {}
    if blurb:
        entry['Tags'] = blurb[0].split(' ')
        create_descriptors(blurb, entry)
    return entry


def clean(blurb):
    cleaned = re.sub('[<#].*?[>;]', '', blurb)
    cleaned = re.sub('&', '', cleaned)
    cleaned = re.sub(' ', ' ', cleaned)
    cleaned = re.sub('nbsp;', ' ', cleaned)
    return cleaned.split('\n')


def print_pretty(name):
    global spells_dict
    print(name)
    for key, value in spells_dict[name].items():
        print('%s: %s' % (key, value))
    print('\n\n\n')


spells = get_html('https://pf2.d20pfsrd.com/spell')
pattern = re.compile('\"https://pf2\.d20pfsrd\.com/spell/.*\"')
spell_urls = pattern.findall(spells)
spells_dict = {}

for item in spell_urls[2:]:
    url = str(item).replace("\"", "")
    html = get_html(url)
    start = html.find('<h4 class="spell">')
    end = html.find('<div class="section15">')
    description = html[start:end]
    cleaned_description = clean(description)
    class_level = get_clean_level(cleaned_description)
    classification = class_level[0]
    level = class_level[1]
    name = re.sub('(Spell( )?\d(\d)?)?(Cantrip( )?\d(\d)?)?(Focus( )?\d(\d)?)?',
                  '', cleaned_description[0].replace('&', '\'')).strip()
    cleaned_description = list(filter(lambda i: i != '', cleaned_description))
    spells_dict[name] = create_entry(cleaned_description[1:])
    spells_dict[name]['Classification'] = classification
    spells_dict[name]['Level'] = level
    # print_pretty(name)
printy = json.dumps(spells_dict)
print(printy)
