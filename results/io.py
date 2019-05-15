import json
import pandas as pd


def oemof_results_to_json(results, param_results):
    """Convert oemof raw results to json

    Parameters
    ----------
    results : :obj:`dict`
        Results from optimization as returned by
        :meth:`oemof.outputlib.processing.results()`
    param_results : :obj:`dict`
        Parameters of optimization as returned by
        :meth:`oemof.outputlib.processing.parameter_as_dict()`

    Returns
    -------
    JSON formatted :obj:`str`
        Serialized results, format:
        {'param_results':
            {'node_from_1':
                {'node_to_1': {'scalars': {'param_1': val_1,
                                           'param_2': val_2}
                              }
                }
            },
        'results':
            {'node_from_1':
                {'node_to_1': {'sequences': [n values]
                              }
                }
            }
        }

    Notes
    -----
    * Node keys in results and para_results must be provided as strings using
      :meth:`oemof.outputlib.processing.convert_keys_to_strings()`
    * In the sequences, timestamps are not preserved (values only)
    """
    data = {'results': {},
            'param_results': {}
            }

    ###########
    # Results #
    ###########
    for (n_from, n_to), val in results.items():
        if data['results'].get(n_from) is None:
            data['results'][n_from] = {}
        data['results'][n_from][n_to] =\
            {'sequences':
                 list(val['sequences'].to_dict()['flow'].values())
             }
    ##########
    # Params #
    ##########
    for (n_from, n_to), val in param_results.items():
        n_to2 = n_from if n_to == 'None' else n_to
        # if data['param_results'].get(n_from) is None:
        #     data['param_results'][n_from] = {}
        entry = {n_from:
                     {n_to2:
                          {'scalars':
                               val['scalars'].to_dict()
                           }
                      }
                 }
        if n_from in data['param_results'].keys():
            data['param_results'][n_from][n_to2] =\
                entry[n_from][n_to2]
        else:
            data['param_results'].update(entry)

    return json.dumps(data, sort_keys=True)


def oemof_json_to_results(results_json):
    """Convert stored oemof results json back to result dicts

    Parameters
    ----------
    results_json : JSON formatted :obj:`str`
        Format see :meth:`stemp_abw.results.tools.oemof_results_to_json()`

    Returns
    -------
    :obj:`dict`
        Results from optimization as returned by
        :meth:`oemof.outputlib.processing.results()`
        (sequences only without timestamps, no scalars)
    :obj:`dict`
        Parameters of optimization as returned by
        :meth:`oemof.outputlib.processing.parameter_as_dict()`
        (scalars only, no sequences)
    """
    data = json.loads(results_json)

    ###########
    # Results #
    ###########
    # make tuple keys from nested dict
    results = {}
    for n_from, val in data['results'].items():
        for n_to, val2 in val.items():
            results[(n_from, n_to)] = val2
    # convert seq to DF
    results = {nodes: {'sequences': pd.DataFrame(results[nodes]
                                                 ['sequences'])}
               for nodes, val in results.items()}
    ##########
    # Params #
    ##########
    # make tuple keys from nested dict
    param_results = {}
    for n_from, val in data['param_results'].items():
        for n_to, val2 in val.items():
            if n_from != n_to:
                param_results[(n_from, n_to)] = val2
            else:
                param_results[(n_from, 'None')] = val2

    # convert seq to Series
    param_results = {nodes: {'scalars': pd.Series(param_results[nodes]
                                                  ['scalars'])}
                     for nodes, val in param_results.items()}

    return results, param_results
