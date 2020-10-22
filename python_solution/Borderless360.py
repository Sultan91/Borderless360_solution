import os
import json


class OrderHistory(object):
    ''' Reads json data and compares dict values between two neighboring Order history results '''
    def __init__(self):
        self.focus_detail_keys = ['customs_id']

    def dict_diff(self, dict1:dict, dict2:dict):
    	''' Determine mismatching values in two dicts '''
        keys = list(dict1.keys())
        diffs = {}
        if keys == list(dict2.keys()):
            for k in keys:
                if isinstance(dict1[k], dict):
                    temp = self.dict_diff(dict1[k], dict2[k])
                    if len(temp)>0:
                        diffs[k] = temp
                else:
                    if dict1[k] != dict2[k]:
                        diffs[k] = [dict1[k], dict2[k]]
            return diffs
        return diffs

    def get_changes(self, dict1:dict, dict2:dict):
    	''' Returns total mismatching key-value paris that given two order history results have'''
        keys = list(dict1.keys())
        if keys == list(dict2.keys()):
            diffs = self.dict_diff(dict1, dict2)
            return diffs

    def display_details(self, key, res:dict)->str:
    	'''General method that records changes in a string and outputs 'em to STDOUT'''
        if key in res.keys():
            fulfil_diffs = self.get_changes(res[key][0][0], res[key][1][0])
            out_str = ""
            for k in fulfil_diffs.keys():
                if isinstance(fulfil_diffs[k], list):
                    out_str += k + ": " + str(fulfil_diffs[k][0]) + " -> " + str(fulfil_diffs[k][1]) + "; "
                elif isinstance(fulfil_diffs[k], dict):
                    for sub_k in fulfil_diffs[k].keys():
                        if isinstance(fulfil_diffs[k][sub_k], list):
                            out_str += k + ": " + str(fulfil_diffs[k][sub_k][0]) + " -> " + str(fulfil_diffs[k][sub_k][1]) + "; "
            return out_str
        return ""

    def check_file(self, f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            results = data['results']
            print("/////////////////////////          ORDER HISTORY         ////////////////////////////////////\n")
            outputs = []
            for i in range(len(results) - 2, 0, -1):
                res = self.get_changes(results[i]['model_data'], results[i + 1]['model_data'])
                user_info = results[i]['user']
                if user_info is not None:
                    username = 'System' if user_info['username'] == '' else user_info['username']
                else:
                    username = 'System'
                event_type = "NEW ACTION" if results[i]['event_type'] == 'transition' else "ORDER UPDATED"
                status = results[i]['model_data']['status_display']
                # print(res)
                out_str ="\n---------------------------------------------------------------\n"
                if results[i]['event_type'] != 'updated':
                    out_str += f"{username}, {event_type}: {status}\n"
                elif results[i]['event_type'] == 'updated':
                    out_str += f"{username}, {event_type}: {status}\n"
                    # details
                    out_str = self.display_details('fulfillments', res)
                    out_str += self.display_details('order_items', res)
                    for fk in self.focus_detail_keys:
                        if fk in res.keys():
                            out_str += f"{fk}: {str(res[fk][0])} -> {str(res[fk][1])}"
                outputs.append(out_str)
            reversed(outputs)
            for o in outputs:
                print(o)


if __name__ == '__main__':
    folder = "../data/"
    files = os.listdir(folder)
    f_path = os.path.join(folder, files[2])
    oh = OrderHistory()
    oh.check_file(f_path=f_path)


