import multiprocessing as mp
from stemp_abw.simulation.simulation import default_simulation_fct


def simulate_energysystem():
    #energysystem = session.energysystem
    simulation_fct = default_simulation_fct
    results, parameters = multiprocess_energysystem(
        simulation_fct)
    return results, parameters


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
