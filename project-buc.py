# run in python >= 3.9

import re
import itertools

def pre_process(input_file_name: str) -> list[dict]:
    """Convert records to dict: {"A": 0 or 1, ...}"""

    out_list = []

    with open(input_file_name, "r") as dataset:
        #for line in itertools.islice(dataset, 1000):
        for line in dataset:
            out_line = {}

            if re.search(r"\b[0-3]\b", line):
                out_line["A"] = 1
            else:
                out_line["A"] = 0

            if re.search(r"\b[4-7]\b", line):
                out_line["B"] = 1
            else:
                out_line["B"] = 0

            if re.search(r"\b[8-9]\b|\b1[01]\b", line):
                out_line["C"] = 1
            else:
                out_line["C"] = 0

            if re.search(r"\b1[2-5]\b", line):
                out_line["D"] = 1
            else:
                out_line["D"] = 0

            if re.search(r"\b1[6-9]\b", line):
                out_line["E"] = 1
            else:
                out_line["E"] = 0

            out_list.append(out_line)

    return out_list

def cell_repr(cell: dict) -> str:

    global cell_counter
    cell_counter += 1
    return f"({cell.get('A')}, {cell.get('B')}, {cell.get('C')}, {cell.get('D')}, {cell.get('E')})"

def buc(input: list[dict], dim_index: int, cell: dict):
    """Bottom-up computation of Iceberg CUBE"""

    dims = ['A', 'B', 'C', 'D', 'E']
    attr = [0, 1]

    global min_sup

    for cur_dim in dims[dim_index:]:
        
        aggr_list_1 = [] 
        aggr_list_0 = [] 

        for row in input:
            if row.get(cur_dim) == 1:
                aggr_list_1.append(row)
            else:
                aggr_list_0.append(row)

        datacount = [len(aggr_list_0), len(aggr_list_1)]

        if datacount[1] >= min_sup:  # Pruning
            
            cell_copy = cell.copy()  # Shallow Copy
            cell_copy[cur_dim] = "1"
            print(f"{cell_repr(cell_copy)}: {datacount[1]}")

            if (index:= dims.index(cur_dim) + 1) < len(dims):
                buc(aggr_list_1, index, cell_copy)

        if datacount[0] >= min_sup:  # Pruning
        
            cell_copy = cell.copy()
            cell_copy[cur_dim] = "0"
            print(f"{cell_repr(cell_copy)}: {datacount[0]}")

            if (index:= dims.index(cur_dim) + 1) < len(dims):
                buc(aggr_list_0, index, cell_copy)

def main():

    global cell_counter
    cell_counter = 2  # including (0, 0, ...) and (*, *, ...) cells.

    global min_sup
    min_sup = 1000

    cell = {"A":"*", "B":"*", "C":"*", "D":"*", "E":"*"}

    input_records = pre_process("Dataset.txt")

    buc(input_records, 0, cell)

    print(f"\n({('0, ' * len(cell))[:-2]}): 0")
    print(f"({('*, ' * len(cell))[:-2]}): {len(input_records)}")

    print("------------------------------")

    print("Cell Counts:", cell_counter)
    print("Pruned Cells:", 3 ** len(cell) - cell_counter)

if __name__ == "__main__":
    main()