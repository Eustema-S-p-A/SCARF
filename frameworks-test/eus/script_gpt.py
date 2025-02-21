from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric, BiasMetric
from deepeval import evaluate
from deepeval.test_case import LLMTestCaseParams
from deepeval.metrics.ragas import RagasMetric
from deepeval.metrics import HallucinationMetric
import os
from deepeval.metrics import GEval
import argparse
import os
import json

parser = argparse.ArgumentParser(description='Evaluate a language model with RAG on a set of test cases.')
parser.add_argument('--path_data', type=str, default="./results/test_results.json", help='Path to the data file containing the responses to evaluate.')
parser.add_argument('--path_output', type=str, default="./results/output_results",help='Path to the output file to save the results.')
parser.add_argument('--api_key', default="", type=str, help='API key for GPT model.')
args = parser.parse_args()



def metrics(name):
    """
    Return the metric object corresponding to the given name.
    """
    if name=="relevancy":
        metric = AnswerRelevancyMetric(
                threshold=0.7,
                model="gpt-4o-mini",
                include_reason=True)
    elif name=="faithfulness":
        metric = FaithfulnessMetric(
            threshold=0.7,
            model="gpt-4o-mini",
            include_reason=True)
    elif name=='bias':
        metric = BiasMetric(threshold=0.5)
    elif name=="contextual_precision":
        metric = ContextualPrecisionMetric(
            threshold=0.7,
            model="gpt-4o-mini",
            include_reason=True)
    elif name=="contextual_recall":
        metric = ContextualRecallMetric(
            threshold=0.7,
            model="gpt-4o-mini",
            include_reason=True)
    elif name=="contextual_relevancy":
        metric = ContextualRelevancyMetric(
            threshold=0.7,
            model="gpt-4o-mini",
            include_reason=True)
    elif name=="ragas":
        metric = RagasMetric(threshold=0.5, model="gpt-4o-mini")
    elif name=="geval":
        metric = GEval(
        name="Correctness",
        criteria="Determine whether the actual output is factually correct based on the expected output.",
        # NOTE: you can only provide either criteria or evaluation_steps, and not both
        evaluation_steps=[
            "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
            "You should also heavily penalize omission of detail",
            "Vague language, or contradicting OPINIONS, are OK"
        ], model="gpt-4o-mini",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT])

    return metric



def create_test_case(input, output, expected_output=None, rag_output=None):
    """
    Create a test case object with the given input and output.
    """
    if rag_output is not None:
        return LLMTestCase(
            input=input,
            actual_output=output,
            expected_output=expected_output,
            retrieval_context=rag_output)
    else:
        return LLMTestCase(
            input=input,
            actual_output=output,
            )


def evaluate_test_cases(test_cases, metric):
    """
    Evaluate a list of test cases with a given metric.
    """
    metric.measure(test_cases)
    print(metric.score)
    print(metric.reason)
    return metric.score, metric.reason



def save_results_to_json(results, path):
    """
    Save the results to a JSON file.
    """
    with open(path, "w") as f:
        json.dump(results, f, indent=4)


def get_data_interaction(interaction):
    """
    Get the input and output from the interaction.
    """

    rag_ouptut = []
    
    if interaction['framework'] == "cheshirecat":
        input = interaction['question']
        output = interaction['text_response']
        expected_response = interaction['expected_response']

        full_response_memory = interaction['full_response']['data']['why']['memory']['declarative']

        for element in full_response_memory:
            rag_ouptut.append(element['page_content'])
        
        return input, output, expected_response, rag_ouptut
    
    elif interaction['framework'] == "anythingllm":
        input = interaction['question']
        output = interaction['text_response']
        expected_response = interaction['expected_response']
        # verify if is it correct since anythingllm does not response
        full_response_memory = interaction['full_response']['data']['source']

        for element in full_response_memory:
            rag_ouptut.append(element)
        
        return input, output, expected_response, rag_ouptut
    






def main():
    os.environ["OPENAI_API_KEY"]=args.api_key
    # Load the data file
    with open(args.path_data, "r") as f:
        data_interaction = json.load(f)

    results_eval = []
    metrics_quality_response = ["relevancy"] #["relevancy", "bias"]
    metrics_rag = ["contextual_relevancy"] #others [ "faithfulness", "contextual_recall", "contextual_precision", 'ragas', 'geval']
                                
                     
    for i, interaction in enumerate(data_interaction):
        input, output, expected_output, rag_output = get_data_interaction(interaction)
        
        for metric_name in metrics_quality_response:
            
            metric = metrics(metric_name)
            # None rag_output since this metric does not use it
            test_case = create_test_case(input, output, expected_output, rag_output=None)
            score, reason = evaluate_test_cases(test_case, metric)
            results_eval.append({
                "framework": interaction['framework'],
                "filename": interaction['filename'],
                "file_path": interaction['file_path'],
                "question": input,
                "text_response": output,
                "full_response": rag_output,
                "expected_response": expected_output,
                "metric": metric_name,
                "score": score,
                "reason": reason
            })

        for metric_name in metrics_rag:
            metric = metrics(metric_name)
            test_case = create_test_case(input, output, expected_output, rag_output)
            score, reason = evaluate_test_cases(test_case, metric)
            results_eval.append({
                "framework": interaction['framework'],
                "filename": interaction['filename'],
                "file_path": interaction['file_path'],
                "question": input,
                "text_response": output,
                "full_response": rag_output,
                "expected_response": expected_output,
                "metric": metric_name,
                "score": score,
                "reason": reason
            })

    save_results_to_json(results_eval, args.path_output)
        
    



if __name__ == '__main__':
    main()