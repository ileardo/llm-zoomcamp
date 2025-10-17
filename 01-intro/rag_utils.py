"""
RAG (Retrieval-Augmented Generation) utilities for building and querying a knowledge base.

This module provides functions for loading documents, indexing them for search,
performing searches, building prompts, and interacting with language models.
"""

from typing import List, Dict, Optional, Any
import minsearch
import json


def load_and_indexknowledge_base(file_path: str) -> minsearch.Index:
    """
    Load a knowledge base from a JSON file and create a searchable index.

    This function reads a JSON file containing course documents, flattens the structure
    by adding course information to each document, and creates a minsearch Index
    for efficient searching.

    Args:
        file_path: Path to the JSON file containing the knowledge base.
                  Expected format: list of dicts with 'course' and 'documents' keys.

    Returns:
        A fitted minsearch.Index object ready for searching.

    Example:
        >>> index = load_and_indexknowledge_base('documents.json')
        >>> results = index.search('How do I install Python?')
    """
    with open(file_path, 'rt') as f_in:
        docs_raw = json.load(f_in)

    knowledge_base = []
    for course_dict in docs_raw:
        for doc in course_dict['documents']:
            doc['course'] = course_dict['course']
            knowledge_base.append(doc)

    index = minsearch.Index(
        text_fields=['question', 'text', 'section'],
        keyword_fields=['course']
    )
    index.fit(knowledge_base)
    return index


def search(
    index: minsearch.Index,
    query: str,
    boost_dict: Optional[Dict[str, float]] = None,
    filter_dict: Optional[Dict[str, Any]] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the knowledge base index for documents matching the query.

    Args:
        index: A fitted minsearch.Index object to search.
        query: The search query string.
        boost_dict: Optional dictionary to boost specific fields during search.
                   Example: {'question': 3.0, 'section': 0.5}
        filter_dict: Optional dictionary to filter results by specific field values.
                    Example: {'course': 'data-engineering-zoomcamp'}
        top_k: Number of top results to return. Default is 5.

    Returns:
        List of document dictionaries matching the search query,
        ordered by relevance score.

    Example:
        >>> results = search(index, 'python installation', top_k=3)
        >>> for doc in results:
        ...     print(doc['question'])
    """
    results = index.search(
        query,
        boost_dict=boost_dict,
        filter_dict=filter_dict,
        num_results=top_k
    )
    return results


def build_prompt(query: str, search_results: List[Dict[str, Any]]) -> str:
    """
    Build a prompt for the LLM using the search results as context.

    Constructs a prompt that instructs the LLM to act as a course teaching assistant
    and answer the question based only on the provided context from the FAQ database.

    Args:
        query: The user's question.
        search_results: List of document dictionaries from the search function.
                       Each document should have 'section', 'question', and 'text' keys.

    Returns:
        A formatted prompt string ready to be sent to the LLM.

    Example:
        >>> prompt = build_prompt('How do I install Python?', search_results)
        >>> answer = llm(client, prompt)
    """
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    context = ""

    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(client: Any, prompt: str, model_name: str = 'gpt-4o') -> str:
    """
    Send a prompt to a language model and return the response.

    Uses the OpenAI chat completions API to generate a response based on the prompt.

    Args:
        client: An OpenAI client instance (e.g., from openai.OpenAI()).
        prompt: The prompt string to send to the model.
        model_name: The name of the OpenAI model to use. Default is 'gpt-4o'.

    Returns:
        The text content of the model's response.

    Example:
        >>> from openai import OpenAI
        >>> client = OpenAI()
        >>> response = llm(client, 'Explain Python decorators')
        >>> print(response)
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

    