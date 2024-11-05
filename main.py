'''
This is the main function for the reliable knowledge estimation project.
'''
import yaml
import argparse

from latent_knowledge_extractor.LKEs import VllmLKEs
from latent_knowledge_extractor.generation import Generation

def get_new_config(
        config_path,
        model_name,
        test_relation_id,
        lke_type,
        lke_index,
        example_num,
        num_options
):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    config['model_name'] = model_name
    config['test_relation_id'] = test_relation_id
    config['lke_type'] = lke_type
    config['lke_index'] = lke_index
    config['example_num'] = example_num
    config['num_options'] = num_options
    new_config_path = config_path.replace('.yaml', f'_{model_name}_{test_relation_id}_{lke_type}_{lke_index}.yaml')
    with open(new_config_path, 'w') as f:
        yaml.dump(config, f)
    return new_config_path

def main():
    parser = argparse.ArgumentParser(description='Reliable Knowledge Estimation')
    parser.add_argument('--config_path', default='/NS/llm-1/work/qwu/lke_open_code/config/test.yaml', type=str, help='Path to the configuration file')
    parser.add_argument('--model_name', default='llama2-7b', type=str, help='Model name')
    parser.add_argument('--test_relation_id',default=1, type=int, help='Test relation id')
    parser.add_argument('--lke_type', type=str, default='zp-lke',help='LKE type')
    parser.add_argument('--lke_index', type=int, default=0, help='LKE index')
    parser.add_argument('--example_num', type=int, default=50, help='Number of examples')
    parser.add_argument('--num_options', type=int, default=100, help='Number of options')
    args = parser.parse_args()
    new_config_path = get_new_config(
        config_path=args.config_path,
        model_name=args.model_name,
        test_relation_id=args.test_relation_id,
        lke_type=args.lke_type,
        lke_index=args.lke_index,
        example_num=args.example_num,
        num_options=args.num_options
    )
    
    vllm_lkes = VllmLKEs(config_path=new_config_path)
    print('Knowledge estimation start, multiple choice test')
    accuracy, prob_mass_correct_answer = vllm_lkes.get_accuracy()
    print(f'MC Accuracy: {accuracy}, Probability mass of correct answer: {prob_mass_correct_answer}')
    print('Knowledge estimation start, open generation test')
    generation = Generation(config_path=new_config_path)
    outputs, base_prompts, ground_truth = generation.inference()
    acc_gen = generation.save_outputs(outputs, base_prompts, ground_truth)
    print(f'Generation accuracy: {acc_gen}')

if __name__ == '__main__':
    main()