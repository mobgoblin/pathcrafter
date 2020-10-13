import json
import urllib.request
import re

def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    value = mybytes.decode("utf8")
    fp.close()
    return value;

def get_level(blurb):
    level = ''
    for item in blurb:
        pattern = re.compile('(?!$)(Spell\d)?(Cantrip\d)?(Focus\d)?$')
        if pattern.search(item.strip()):
            level = pattern.search(item.strip()).group(0)
    return level

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
    pattern = re.compile('[<#].*?[>;]')
    cleaned_description = pattern.sub("", description).split('\n')
    level = get_level(cleaned_description)
    name = re.sub('((Spell\d)?(Cantrip\d)?(Focus\d)?)+', '', cleaned_description[0])
    spells_dict[name] = {'level': level, 'description': cleaned_description[1:]}
printy = json.dumps(spells_dict)
print(printy)
