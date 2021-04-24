from security import *
import pdb
import json

# pdb.set_trace()

# message
msg = 'super secret message XD'

encrypt_file('data/test', msg, 'key')

dec_msg = decrypt_file('data/test', 'key')

print(dec_msg)

# json
json_dict = { 'root' : {
    'item_1' : 'poggers',
    'item_2' : {
        'item_2_1' : ':]',
        'item_2_2' : {}
        }
    },
    'item_3' : 'lel'
}

encrypt_filesystem('data/test', json_dict, 'key')

dec_json = decrypt_filesystem('data/test', 'key')

dec_json_str = json.dumps(dec_json, indent=4)

print(dec_json_str)