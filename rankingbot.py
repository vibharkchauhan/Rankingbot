from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import json
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0)


def generate_score_prompt(prompt, response):
    return [
        SystemMessage(content=(
            "You are a helpful assistant that evaluates text responses. "
            "Score each response from 1–10 on the following criteria:\n"
            "- Relevance\n- Clarity\n- Specificity\n- Balance\n- Actionability\n"
            "Provide output as a valid JSON like this:\n"
            "{ 'relevance': 9, 'clarity': 8, 'specificity': 7, 'balance': 9, 'actionability': 8, 'comment': 'summary' }"
        )),
        HumanMessage(content=f"Prompt: {prompt}\nResponse: {response}")
    ]


def evaluate_response(prompt, response_text):
    messages = generate_score_prompt(prompt, response_text)
    result = llm(messages)
    try:
        return json.loads(result.content)
    except:
        return {"relevance": 0, "clarity": 0, "specificity": 0, "balance": 0, "actionability": 0, "comment": "Error parsing"}


def rank_responses(prompt, responses):
    results = []
    for label, text in responses.items():
        scores = evaluate_response(prompt, text)
        weighted_score = (
            scores["relevance"] * 0.3 +
            scores["clarity"] * 0.2 +
            scores["specificity"] * 0.2 +
            scores["balance"] * 0.2 +
            scores["actionability"] * 0.1
        )
        results.append({
            "id": label,
            "score": round(weighted_score, 2),
            "scores": scores,
            "text": text
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
