import re
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

LLM_AGENTS = [
    'dialogue_phy_deepseekr1:70b_ass_llama3:8b_randomSet_icd10.txt',
    'dialogue_phy_llama3:70b_ass_llama3:8b_randomSet_icd10.txt',
    'dialogue_phy_gemma2_27b_ass_llama3_8b_randomSet_icd10.txt'
]

output_dir = Path('dataset/output_dialogues')
pattern = r"Finished Agent CP \((\d+)\)"

model_names = ['DeepSeek-R1:70B', 'Llama3:70B', 'Gemma2:27B']
model_results = {}
for idx, llm_agent in enumerate(LLM_AGENTS):
    print(llm_agent)
    with open(output_dir / llm_agent, "r") as file:
        lines = file.readlines()
    print(f'NUmber of lines {len(lines)}')
    for line in lines:
        matches = re.findall(pattern, line)
        result = list(map(int, matches))
        if len(result) == 0:
            continue
        if model_names[idx] not in model_results:
            model_results[model_names[idx]] = []
        model_results[model_names[idx]].append(result[0]-1)

# print(model_results)

plt.figure(figsize=(12, 6))

outlier_threshold = 100
for model_name, turns in model_results.items():
    print(model_name)
    print(np.mean(np.asarray(turns)))
    filtered_turns = [x for x in turns if x <= outlier_threshold]
    plt.hist(
        filtered_turns,
        bins=50,
        alpha=0.6,
        label=model_name,
        edgecolor='black'
    )

# Customize the plot
# plt.title("Turns Histogram")
plt.xlabel("Number of Turns")
plt.ylabel("Frequency")
plt.legend(loc='upper right')  # Display a legend for the models
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save plot to a file or display
plt.savefig("combined_histogram_with_outliers.pdf", format="pdf", bbox_inches="tight")
plt.show()