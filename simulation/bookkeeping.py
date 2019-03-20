import multiprocessing as mp
from stemp_abw.simulation.simulation import default_simulation_fct


def simulate_energysystem(esys):
    simulation_fct = default_simulation_fct
    results, parameters = multiprocess_energysystem(
        esys,
        simulation_fct)
    return results, parameters


def multiprocess_energysystem(esys, simulate_fct):
    queue = mp.Queue()
    p = mp.Process(
        target=queue_energysystem,
        args=(queue, esys, simulate_fct)
    )
    p.start()
    results = queue.get()
    p.join()
    return results


def queue_energysystem(queue, esys, simulate_fct):
    """
    All function in fcts are succesively run on energysystem
    """
    results = simulate_fct(esys)
    queue.put(results)
