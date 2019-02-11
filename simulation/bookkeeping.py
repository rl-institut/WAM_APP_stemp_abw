import multiprocessing as mp
from stemp_abw.simulation.simulation import simulation_fct_test


def simulate_energysystem():
    #energysystem = session.energysystem
    simulation_fct = simulation_fct_test
    result, param_result = multiprocess_energysystem(
        simulation_fct)
    return result, param_result


# TODO: Create user-dependent pool in settings
def multiprocess_energysystem(simulate_fct):
    queue = mp.Queue()
    p = mp.Process(
        target=queue_energysystem,
        args=(queue, simulate_fct)
    )
    p.start()
    results = queue.get()
    p.join()
    return results


def queue_energysystem(queue, simulate_fct):
    """
    All function in fcts are succesively run on energysystem
    """
    results = simulate_fct()
    queue.put(results)
