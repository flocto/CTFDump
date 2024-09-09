import bs4
from collections import Counter

html = open('dump.html').read()

soup = bs4.BeautifulSoup(html, 'html.parser')
out = ""

depths = Counter()

def recurse(tag):
    global out
    for child in tag.children:
        if child.name:
            # if 'class' in child.attrs:
            #     print(child.attrs['class'])
            #     if 'reduction-beta-child' in child.attrs['class']:
            #         out += '\n'
                
            recurse(child)
            
            if 'class' in child.attrs:
                print(child.attrs['class'])
                if 'reduction-beta-child' in child.attrs['class']:
                    out += '\n'
                if 'term-variable' in child.attrs['class']:
                    out += ' '

                for c in child.attrs['class']:
                    if c.startswith('reduction-depth-'):
                        depths[c] += 1
        else:
            # print(child)
            out += child

recurse(soup)
print(depths)

# print(out)
open('dump/dump.lc', 'w').write(out)
