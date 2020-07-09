import json
import os
from collections import defaultdict

def parse_object_pairs(pairs):
    
    pairs_str = str(pairs)
    if "Participant_Admin" in pairs_str or u"Participant_Admin" in pairs_str:
        permissions = {}
        for pair in pairs:
            role, transition_permissions_list = pair
            if role not in permissions:
                permissions[role] = {}
            transition_name, transition_permissions = transition_permissions_list[0]
            permissions[role][transition_name] = transition_permissions
        return permissions
    elif isinstance(pairs[0][1], dict):
        return pairs
    else:
        condensed_permissions = {
            'read': [],
            'read_write': [],
            'none': []
        }
        for pair in pairs:
            field, permission = pair
            if permission in ('read', 'read_write'):
                condensed_permissions[permission].append(field)
            elif permission is None:
                condensed_permissions['none'].append(field)
        return condensed_permissions


def get_optimized_obj(obj):
    optimized_obj = {}
    all_fields = set()
    for user in obj:
        optimized_obj[user] = {
            'default_permissions': {
                'read': [],
                'read_write': [],
                'none': []
            }
        }

        counts = {
            'read': defaultdict(int),
            'read_write': defaultdict(int),
            'none': defaultdict(int)
        }
        
        for transition in obj[user]:
            for permission in obj[user][transition]:
                for field in obj[user][transition][permission]:
                    all_fields.add(field)
                    counts[permission][field] += 1
        
        for field in all_fields:
            most_common_permission = max(counts, key = lambda k: counts[k][field])
            optimized_obj[user]['default_permissions'][most_common_permission].append(field)

        for transition in obj[user]:
            if transition is 'default_permissions':
                continue
            optimized_obj[user][transition] = {}
            for permission in obj[user][transition]:
                fields = obj[user][transition][permission]
                optimized_obj[user][transition][permission] = \
                    [f for f in fields if f not in optimized_obj[user]['default_permissions'][permission]]
    return optimized_obj
    # import pdb; pdb.set_trace()



script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
input_rel_path = '../participant_permissions.json'
output_rel_path = '../optimized_participant_permissions.json'
abs_file_path = os.path.join(script_dir, input_rel_path)
new_file_path = os.path.join(script_dir, output_rel_path)
print(abs_file_path)
with open(abs_file_path) as json_file:
    data = json_file.read().replace('\n', '')
    decoder = json.JSONDecoder(object_pairs_hook=parse_object_pairs)
    obj = decoder.decode(data)
    optimized_obj = get_optimized_obj(obj)
    with open(new_file_path, 'w') as outfile:
        json.dump(optimized_obj, outfile)
