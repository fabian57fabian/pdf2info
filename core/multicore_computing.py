import multiprocessing


def execute_parallel(all_data, function_for_chunk, DEBUG=False):
    """
    Prende in input una lista di dati (di qualsiasi natura) e una funzione da chiamare.
    Divide i dati in parti ed esegue la funzione passandogli una parte dei dati e un identificativo per tale processo.
    :param all_data: lista di object
    :param function_for_chunk: una funzione che prende in ingresso una lista di object ed un numero intero
    :return:
    """
    NUMBER_CORES = multiprocessing.cpu_count()
    processes = []
    chunk = len(all_data) / NUMBER_CORES
    if chunk != int(chunk):
        chunk = int(chunk) + 1
    else:
        chunk = int(chunk)
    for i in range(0, len(all_data), chunk):
        start = i
        end = min(i + chunk, len(all_data))
        if DEBUG: print("Generating chunk from %d to %d" % (start, end))
        part = all_data[start:end]
        p = multiprocessing.Process(target=function_for_chunk, args=(part, int(i / chunk)))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()


def simple_process(chunk, id):
    sum = 0
    for d in chunk:
        sum += d
    print("Job ended, pig #%d | Data size: %d | sum: %s" % (id, len(chunk), sum))


if __name__ == '__main__':
    # Test
    data = range(79)
    execute_parallel(data, simple_process)
