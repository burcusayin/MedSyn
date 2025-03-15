import ast
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input')

    args = parser.parse_args()
    input_file = args.input

    results = pd.read_csv(input_file)
    icd_codes = results['gt_icd10_diag'].tolist()
    print(icd_codes[:6])

    codes = []
    for icd_code_set in icd_codes:

        codes.extend(ast.literal_eval(icd_code_set))
    print(f'number of the codes: {len(codes)}')
    print(f'number of unique codes: {len(set(codes))}')

    occurrences = Counter(codes)
    rare_diagnosis = [key for key in occurrences if all(occurrences[temp] >= occurrences[key] for temp in occurrences)]
    common_diagnosis = [key for key in occurrences if
                        all(occurrences[temp] <= occurrences[key] for temp in occurrences)]
    print("rare_diagnosis: ", rare_diagnosis)
    print(len(rare_diagnosis))
    print(occurrences['H53.40'])
    print("common_diagnosis: ", common_diagnosis)