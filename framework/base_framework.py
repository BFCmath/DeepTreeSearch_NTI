# base_framework.py

import importlib
from langchain_core.language_models.chat_models import BaseChatModel

def run_pipeline(topic: str, model: BaseChatModel, approach_name: str) -> str:
    """
    The main interface to run a deep research pipeline.

    It dynamically loads and executes the specified research approach.

    Args:
        topic (str): The research topic provided by the user.
        model (BaseChatModel): An initialized LangChain chat model (e.g., ChatGoogleGenerativeAI).
        approach_name (str): The name of the approach folder (e.g., 'zeroshot').

    Returns:
        str: The final research report as a string.
        
    Raises:
        ValueError: If the specified approach_name does not correspond to a valid approach module.
    """
    print(f"🚀 Starting pipeline for topic: '{topic}' using '{approach_name}' approach...")

    try:
        # Dynamically import the `chain.py` module from the specified approach folder
        approach_module = importlib.import_module(f"approaches.{approach_name}.chain")
        print(f"✅ Successfully loaded '{approach_name}' approach module.")
    except ModuleNotFoundError:
        raise ValueError(
            f"Approach '{approach_name}' not found or does not contain a 'chain.py' file."
        )

    # Get the chain constructor function from the loaded module
    get_chain_func = getattr(approach_module, "get_chain")

    # Get the unified search tool
    from tools.search import get_search_tool
    search_tool = get_search_tool()
    print("🔧 Search tool initialized.")

    # Construct the specific research chain by passing the model and tool
    research_chain = get_chain_func(model, search_tool)
    print("🔗 Research chain constructed.")

    # Execute the chain with the user's topic
    print("⏳ Invoking the research chain... please wait.")
    result = research_chain.invoke({"topic": topic})
    print("✅ Pipeline finished successfully.")

    return result