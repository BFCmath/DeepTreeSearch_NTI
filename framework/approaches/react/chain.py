# approaches/react/chain.py

from typing import List, TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
# --- CHANGE: Removed the failing import and only import necessary message types ---
from langchain_core.messages import AIMessage, HumanMessage
# --- END CHANGE ---
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.tools import BaseTool

from .prompts import REACT_PROMPT, REPORT_GENERATOR_PROMPT

ACTION_REGEX = r"Action: (.*)\nAction Input: (.*)"

class ReActState(TypedDict):
    """Represents the state of our ReAct agent."""
    question: str
    scratchpad: Annotated[list, add_messages]
    iterations: int
    article: Optional[str]

def get_chain(model: BaseChatModel, search_tool: BaseTool) -> Runnable:
    """
    Constructs and returns the LangGraph runnable for the ReAct research approach,
    including a final report generation step.
    """
    MAX_ITERATIONS = 10

    # --- CHANGE: Added a self-contained helper function to format messages ---
    def _format_messages(messages: list) -> str:
        """Joins the content of messages into a single string."""
        return "\n".join([msg.content for msg in messages])
    # --- END CHANGE ---

    def run_agent(state: ReActState):
        # --- CHANGE: Use the new helper function ---
        formatted_scratchpad = _format_messages(state["scratchpad"])
        prompt = REACT_PROMPT.invoke(
            {"question": state["question"], "scratchpad": formatted_scratchpad}
        )
        # --- END CHANGE ---
        response = model.invoke(prompt)
        return {"scratchpad": [response], "iterations": state["iterations"] + 1}

    def run_tool(state: ReActState):
        last_message_content = state["scratchpad"][-1].content
        action_match = __import__("re").search(ACTION_REGEX, last_message_content, __import__("re").DOTALL)
        if not action_match:
            raise ValueError("The model did not produce a valid action.")
        action, action_input = action_match.group(1).strip(), action_match.group(2).strip()
        if action == "Search":
            result = search_tool.invoke(action_input)
            return {"scratchpad": [HumanMessage(content=f"Observation: {result}")]}
        return {"scratchpad": [HumanMessage(content="Observation: Invalid action specified.")]}

    def should_continue(state: ReActState):
        last_message_content = state["scratchpad"][-1].content
        if "Action: Finish" in last_message_content or state["iterations"] >= MAX_ITERATIONS:
            return "end"
        return "continue"
    
    def generate_report_node(state: ReActState):
        print("--- Synthesizing final report ---")
        # --- CHANGE: Use the new helper function ---
        research_summary = _format_messages(state["scratchpad"])
        # --- END CHANGE ---
        report_generator_chain = REPORT_GENERATOR_PROMPT | model | StrOutputParser()
        final_report = report_generator_chain.invoke({
            "question": state["question"],
            "research_summary": research_summary,
        })
        return {"article": final_report}
    
    def structure_final_output(final_state: ReActState):
        search_count = sum(1 for msg in final_state["scratchpad"] if isinstance(msg, AIMessage) and "Action: Search" in msg.content)
        return {
            "article": final_state.get("article", "No report generated."),
            "metadata": {"search_count": search_count},
        }

    graph = StateGraph(ReActState)
    graph.add_node("agent", run_agent)
    graph.add_node("tool", run_tool)
    graph.add_node("generate_report", generate_report_node)

    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {"continue": "tool", "end": "generate_report"},
    )
    graph.add_edge("tool", "agent")
    graph.add_edge("generate_report", END)

    runnable_graph = graph.compile()
    
    final_chain = RunnableLambda(
        lambda x: {"question": x["topic"], "scratchpad": [], "iterations": 0}
    ) | runnable_graph | RunnableLambda(structure_final_output)

    return final_chain