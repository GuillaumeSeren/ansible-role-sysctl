from ansible.utils.display import Display
display = Display()


class FilterModule(object):

    # Declare available filter with external names
    def filters(self):
        return {
            'override': self.override,
            'flatten_item': self.flatten_item,
            'compare_dict': self.compare_dict,
            'compare_dict_changed': self.compare_dict_changed,
            'compare_dict_same': self.compare_dict_same
        }

    # Override dict_a with dict_b
    # dict_a is a list of dict like users
    # dict_b is a dict of value to override like override
    def override(self, dict_a, dict_b):
        for overb in dict_b:
            # each override key
            for key in dict_a:
                for overa in key:
                    # Check if overa exist in dict_b
                    if overa in dict_b:
                        # the override
                        key.update(dict_b)
        return dict_a

    # Convert your value content after a dict2item
    # to be key, value for easy target
    def flatten_item(self, dict_a):
        ret = []
        # loop over dict_a
        for element in dict_a:
            value_ret = []
            if 'value' in element.keys():
                for value_element in element['value']:
                    value_ret.append({'key': value_element, 'value': element['value'][value_element]})
                element.update({'value': value_ret})
            ret.append(element)
        return ret

    # Compare two dict in the difference filter fashion
    #
    # dict_a the active element
    # dict_b the reference element
    # output_filter select filter element to output
    # if key = key and value != value override value
    def compare_dict(self, dict_a, dict_b, output_filter='NO'):
        ret = {}
        # compare key on first level should be both defined
        # Check that reference element
        for dict_b_key in dict_b:

            # @TODO Maybe also check if dict_b[key] is a dict
            if type(dict_b[dict_b_key]) == type({}):
                # lets iterate on inner dict
                if dict_b_key not in dict_a:
                    dict_a[dict_b_key] = dict_b[dict_b_key]

                iterate_inner = FilterModule.compare_dict(self, dict_a[dict_b_key], dict_b[dict_b_key], output_filter)
                if iterate_inner:
                    ret[dict_b_key] = iterate_inner
            else:
                if dict_b_key in dict_a:
                    if dict_a[dict_b_key] != dict_b[dict_b_key] and output_filter == 'CHANGED':
                        # if it is the same override with the reference value
                        ret[dict_b_key] = dict_b[dict_b_key]
                    elif dict_a[dict_b_key] == dict_b[dict_b_key] and output_filter == 'SAME':
                        ret[dict_b_key] = dict_b[dict_b_key]
                    elif output_filter == 'NO':
                        ret[dict_b_key] = dict_b[dict_b_key]

        return ret

    # Compare two dict in the difference filter fashion, output only changed
    # dict_a the active element
    # dict_b the reference element
    def compare_dict_changed(self, dict_a, dict_b):
        ret = {}
        ret = FilterModule.compare_dict(self, dict_a, dict_b, 'CHANGED')
        return ret

    # Compare two dict in the difference filter fashion, output only same
    # dict_a the active element
    # dict_b the reference element
    def compare_dict_same(self, dict_a, dict_b):
        ret = {}
        ret = FilterModule.compare_dict(self, dict_a, dict_b, 'SAME')
        return ret
