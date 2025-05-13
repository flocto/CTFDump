import json

content = open('OLDproject.json').read()
# replace unicode i with I
escaped = content.replace('\u0456', 'I')
project = json.loads(escaped)

targets = project['targets']

import random
def getrandname():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))

for i in range(len(targets)):
    parent = {}
    for j in targets[i]['blocks']:
        x = targets[i]['blocks'][j]

        print(j, x)
        # if 'x' in x:
        #     x['x'] = -200
        # if 'y' in x:
        #     x['y'] = -200
        if 'shadow' in x:
            x['shadow'] = False
        # if x['parent'] is not None:
        #     if x['parent'] not in parent:
        #         parent[x['parent']] = []
        #     parent[x['parent']].append(j)
    
    # for j in targets[i]['blocks']:
    #     x = targets[i]['blocks'][j]
    #     if x['next'] is None:
    #         if j in parent and len(parent[j]) >= 1:
    #             x['next'] = parent[j][0]
    #     print(j, x)
                
        
with open('project.json', 'w') as f:
    json.dump(project, f)