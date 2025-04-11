# graphs/cv_graph.py
from langgraph.graph import StateGraph, END
from agents.cv_agents.file_summarizer import summarize_node
from agents.cv_agents.file_text_extractor import extract_node
import json
import chromadb
from langgraph.graph import StateGraph
from state_schema import StateType


client = chromadb.PersistentClient(path=r"c:\\Users\\kanis\\Resume_Shortlisting")
collection = client.get_or_create_collection(name="RESUME")

def save_to_chromaDB(summarized_text):
    collection.add(
        documents=[summarized_text],
        ids=[str(hash(str(summarized_text)))]
    )

def save_node(state: StateType) -> dict:
    """
    Node to save summarized CV summary to ChromaDB.
    Expects state with key 'summary'.
    Returns empty dict.
    """
    summary = state.summary or ""
    if isinstance(summary, dict):
        summary = json.dumps(summary)
    save_to_chromaDB(summary)
    return {}


# Define graph state structure
cv_graph_builder = StateGraph(state_schema=StateType)

cv_graph_builder.add_node("extract_text", extract_node)
cv_graph_builder.add_node("summarize_cv", summarize_node)
cv_graph_builder.add_node("save_to_vectorstore", save_node)

cv_graph_builder.set_entry_point("extract_text")
cv_graph_builder.add_edge("extract_text", "summarize_cv")
cv_graph_builder.add_edge("summarize_cv", "save_to_vectorstore")
cv_graph_builder.add_edge("save_to_vectorstore", END)

cv_graph = cv_graph_builder.compile()


def process_directory(directory_path):
    """
    Iterate through all files in the given directory and invoke cv_graph on each file.
    """
    import os
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Only process files with .docx extension
        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            print("yess")
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            # Invoke the graph on each file
            cv_graph.invoke({'file': file_bytes})





