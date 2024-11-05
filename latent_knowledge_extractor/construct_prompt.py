'''
Construct the prefix for all kinds of LKEs
'''
import logging
import os
import pandas as pd
import yaml
import random
import json
import ast
from datasets import load_dataset

from .prompt_template import MMP_TEMPLATES, HGP_TEMPLATES

class ConstructPrompt:
    def __init__(self, config_path):
        """
        Initialize the ConstructPrompt class by loading the configuration from a YAML file.
        """
        self.config = self.read_config(config_path)
        self.test_dataset_name = self.config.get('test_dataset_name')
        self.test_relation_id = self.config.get('test_relation_id')
        self.test_index_begin = self.config.get('test_index_begin')
        self.test_index_end = self.config.get('test_index_end')
        self.random_seed = self.config.get('random_seed')
        self.lke_type = self.config.get('lke_type')
        self.lke_index = self.config.get('lke_index')
        self.example_num = self.config.get('example_num')
        self.example_seperator = self.config.get('example_seperator')
    
    def read_config(self, path):
        """
        Read the YAML configuration file and return the config dictionary.
        """
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def load_data(self):
        """
        Load and preprocess the test dataset based on specified parameters.

        Returns:
            Tuple of pandas DataFrames: (df_train, df_test)
            - df_train: Sampled training dataset with specified number of examples.
            - df_test: Filtered test dataset based on the provided relation ID and index range.
        """
        # Load dataset from HuggingFace or specified path
        try:
            dataset = load_dataset(self.test_dataset_name)
        except Exception as e:
            logging.error(f"Failed to load dataset: {e}")
            raise

        # Extract train and test splits
        train_data, test_data = dataset['train'], dataset['test']

        # Filter data based on Relation_ID
        try:
            train_data = train_data.filter(lambda example: example['Relation_ID'] == self.test_relation_id)
            test_data = test_data.filter(lambda example: example['Relation_ID'] == self.test_relation_id)
        except KeyError:
            logging.error("Relation_ID key not found in dataset")
            raise

        # Convert to pandas DataFrames
        df_train, df_test = train_data.to_pandas(), test_data.to_pandas()

        # Sample specified number of examples from training data
        if self.example_num:
            df_train = df_train.sample(n=self.example_num, random_state=self.random_seed)

        # Select test data based on index range, if specified
        if self.test_index_begin is not None or self.test_index_end is not None:
            logging.info(f"Test_index_begin: {self.test_index_begin}, Test_index_end: {self.test_index_end}")
            df_test = df_test.iloc[self.test_index_begin:self.test_index_end]

        logging.info(f"Length of the test data: {len(df_test)}")

        return df_train, df_test
    

    def construct_prompt(self):
        """
        Construct prompt strings based on configuration parameters.

        Returns:
            Tuple:
                - all_input_texts: List of fully constructed input texts.
                - base_prompts: List of base prompts for each test subject-object pair.
        """
        # Load and filter data
        df_train, df_test = self.load_data()
        subject_label = 'Subject'
        object_label = 'Object'

        # Handle multiple choices based on data dimensionality
        if len(df_test.shape) == 1:
            multiple_choices = [ast.literal_eval(df_test['Multiple Choices'])]
        else:
            multiple_choices = [ast.literal_eval(choice) for choice in df_test['Multiple Choices'].tolist()]

        # Prepare subject and object lists from training and test data
        train_subject_list = df_train[subject_label].tolist()
        train_object_list = df_train[object_label].tolist()
        
        if len(df_test.shape) == 1:
            test_subject_list = [df_test[subject_label]]
            test_object_list = [df_test[object_label]]
        else:
            test_subject_list = df_test[subject_label].tolist()
            test_object_list = df_test[object_label].tolist()

        all_input_texts = []
        base_prompts = []

        # Generate prompts for each test subject-object pair
        for subject_index, (test_subject, test_object) in enumerate(zip(test_subject_list, test_object_list)):
            inputs = []
            base_prompt = ""
            
            # Construct base prompts based on lke_type
            match self.lke_type:
                case 'zp-lke':
                    base_prompt = ', '.join(
                        f"{train_subject_list[i]}{self.example_seperator}{train_object_list[i]} "
                        for i in range(len(train_subject_list))
                    )
                    base_prompt += f"{test_subject}{self.example_seperator}"
                case 'hgp':
                    template = HGP_TEMPLATES[str(self.test_relation_id)][str(self.prompt_index)]
                    base_prompt = template.replace('{head}', test_subject)
                case 'mmp':
                    template = MMP_TEMPLATES[str(self.test_relation_id)][str(self.prompt_index)]
                    base_prompt = template.replace('{head}', test_subject)
            
            # Prepare multiple choice options, including the correct fact
            if len(df_test.shape) == 1:
                options = multiple_choices[0]
                options.append(df_test['Object'])
            else:
                options = multiple_choices[subject_index]
                options.append(df_test.iloc[subject_index]['Object'])
            
            # Generate full input texts by appending each option to the base prompt
            for option in options:
                inputs.append(f"{base_prompt}{self.example_seperator}{option}")

            all_input_texts.extend(inputs)
            base_prompts.append(base_prompt)
        
        return all_input_texts, base_prompts
    

# Example usage, ONLY for testing
if __name__ == '__main__':
    config_path = '/NS/llm-1/work/qwu/lke_open_code/config/test.yaml'
    prompt_constructor = ConstructPrompt(config_path)
    all_input_texts, base_prompts = prompt_constructor.construct_prompt()
    print(all_input_texts[0])
    print('-----------------')
    print(base_prompts[0])
