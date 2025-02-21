import os
import logging
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    BiasMetric,
    HallucinationMetric,
    GEval
)
from deepeval.metrics.ragas import RagasMetric


class EvaluatorGPT:
    def __init__(self, api_key: str):
        """Initialize the evaluator with an API key."""
        self.api_key = api_key
        self.metrics_quality_response = ["relevancy"]
        self.metrics_rag = ["contextual_relevancy"]

    def get_metric(self, name: str):
        """Return the metric object corresponding to the given name."""
        if name == "relevancy":
            return AnswerRelevancyMetric(threshold=0.7, model="gpt-4o-mini", include_reason=True)
        elif name == "faithfulness":
            return FaithfulnessMetric(threshold=0.7, model="gpt-4o-mini", include_reason=True)
        elif name == 'bias':
            return BiasMetric(threshold=0.5)
        elif name == "contextual_precision":
            return ContextualPrecisionMetric(threshold=0.7, model="gpt-4o-mini", include_reason=True)
        elif name == "contextual_recall":
            return ContextualRecallMetric(threshold=0.7, model="gpt-4o-mini", include_reason=True)
        elif name == "contextual_relevancy":
            return ContextualRelevancyMetric(threshold=0.7, model="gpt-4o-mini", include_reason=True)
        elif name == "ragas":
            return RagasMetric(threshold=0.5, model="gpt-4o-mini")
        elif name == "geval":
            return GEval(
                name="Correctness",
                criteria="Determine whether the actual output is factually correct based on the expected output.",
                evaluation_steps=[
                    "Check whether the facts in 'actual output' contradict any facts in 'expected output'",
                    "Heavily penalize omission of detail",
                    "Vague language or contradicting opinions are OK"
                ],
                model="gpt-4o-mini",
                evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
            )

    def create_test_case(self, input: str, output: str, expected_output=None, rag_output=None):
        """Create a test case object with the given input and output."""
        if rag_output:
            return LLMTestCase(input=input, actual_output=output, expected_output=expected_output, retrieval_context=rag_output)
        return LLMTestCase(input=input, actual_output=output, expected_output=expected_output)

    def evaluate_test_cases(self, test_cases, metric):
        """Evaluate a list of test cases with a given metric."""
        metric.measure(test_cases)
        logging.info(f"Metric: {metric.__class__.__name__} - Score: {metric.score}, Reason: {metric.reason}")
        return metric.score, metric.reason

    def get_data_interaction(self, interaction: dict):
        """Extract the input, output, expected response, and RAG output from the interaction."""
        rag_output = []

        if interaction['framework'] == "cheshirecat":
            input = interaction['question']
            output = interaction['text_response']
            expected_response = interaction.get('expected_response', '')

            full_response_memory = interaction.get('full_response', {}).get('data', {}).get('why', {}).get('memory', {}).get('declarative', [])
            for element in full_response_memory:
                rag_output.append(element.get('page_content', ''))

            return input, output, expected_response, rag_output

        elif interaction['framework'] == "anythingllm":
            input = interaction['question']
            output = interaction['text_response']
            expected_response = interaction.get('expected_response', '')

            full_response_memory = interaction.get('full_response', {}).get('data', {}).get('source', [])
            for element in full_response_memory:
                rag_output.append(element)

            return input, output, expected_response, rag_output

    def evaluate_model(self, data_interaction: list):
        """Evaluate test cases using selected metrics and return the results."""
        if not data_interaction:
            logging.warning("No data interactions found to evaluate.")
            return []

        os.environ["OPENAI_API_KEY"] = self.api_key

        results_eval = []

        for interaction in data_interaction:
            input, output, expected_output, rag_output = self.get_data_interaction(interaction)

            for metric_name in self.metrics_quality_response:
                metric = self.get_metric(metric_name)
                test_case = self.create_test_case(input, output, expected_output)
                score, reason = self.evaluate_test_cases(test_case, metric)
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

            for metric_name in self.metrics_rag:
                metric = self.get_metric(metric_name)
                test_case = self.create_test_case(input, output, expected_output, rag_output)
                score, reason = self.evaluate_test_cases(test_case, metric)
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

        return results_eval
