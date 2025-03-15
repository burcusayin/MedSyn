import re
import numpy as np
import pandas as pd
from typing import List
from argparse import ArgumentParser
from tqdm import tqdm
from src.evaluation.metrics import compute_icd10_metrics, compute_diagnosis_metrics
from src.evaluation.utils import assign_chapter

regex = r'\b[A-Z][0-9]{2,3}(?:\.[0-9]{1,3})?[A-Z]?\b'

def preprocess_gt_icd_code(text: str, main_disease: str = False)-> List[str]:
    '''function for extracting icd code of the ground truth'''
    text = text.strip('[').strip(']').replace('\'','').strip(' ').strip('\"')
    icds_as_list = text.split()
    icds_as_list = list(map(lambda x: x.replace(',', ''), icds_as_list))

    if main_disease == True:
        icds_as_list = list(map(lambda x: x.split('.')[0] if '.' in x else x, icds_as_list))
        assert len(icds_as_list) >= 1
    return set(icds_as_list)


def preprocess_llm_icd_code(text: str, main_disease: str = False) -> List[str]:
    if isinstance(text, float):
        print('Input of the text in llm_icd_code is none')
        return None
    text = text.split("codes=")[1].replace('\'', '').strip(' ').strip('\"')
    initial_icd_code = text
    text = text.replace('and', '')
    text = text.replace(',', '')
    identified_icds = set()
    if '.' not in text:
        icd_codes = text.split()
        for icd_code in icd_codes:
            identified_icds.add(icd_code)
        if len(identified_icds) == 0:
            identified_icds.add('Not assigned')
        return identified_icds

    icd_codes = set(re.findall(regex, text))
    if len(icd_codes) == 0:
        identified_icds.add(initial_icd_code)
        return identified_icds


    for icd_code in icd_codes:
        if '(' in text:
            text = text.split('(')
            text = text[0].strip()
            identified_icds.add(icd_code)
        else:
            identified_icds.add(icd_code)

    identified_icds = list(identified_icds)
    if main_disease == True:
        identified_icds = list(map(lambda x: x.split('.')[0] if '.' in x else x, identified_icds))
    if len(identified_icds) == 0:
        print(text)

    return set(identified_icds)

def assign_chapter_of_diseases(diseases: List[str]) -> List[str]:
    if not diseases:
        print('the diseases are empty in chapter of diseases func')
        return None
    chapters = set()
    for disease in diseases:
        chapters.add(assign_chapter(disease))
    return chapters

def preprocess_gt_diagnosis(diagnosis: str):
    if isinstance(diagnosis, float):
        print('the diagnosis is empty in preprocess gt diagnosis')
        return None
    diagnosis = diagnosis.replace('___', '')
    diagnosis = re.sub(r'[-#\d+\.]|\d+\)', '', diagnosis)
    diagnosis = re.sub(r'\s+', ' ', diagnosis).strip()
    if '=' in diagnosis:
        diagnosis = re.sub(r'[-=]+', '', diagnosis)
        diagnosis = re.sub(r'\s+', ' ', diagnosis)
        diagnosis = re.sub(r'^\s*|\s*$', '', diagnosis)
    return diagnosis

def preprocess_llm_diagnosis(text: str) -> str:
    if isinstance(text, float):
        print('the diagnosis is empty in preprocess llm diagnosis')
        return None
    text = text.split("diagnosis=", 1)[1].split("codes=")[0].replace('\'','').strip(' ').strip('\"')
    return text

LLM_AGENTS = [
    'baseline_phy_llama8b_output',
    'baseline_phy_llama70b_output',
    'baseline_ass_llama8b_output',
    'baseline_ass_llama70b_output',
    'two_agent_phy_llama70b_ass_llama8b_output',
    'baseline_phy_deepseek70b_output',
    'baseline_ass_deepseek70b_output',
    'two_agent_phy_deepseek70b_ass_llama8b_output',
    'baseline_phy_gemma27b_output',
    'baseline_ass_gemma27b_output',
    'two_agent_phy_llama70b_ass_gemma27b_output',
    'two_agent_phy_gemma27b_ass_llama8b_output',
    'two_agent_phy_gemma27b_ass_gemma27b_output'
]

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    results = pd.read_csv(input_file)

    print(results.columns)

    results['gt_icd10_diag'] = results['icd10_diag'].apply(lambda x: preprocess_gt_icd_code(x))
    results['gt_icd10_diag_main_disease'] = results['icd10_diag'].apply(lambda x: preprocess_gt_icd_code(x, main_disease=True))
    results['gt_icd10_diag_disease_chapter'] = results['gt_icd10_diag_main_disease'].apply(lambda x: assign_chapter_of_diseases(x))
    results['gt_discharge_diag'] = results["discharge diagnosis"].apply(lambda x: preprocess_gt_diagnosis(x))

    problematic_indices = []
    none_values = results.index[results['gt_discharge_diag'].isna()].tolist()
    problematic_indices.extend(none_values)

    print('problematic indices')
    print(problematic_indices)

    for llm_agent in LLM_AGENTS:
        results[f'{llm_agent}_icd10_diag'] = results[llm_agent].apply(lambda x: preprocess_llm_icd_code(x))
        results[f'{llm_agent}_icd10_diag'] = results[f'{llm_agent}_icd10_diag'].apply(lambda x: None if x==None or len(x)==0 else x)
        none_values = results.index[results[f'{llm_agent}_icd10_diag'].isna()].tolist()

        if len(none_values) > 0:
            print(f'{llm_agent} has {len(none_values)} none values')
            problematic_indices.extend(none_values)
            print(f'Indices for none values {none_values}')

        results[f'{llm_agent}_icd10_diag_main_disease'] = results[llm_agent].apply(lambda x: preprocess_llm_icd_code(x, main_disease=True))
        results[f'{llm_agent}_icd10_diag_disease_chapter'] = results[f'{llm_agent}_icd10_diag_main_disease'].apply(
            lambda x: assign_chapter_of_diseases(x))
        results[f'{llm_agent}_discharge_diag'] = results[llm_agent].apply(lambda x: preprocess_llm_diagnosis(x))
    results.to_json(output_file, orient='records', lines=True)
    results.to_csv(output_file, index=False)
    # # TODO: fix it, none values should be with values
    results = results.drop(results.index[problematic_indices])
    for llm_agent in LLM_AGENTS:
        print(f'Predictions of {llm_agent}')

        print('Avg length of GT ICD codes')
        flattened_gt_icd10 = [len(item) for s in results['gt_icd10_diag'] for item in s]
        print(round(np.mean(np.asarray(flattened_gt_icd10)), 2))

        print(f'Avg length of {llm_agent} ICD codes')
        flattened_gt_icd10 = [len(item) for s in results[f'{llm_agent}_icd10_diag_main_disease'] for item in s]
        print(round(np.mean(np.asarray(flattened_gt_icd10)), 2))

        scores = compute_icd10_metrics(results['gt_icd10_diag'].tolist(), results[f'{llm_agent}_icd10_diag'].tolist())
        print('Scores for ICD10 main disease+child disease')
        print(scores)

        print('Disease Category')
        scores = compute_icd10_metrics(results['gt_icd10_diag_main_disease'].tolist(), results[f'{llm_agent}_icd10_diag_main_disease'].tolist())
        print(scores)

        print('Disease Chapter')
        scores = compute_icd10_metrics(results['gt_icd10_diag_disease_chapter'].tolist(), results[f'{llm_agent}_icd10_diag_disease_chapter'].tolist())
        print(scores)