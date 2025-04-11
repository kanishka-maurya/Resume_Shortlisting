# import streamlit as st
# from agents.cv_agents.file_extractor import extract_zip, save_uploaded_file
# from dotenv import load_dotenv
# import os
# # graphs/cv_graph.py
# from langgraph.graph import StateGraph, END
# from agents.cv_agents.file_summarizer import summarize_node
# from agents.cv_agents.file_text_extractor import extract_node
# import json
# import chromadb
# from langgraph.graph import StateGraph
# from state_schema import StateType


# client = chromadb.PersistentClient(path=r"c:\\Users\\kanis\\Resume_Shortlisting")
# collection = client.get_or_create_collection(name="RESUME")

# def save_to_chromaDB(summarized_text):
#     collection.add(
#         documents=[summarized_text],
#         ids=[str(hash(str(summarized_text)))]
#     )

# def save_node(state: StateType) -> dict:
#     """
#     Node to save summarized CV summary to ChromaDB.
#     Expects state with key 'summary'.
#     Returns empty dict.
#     """
#     summary = state.summary or ""
#     if isinstance(summary, dict):
#         summary = json.dumps(summary)
#     save_to_chromaDB(summary)
#     return {}


# # Define graph state structure
# cv_graph_builder = StateGraph(state_schema=StateType)

# cv_graph_builder.add_node("extract_text", extract_node)
# cv_graph_builder.add_node("summarize_cv", summarize_node)
# cv_graph_builder.add_node("save_to_vectorstore", save_node)

# cv_graph_builder.set_entry_point("extract_text")
# cv_graph_builder.add_edge("extract_text", "summarize_cv")
# cv_graph_builder.add_edge("summarize_cv", "save_to_vectorstore")
# cv_graph_builder.add_edge("save_to_vectorstore", END)

# cv_graph = cv_graph_builder.compile()


# def process_directory(directory_path):
#     """
#     Iterate through all files in the given directory and invoke cv_graph on each file.
#     """
#     import os
#     for filename in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, filename)
#         # Only process files with .docx extension
#         if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
#             st.info("actual")
#             with open(file_path, 'rb') as f:
#                 file_bytes = f.read()
#             # Invoke the graph on each file
#             cv_graph.invoke({'file': file_bytes})




# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# st.title("CV Processing Application")

# uploaded_file = st.file_uploader("Upload a ZIP file containing CVs", type="zip")
# if st.button("Saving in vector store"):
#     if not uploaded_file:
#         st.warning("Please upload a Document.")
#     else:
#         if uploaded_file is not None:
#             # Save the uploaded ZIP file
#             zip_path = save_uploaded_file(uploaded_file)
#             if zip_path:
#                 # Extract the ZIP file
#                 extract_dir = extract_zip(zip_path)
#                 st.info(extract_dir)
#                 if extract_dir:
#                     st.info("Processing CVs, please wait...")
#                     # Process the extracted files
#                     #process_directory(extract_dir)
#                     for root, dirs, files in os.walk(extract_dir):
#                        for filename in files:
#                           if filename.lower().endswith('.pdf'):
#                               file_path = os.path.join(root, filename)
#                               st.info(f"Processing file: {file_path}")
#                               with open(file_path, 'rb') as f:
#                                   file_bytes = f.read()
#                 # Ensure cv_graph is defined and accessible in this scope
#                                   cv_graph.invoke({'file': file_bytes})

#                     # for filename in os.listdir(extract_dir):
#                     #        file_path = os.path.join(extract_dir, filename)
#                     #        st.info(file_path)
#                     #        for files in os.path.join()
#                     #        if os.path.isfile(file_path):
#                     #            st.info("actual")
#                     #            with open(file_path, 'rb') as f:
#                     #              file_bytes = f.read()
#                     #              cv_graph.invoke({'file': file_bytes})

#                     st.success("All files have been processed successfully.")



# job_description = st.text_area("Enter Job Description")
# if st.button("Shortlist & Send Emails"):
import streamlit as st
from dotenv import load_dotenv
import os
import json
import sqlite3
import chromadb
from langgraph.graph import StateGraph, END
from agents.cv_agents.file_extractor import extract_zip, save_uploaded_file
from agents.cv_agents.file_summarizer import summarize_node
from agents.cv_agents.file_text_extractor import extract_node
from agents.cv_agents.jd_summarizer import summarize_jd
from agents.cv_agents.extract_candidate_info import extract_info_from_summary
from state_schema import StateType

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Setup ChromaDB
client = chromadb.PersistentClient(path=r"c:\\Users\\kanis\\Resume_Shortlisting")
collection = client.get_or_create_collection(name="RESUME")

# Save summary to ChromaDB
def save_to_chromaDB(summarized_text):
    collection.add(
        documents=[summarized_text],
        ids=[str(hash(str(summarized_text)))]
    )

def save_node(state: StateType) -> dict:
    summary = state.summary or ""
    if isinstance(summary, dict):
        summary = json.dumps(summary)
    save_to_chromaDB(summary)
    return {}

# Graph building
cv_graph_builder = StateGraph(state_schema=StateType)
cv_graph_builder.add_node("extract_text", extract_node)
cv_graph_builder.add_node("summarize_cv", summarize_node)
cv_graph_builder.add_node("save_to_vectorstore", save_node)
cv_graph_builder.set_entry_point("extract_text")
cv_graph_builder.add_edge("extract_text", "summarize_cv")
cv_graph_builder.add_edge("summarize_cv", "save_to_vectorstore")
cv_graph_builder.add_edge("save_to_vectorstore", END)
cv_graph = cv_graph_builder.compile()

# Streamlit UI
st.title("CV Processing and Shortlisting App")

uploaded_file = st.file_uploader("Upload a ZIP file containing CVs", type="zip")
if st.button("Save Resumes to Vector Store"):
    if not uploaded_file:
        st.warning("Please upload a ZIP file.")
    else:
        zip_path = save_uploaded_file(uploaded_file)
        if zip_path:
            extract_dir = extract_zip(zip_path)
            st.info(f"Extracted to: {extract_dir}")
            if extract_dir:
                st.info("Processing CVs...")
                for root, dirs, files in os.walk(extract_dir):
                    for filename in files:
                        if filename.lower().endswith('.pdf'):
                            file_path = os.path.join(root, filename)
                            st.info(f"Processing: {filename}")
                            with open(file_path, 'rb') as f:
                                file_bytes = f.read()
                                cv_graph.invoke({'file': file_bytes})
                st.success("All resumes saved to vector store successfully!")

# Shortlisting resumes
job_description = st.text_area("Enter Job Description")

def save_to_sqlite3(data, db_path="candidate.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            full_name TEXT,
            email TEXT,
            techstack TEXT,
            experience TEXT,
            skills TEXT
        )
    ''')
    for item in data:
        cursor.execute('''
            INSERT INTO candidates (full_name, email, techstack, experience, skills)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            item.get("full_name", ""),
            item.get("email", ""),
            item.get("techstack", ""),
            item.get("experience", ""),
            item.get("skills", "")
        ))
    conn.commit()
    conn.close()

if st.button("Shortlist & Save to DB") and job_description:
    with st.spinner("Shortlisting resumes..."):
        summarized_jd = summarize_jd(job_description)
        results = collection.query(
            query_texts=[summarized_jd],
            n_results=10
        )
        num_to_select = int(len(results['documents'][0]) * 0.8 + 0.5)
        top_matches = results['documents'][0][:num_to_select]
        candidates_info = []
        for summary in top_matches:
            info = extract_info_from_summary(summary)
            candidates_info.append(info)
        save_to_sqlite3(candidates_info)
        st.success("Top candidates shortlisted and saved to candidate.db!")

# Optional: View saved candidates
if st.checkbox("Show Saved Candidates"):
    conn = sqlite3.connect("candidate.db")
    df = None
    try:
        df = conn.execute("SELECT * FROM candidates").fetchall()
    except:
        st.warning("No data found in database.")
    if df:
        st.write("### Shortlisted Candidates")
        for row in df:
            st.markdown(f"""
            **Name:** {row[0]}  
            **Email:** {row[1]}  
            **Tech Stack:** {row[2]}  
            **Experience:** {row[3]}  
            **Skills:** {row[4]}  
            ---
            """)
    conn.close()
