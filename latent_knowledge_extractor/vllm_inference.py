import time
import logging
import json
import yaml
from vllm import LLM, SamplingParams

class VllmInference:
    def __init__(self, config_path):
        """
        Initialize the VllmInference class by loading the model from the model path.
        """
        #get model loading parameters
        self.config = self.read_config(config_path)
        self.model_path = self.config.get('model_path')
        self.tensor_parallel_size = self.config.get('tensor_parallel_size')
        self.trust_trmote_code = self.config.get('trust_remote_code')
        self.gpu_memory_utilization = self.config.get('gpu_memory_utilization')
        self.max_model_len = self.config.get('max_model_len')
        self.prompt_logprobs = self.config.get('prompt_logprobs')
        self.max_new_tokens = self.config.get('max_new_tokens')
        self.temperature = self.config.get('temperature')

    def read_config(self, path):
        """
        Read the YAML configuration file and return the config dictionary.
        """
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    

    def load_model(self):
        if self.prompt_logprobs is None:
            logging.info('Prompt logprobs is None')
            sampling_params = SamplingParams(
            max_tokens = self.max_new_tokens,
            temperature = self.temperature,
            repetition_penalty = self.repetition_penalty,
            top_k = self.top_k,
            top_p = self.top_p,
        )
        else:
            sampling_params = SamplingParams(
                max_tokens = self.max_new_tokens,
                prompt_logprobs = self.prompt_logprobs,
                temperature=0
            )
        logging.info(f'Sampling parameters: {sampling_params}')
        loading_start_time = time.time()
        try:
            llm = LLM(
                model = self.model_path,
                tensor_parallel_size = self.tensor_parallel_size,
                gpu_memory_utilization = self.gpu_memory_utilization,
                trust_remote_code = self.trust_trmote_code,
                max_model_len = self.max_model_len,
            )
        except Exception as e:
            logging.error(f'Error loading model: {e}')
            logging.warning('Failed to load model. Please check the model path and the model loading parameters.\
             if you face OOM error for models with long context windows, like llama3 (8k) and mistral v2 (32k) you may need to try: \n\
                    # 1. you may need to decrease the max_model_len parameter to a smaller value, like 4096 \n\
                    # 2. you may need to decrease the gpu_memory_utilization parameter to a smaller value, like 0.5 \n\
                    # 3. you may need to use more GPUs to load the model (also increase the tensor_parallel_size parameter)\n\
                    # you can also check the discussion here if the above solutions do not work: https://github.com/vllm-project/vllm/issues/188\n ')
            exit()
            
        logging.info('Model loaded.')
        logging.info(f'Loading time: {time.time() - loading_start_time}')
        return llm, sampling_params

    def inference(self, input_data, sampling_params, model):
        """
        Inference the model with the input data.
        """
        inference_start_time = time.time()
        output = model.generate(
            input_data,
            sampling_params = sampling_params,
        )
        logging.info(f'Finish inference')
        logging.info(f'Inference time: {time.time() - inference_start_time}')
        return output
    
    
#only for test
if __name__ == '__main__':
    config_path = '/NS/llm-1/work/qwu/lke_open_code/config/test.yaml'
    inference = VllmInference(config_path)
    model, sampling_params = inference.load_model()
    def read_json_test(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        prompt = data["prompts"][0]["content"]
        return prompt
    prompt = 'Hello!'
    input_data = prompt
    outputs = inference.inference(input_data, sampling_params, model)
    for output in outputs:
        print(output.outputs[0].text)
