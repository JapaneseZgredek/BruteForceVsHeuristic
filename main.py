import sys
from concurrent.futures import ThreadPoolExecutor
from dataset import Dataset
import random
from time import time

global should_run


def read_dataset(list_to_create_dataset_from: list) -> Dataset:
    dataset_to_return = Dataset()
    dataset_to_return.init_sizes(list(map(int, list_to_create_dataset_from[1].split('=')[1].replace(' ', '').replace('{', '').replace('}', '').split(','))))
    dataset_to_return.init_vals(list(map(int, list_to_create_dataset_from[2].split('=')[1].replace(' ', '').replace('{', '').replace('}', '').split(','))))
    return dataset_to_return


def read_data():
    with open('data/plecak.txt', 'r') as f:
        file_content = f.read().split('\n')
    length = int(file_content[0].split(' ')[2].replace(',', ''))
    capacity = int(file_content[0].split(' ')[4])
    i, j = 1, 4
    datasets_list = []
    while i+4 <= len(file_content):
        datasets_list.append(read_dataset(file_content[i:j]))
        i += 4
        j += 4
    return length, capacity, datasets_list


def brudas_force(dataset_to_work_on: Dataset, length: int, capacity: int):
    start = time()
    number_of_possibilities = 2 ** length
    winning_set = []
    max_value = 0
    min_size_taken = sys.maxsize
    for i in range(1, number_of_possibilities):
        if not should_run:
            return (time() - start), winning_set, max_value, min_size_taken
        current_indexes, current_size, current_value = calculate_on_current_possible_set(i, dataset_to_work_on.sizes.copy(), dataset_to_work_on.vals.copy(), capacity)
        if current_size is None:
            continue
        if current_value > max_value:
            max_value, min_size_taken, winning_set = current_value, current_size, current_indexes
            continue
        if current_value == max_value:
            if current_size < min_size_taken:
                max_value, min_size_taken, winning_set = current_value, current_size, current_indexes
                continue
    return (time() - start), winning_set, max_value, min_size_taken


def calculate_on_current_possible_set(i, sizes, values, capacity):
    binary_representation = bin(i)[2:]
    indexes = [i for i, bit in enumerate(binary_representation) if bit == '1']
    size = sum(sizes[i] for i in indexes)
    value = sum(values[i] for i in indexes)
    values_not_used = [values[x] for x in range(len(values)) if x not in indexes]
    if size > capacity or size + min(values_not_used) < capacity:
        return None, None, None
    return indexes, size, value


def sorting_based_on_ratio(ratio, sizes, values):



def autistic_heuristic(dataset_to_work_on: Dataset, length: int, capacity: int):
    ratio = [dataset_to_work_on.vals[i]/dataset_to_work_on.sizes[i] for i in range(len(dataset_to_work_on.vals))]
    sorting_based_on_ratio(ratio)


def main():
    length, capacity, datasets_list = read_data()
    dataset_number = random.randint(0, len(datasets_list))
    dataset_to_work_on = datasets_list[dataset_number]
    global should_run
    should_run = True
    pool = ThreadPoolExecutor(2)
    print("FIGHT!!!")
    #brudas = pool.submit(brudas_force, dataset_to_work_on, length, capacity)
    pool.submit(autistic_heuristic, dataset_to_work_on, length, capacity)
    #time_needed, winning_set, value, size_taken = brudas.result()
    #print(f'Brudas force needed: {time_needed}\nWinning set is: {winning_set}\nValue: {value}\nSize taken:{size_taken}')


if __name__ == '__main__':
    main()
