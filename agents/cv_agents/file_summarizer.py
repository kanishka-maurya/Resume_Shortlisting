from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from prompts.extracted_text_prompt_template import Extracted_Prompt_Template
from state_schema import StateType

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

def cv_summary(extracted_text):
    chain = LLMChain(llm=llm, prompt=Extracted_Prompt_Template)
    summarized_text = chain.run(extracted_resume_text=extracted_text)
    return summarized_text

def summarize_node(state: StateType) -> dict:
    """
    Node to summarize extracted CV text using LLM.
    Expects state with key 'text'.
    Returns dict with 'summary'.
    """
    text = state.extracted_text
    summary = cv_summary(text)
    return {"summary": summary}


