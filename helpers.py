from collections import OrderedDict


def order_dict(dictionary):
    """Order dictionary recursively"""
    return OrderedDict({k: order_dict(v) if isinstance(v, dict) else v
                        for k, v in sorted(dictionary.items())})
