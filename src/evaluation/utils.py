'''
This code based on https://github.com/JoakimEdin/medical-coding-reproducibility/blob/main/notebooks/code_analysis.ipynb
'''

chapter2name = {
    "A00-B99": "Certain infectious and parasitic diseases",
    "C00-D49": "Neoplasms",
    "D50-D89": "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
    "E00-E89": "Endocrine, nutritional and metabolic diseases",
    "F01-F99": "Mental, Behavioral and Neurodevelopmental disorders",
    "G00-G99": "Diseases of the nervous system",
    "H00-H59": "Diseases of the eye and adnexa",
    "H60-H95": "Diseases of the ear and mastoid process",
    "I00-I99": "Diseases of the circulatory system",
    "J00-J99": "Diseases of the respiratory system",
    "K00-K95": "Diseases of the digestive system",
    "L00-L99": "Diseases of the skin and subcutaneous tissue",
    "M00-M99": "Diseases of the musculoskeletal system and connective tissue",
    "N00-N99": "Diseases of the genitourinary system",
    "O00-O9A": "Pregnancy, childbirth and the puerperium",
    "P00-P96": "Certain conditions originating in the perinatal period",
    "Q00-Q99": "Congenital malformations, deformations and chromosomal abnormalities",
    "R00-R99": "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",
    "S00-T88": "Injury, poisoning and certain other consequences of external causes",
    "U00-U85": "Codes for special purposes",
    "V00-Y99": "External causes of morbidity",
    "Z00-Z99": "Factors influencing health status and contact with health services",
}

name2chapter = {v: k for k, v in chapter2name.items()}

letter2name = {
    "A": "Certain infectious and parasitic diseases",
    "B": "Certain infectious and parasitic diseases",
    "C": "Neoplasms",
    "E": "Endocrine, nutritional and metabolic diseases",
    "F": "Mental, Behavioral and Neurodevelopmental disorders",
    "G": "Diseases of the nervous system",
    "I": "Diseases of the circulatory system",
    "J": "Diseases of the respiratory system",
    "K": "Diseases of the digestive system",
    "L": "Diseases of the skin and subcutaneous tissue",
    "M": "Diseases of the musculoskeletal system and connective tissue",
    "N": "Diseases of the genitourinary system",
    "O": "Pregnancy, childbirth and the puerperium",
    "P": "Certain conditions originating in the perinatal period",
    "Q": "Congenital malformations, deformations and chromosomal abnormalities",
    "R": "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",
    "S": "Injury, poisoning and certain other consequences of external causes",
    "T": "Injury, poisoning and certain other consequences of external causes",
    "U": "Codes for special purposes",
    "V": "External causes of morbidity",
    "W": "External causes of morbidity",
    "Y": "External causes of morbidity",
    "X": "External causes of morbidity",
    "Z": "Factors influencing health status and contact with health services",
}


def difficult_chapters(x: str) -> str:
    if "D" in x:
        if "3A" in x:
            return "Neoplasms"
        if isinstance(x[1:], str):
            return x
        if int(x[1:]) < 50:
            return "Neoplasms"
        else:
            return "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism"

    if "H" in x:
        if int(x[1:]) < 60:
            return "Diseases of the eye and adnexa"
        else:
            return "Diseases of the ear and mastoid process"

def assign_chapter(icd_code:str)->str:
    chapter  = letter2name.get(icd_code[0])
    if not chapter:
        chapter = difficult_chapters(icd_code)
    return chapter

if __name__ == '__main__':
    icd_code = 'D30'
    print('ICD-Code')
    chapter = assign_chapter(icd_code)
    print(chapter)