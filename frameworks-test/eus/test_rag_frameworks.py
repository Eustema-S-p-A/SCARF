import logging
import argparse
import os
import json
import csv
from modules.cheshirecat_api import CheshireCatAPI
from modules.anythingllm_api import AnythingLLMAPI
from modules.evaluator_gpt import EvaluatorGPT


def load_config(config_file: str) -> dict:
    """Load configuration from a JSON file."""
    if not os.path.exists(config_file):
        logging.error(f"Configuration file {config_file} not found.")
        exit(1)

    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file {config_file}.")
        exit(1)


def parse_api_keys(api_key_args: list) -> dict:
    """Parse multiple API key arguments passed as module_name:api_key."""
    api_keys = {}
    for api_key_arg in api_key_args:
        try:
            module_name, api_key = api_key_arg.split(':')
            api_keys[module_name] = api_key
        except ValueError:
            logging.error(f"Invalid API key format: {api_key_arg}. Expected format: module_name:api_key")
            exit(1)
    return api_keys


def get_api_key(api_key_file_path: str) -> str:
    """Retrieve the API key from a file."""
    if os.path.exists(api_key_file_path):
        try:
            with open(api_key_file_path, 'r') as file:
                return file.read().strip()
        except IOError as e:
            logging.error(f"Error reading API key from file {api_key_file_path}: {e}")
            raise
    else:
        logging.error(f"API key non provided as flag and file {api_key_file_path} not found.")
        raise ValueError(f"API key is missing. Provide it as an argument or in the {api_key_file_path} file.")


def save_results_to_csv(results, filename='test_results.csv', results_dir='results'):
    """Save test results to a CSV file inside results_dir directory."""
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, filename)
    fieldnames = ['framework', 'filename', 'file_path', 'question', 'text_response', 'full_response', 'expected_response']
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        logging.info(f"Results successfully saved to {file_path}.")
    except IOError as e:
        logging.error(f"Error saving results to {file_path}: {e}")


def save_results_to_json(results, filename='test_results.json', results_dir='results'):
    """Save test results to a JSON file inside results_dir directory."""
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, filename)
    try:
        with open(file_path, 'w') as file:
            json.dump(results, file, indent=4)
        logging.info(f"Results successfully saved to {file_path}.")
    except IOError as e:
        logging.error(f"Error saving results to {file_path}: {e}")


def run_tests(api_module, framework_name, generic_questions, generic_expected_responses, dataset_folder, dataset_files, file_specific_questions, file_expected_responses):
    """Run the tests for generic questions and file-specific questions."""
    results = []

    # Test generic questions
    for i, question in enumerate(generic_questions):
        response = api_module.send_message(question)
        results.append({
            'framework': framework_name,
            'filename': "generic question",
            'file_path': "N/A",
            'question': question,
            'text_response': response.get('text_response', {}),
            'full_response': response.get('full_response', {}),
            'expected_response': generic_expected_responses[i] if i < len(generic_expected_responses) else 'No expected response available'
        })

    # Test document upload and specific questions
    for filename in dataset_files:
        file_path = os.path.join(dataset_folder, filename)
        upload_result = api_module.upload_document(file_path)

        specific_questions = file_specific_questions.get(filename, [])
        expected_responses = file_expected_responses.get(filename, [])

        for i, question in enumerate(specific_questions):
            response = api_module.send_message(question)
            results.append({
                'framework': framework_name,
                'filename': filename,
                'file_path': file_path,
                'question': question,
                'text_response': response.get('text_response', {}),
                'full_response': response.get('full_response', {}),
                "expected_response": expected_responses[i] if i < len(expected_responses) else 'No expected response available'
            })

    return results


def main():
    parser = argparse.ArgumentParser(description='API Test Runner')
    parser.add_argument('--apikey', type=str, nargs='+', help='API key(s) for authentication in the format module_name:api_key')
    parser.add_argument('--config', type=str, default='./config.json', help='Path to the configuration file')
    parser.add_argument('--api', type=str, choices=['cheshirecat', 'anythingllm', 'all'], default='all', help='Select the API to test')
    parser.add_argument('--username', type=str, help='Username for CheshireCat API', required=False)
    parser.add_argument('--password', type=str, help='Password for CheshireCat API', required=False)
    parser.add_argument('--loglevel', type=str, help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()

    # Determine logging level: flag > env var > default to INFO
    loglevel = args.loglevel or os.getenv('LOGLEVEL', 'INFO').upper()
    logging_level = getattr(logging, loglevel, logging.INFO)
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

    config = load_config(args.config)
    api_keys = parse_api_keys(args.apikey) if args.apikey else {}
    all_results = []

    # CheshireCat API testing
    if args.api in ['cheshirecat', 'all']:
        base_url = config['cheshirecat']['base_url']
        api_key_file_path = config['cheshirecat']['api_key_file_path']
        cheshirecat_api_key = api_keys.get('cheshirecat')
        if not cheshirecat_api_key:
            cheshirecat_api_key = get_api_key(api_key_file_path)
        logging.debug(f"cheshirecat api_key: {cheshirecat_api_key}")
        cheshirecat_username = args.username if args.username else config['cheshirecat']['username']
        cheshirecat_password = args.password if args.password else config['cheshirecat']['password']

        api_module = CheshireCatAPI(base_url=base_url, api_key=cheshirecat_api_key, username=cheshirecat_username, password=cheshirecat_password)

        dataset_folder = config['dataset']['path']
        dataset_files = config['dataset']['file_names']
        generic_questions = config['dataset']['generic_questions']
        generic_expected_responses = config['dataset']['generic_expected_responses']
        file_specific_questions = config['dataset']['file_specific_questions']
        file_expected_responses = config['dataset']['file_expected_responses']

        logging.info("Running tests for CheshireCat API...")
        cheshirecat_results = run_tests(api_module, 'cheshirecat', generic_questions, generic_expected_responses, dataset_folder, dataset_files, file_specific_questions, file_expected_responses)
        all_results.extend(cheshirecat_results)

    # AnythingLLM API testing
    if args.api in ['anythingllm', 'all']:
        base_url = config['anythingllm']['base_url']
        api_key_file_path = config['anythingllm']['api_key_file_path']
        anythingllm_api_key = api_keys.get('anythingllm')
        if not anythingllm_api_key:
            anythingllm_api_key = get_api_key(api_key_file_path)
        workspace_slug = config['anythingllm']['workspace_slug']
        logging.debug(f"anythingllm api_key: {anythingllm_api_key}")
        api_module = AnythingLLMAPI(base_url=base_url, api_key=anythingllm_api_key, workspace_slug=workspace_slug)

        dataset_folder = config['dataset']['path']
        dataset_files = config['dataset']['file_names']
        generic_questions = config['dataset']['generic_questions']
        file_specific_questions = config['dataset']['file_specific_questions']

        logging.info("Running tests for AnythingLLM API...")
        anythingllm_results = run_tests(api_module, 'anythingllm', generic_questions, generic_expected_responses, dataset_folder, dataset_files, file_specific_questions, file_expected_responses)
        all_results.extend(anythingllm_results)

    # Save all results to file
    save_results_to_csv(all_results)
    save_results_to_json(all_results)

    # Evaluator step
    evaluator_api_key_file_path = config['evaluator']['api_key_file_path']
    evaluator_api_key = api_keys.get('evaluator')
    if not evaluator_api_key:
        evaluator_api_key = get_api_key(evaluator_api_key_file_path)
    logging.debug(f"evaluator api_key: {evaluator_api_key}")

    # Import evaluator and evaluate the test results
    evaluator = EvaluatorGPT(api_key=evaluator_api_key)

    # Perform evaluation and get the evaluation results
    evaluation_results = evaluator.evaluate_model(data_interaction=all_results)

    # Save the evaluation results in the calling script
    save_results_to_json(results=evaluation_results, filename='evaluation_results.json')


if __name__ == '__main__':
    main()
