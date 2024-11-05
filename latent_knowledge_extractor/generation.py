'''
This script is to check the generation of each LKEs to evaluate the exact matching accuracy.
'''
import yaml
import os
import json
import numpy as np

from .construct_prompt import ConstructPrompt
from .vllm_inference import VllmInference

class Generation:
    '''
    Implimentationi based on vllm, check the next 50 tokens as the model response.
    '''
    def __init__(self, config_path):
        """
        Initialize the generation class by loading the configuration from a YAML file.
        """
        self.config = self.read_config(config_path) 
        self.config_path = config_path
        self.model_name = self.config.get('model_name')
        self.test_dataset_name = self.config.get('test_dataset_name')
        self.test_relation_id = self.config.get('test_relation_id')
        self.lke_type = self.config.get('lke_type')
        self.lke_index = self.config.get('lke_index')
        self.save_path = self.config.get('save_path')
        self.config_path = config_path
        self.random_seed = self.config.get('random_seed')
    
    def read_config(self, path):
        """
        Read the YAML configuration file and return the config dictionary.
        """
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def inference(self):
        prompt_constructor = ConstructPrompt(self.config_path)
        _, base_prompts = prompt_constructor.construct_prompt()
        _, df_test = prompt_constructor.load_data()

        inference_agent = VllmInference(self.config_path)
        model, sampling_params = inference_agent.load_model()
        outputs = model.generate(base_prompts, sampling_params)
        #get the output text
        responses = []
        for output in outputs:
            responses.append(output.outputs[0].text)
        return responses, base_prompts, df_test['Object'].tolist()
    
    def get_generation_acc(self, ground_truth, response):
        #lower case for both ground_truth and response
        ground_truth = [x.lower() for x in ground_truth]
        response = [x.lower() for x in response]
        #remove all the special characters like : , . etc.
        ground_truth = [x.replace(':', '').replace(',', '').replace('.', '') for x in ground_truth]
        generation_acc = []
        for i in range(len(ground_truth)):
            if ground_truth[i] in response[i]:
                generation_acc.append(1)
            else:
                generation_acc.append(0)
        acc = np.mean(generation_acc)
        return acc

    def save_outputs(self, outputs, base_prompts, ground_truth):
        '''
        Save the outputs to a JSON file.
        '''
        acc = self.get_generation_acc(ground_truth, outputs)
        dict_to_save = {
            'base_prompts': base_prompts,
            'ground_truth': ground_truth,
            'outputs': outputs,
            'generation_acc': acc
        }
        save_folder = f'{self.save_path}/generation/{self.lke_type}/{self.lke_index}/{self.model_name}/{self.test_dataset_name}/{self.test_relation_id}'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        #save all the outputs into random_seed-{random_seed}.json
        save_path = f'{save_folder}/random_seed-{self.random_seed}.json'
        with open(save_path, 'w') as file:
            json.dump(dict_to_save, file)
        print(f'Outputs saved to {save_path}')
        
        return acc


def main(
    config_path = '/NS/llm-1/work/qwu/lke_open_code/config/test.yaml'
):
    generation = Generation(config_path)
    outputs, base_prompts, ground_truth = generation.inference()
    acc=generation.save_outputs(outputs, base_prompts, ground_truth)
    print(f'Generation accuracy: {acc}')
    

if __name__ == '__main__':
    main()