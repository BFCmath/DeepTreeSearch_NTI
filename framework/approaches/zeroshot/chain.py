# approaches/zeroshot/chain.py

from operator import itemgetter
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.tools import BaseTool

from .prompts import QueryList, QUERY_GENERATOR_PROMPT, REPORT_GENERATOR_PROMPT

# --- START OF CHANGE ---
# This function is now upgraded to handle the structured output from Tavily.
def _format_search_results(results: list[list[dict]]) -> str:
    """
    Formats the structured search results from Tavily into a single string.
    
    Args:
        results: A list where each element is a list of dictionaries, 
                 with each dictionary representing a search result.
                 Example: [[{'title': ..., 'content': ...}], [{'title': ..., 'content': ...}]]

    Returns:
        A formatted string concatenating all search result content.
    """
    formatted_string = []
    # This counter ensures unique numbering for each search snippet.
    result_counter = 1
    # The input is a list of lists, so we iterate through both.
    for query_results in results:
        for result in query_results:
            # We extract the content from each result dictionary.
            formatted_string.append(
                f"Result {result_counter}:\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"URL: {result.get('url', 'N/A')}\n"
                f"Content: {result.get('content', 'No content available.')}"
            )
            result_counter += 1
    
    return "\n\n---\n\n".join(formatted_string)
# --- END OF CHANGE ---

def get_chain(model: BaseChatModel, search_tool: BaseTool) -> Runnable:
    """
    Constructs and returns the LCEL chain for the zeroshot research approach,
    now with a reliable Pydantic parser for query generation.
    """
    pydantic_parser = PydanticOutputParser(pydantic_object=QueryList)

    generate_queries_chain = (
        RunnablePassthrough.assign(
            format_instructions=lambda _: pydantic_parser.get_format_instructions()
        )
        | QUERY_GENERATOR_PROMPT
        | model
        | pydantic_parser
    ).with_retry(stop_after_attempt=3)

    generate_report_chain = (
        REPORT_GENERATOR_PROMPT
        | model
        | StrOutputParser()
    )

    zeroshot_chain = (
        {
            "queries_object": generate_queries_chain,
            "topic": itemgetter("topic"),
        }
        | RunnablePassthrough.assign(
            search_results=(
                itemgetter("queries_object")
                | RunnableLambda(lambda x: x.queries)
                | search_tool.map()
            )
        )
        | RunnablePassthrough.assign(
            search_results=itemgetter("search_results") | RunnableLambda(_format_search_results)
        )
        | generate_report_chain
    )

    return zeroshot_chain