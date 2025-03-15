#!/bin/bash
#SBATCH -p long-disi
#SBATCH --gres=gpu:a100.80:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem-per-cpu=4096
#SBATCH -N 1
#SBATCH --error=/home/error/baseline_phy_deepseek-r1:70b_randomSet.err
#SBATCH --output=/home/output/baseline_phy_deepseek-r1:70b_randomSet.txt


MAIN_DIR=/home/


cd ${MAIN_DIR}
pwd

ollama serve &

# Wait until Ollama service has been started
sleep 2

echo "Server started"


#ollama run command-r-plus:104b
#ollama run command-r:35b
#ollama run openchat:7b 
#ollama run mistral:7b-instruct-v0.2-q8_0
#ollama run mistrallite:7b
#ollama run mixtral:8x7b
#ollama run qwen2:7b
#ollama run meditron:7b 
#ollama run meditron:70b
#ollama run medllama2:7b  
#ollama run llama3-chatqa:8b
#ollama run llama3-chatqa:70b
#ollama run llama3:8b
#ollama run llama3:70b
#ollama run llama3.1:8b
#ollama run llama3.2:3b
#ollama run dolphin-llama3:8b
#ollama run dolphin-llama3:70b
#ollama run phi3:14b
#ollama run nemotron:70b
#ollama run alfred:40b
#ollama run llama3.3:70b
#ollama run mistral-nemo:12b
#ollama run dolphin-llama3:8b
#ollama run dolphin-llama3:70b
#ollama run zephyr:7b
#ollama run zephyr:141b
#ollama run neural-chat:7b
#ollama run tulu3:8b
#ollama run tulu3:70b
#ollama run deepseek-r1:14b
#ollama run deepseek-r1:32b
ollama run deepseek-r1:70b
#ollama run gemma2:27b

BASELINE_MODEL=deepseek-r1:70b

ollama ps

python ${MAIN_DIR}src/main.py \
--input_file ${MAIN_DIR}dataset/mimiciv/3.1/preprocessed/mimicIV_1000_random_sample_filtered_parsed_icd10.csv \
--history_file ${MAIN_DIR}output/dialogues/physician_agent/random/  \
--discharge_data_file ${MAIN_DIR}output/discharge_texts/random/ \
--mode phy_baseline \
--baseline_model $BASELINE_MODEL \
--baseline_system_prompt ${MAIN_DIR}prompts/baseline_system.txt \
--baseline_prompt_template ${MAIN_DIR}prompts/baseline_user.txt 
