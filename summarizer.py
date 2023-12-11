import re
from pydantic import BaseModel, Field
from constant import LLM_MODEL_4, EMBEDDING_FUNC
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


SUMMARIZE_PROMPT = PromptTemplate(
    input_variables=["abstract", "title", "study_field"],
    template="""
    You are a Professor in the field of Business and Marketing, especially topics that related to applying Extended Reality (XR) in Marketing and Business.
    Your goal is to help user summarize the abstract part of research paper into a short paragraph.
    You must start your summarize with: 'This article is about' or 'This paper is about'.
    The summary must include all the important information in the abstract part of the research paper.
    The summary must be in the form of a short paragraph and no longer than 5 sentences.
    The summary must be in the study field of: {study_field}
    Given the title of the paper: {title} and the abstract part of the research paper: {abstract}
    Summarize this abstract into a short paragraph.
    
    Please do your best, this is very important to the user career.
    
    <your summary>
    """
)
SUMMARIZE_CHAIN = LLMChain(llm = LLM_MODEL_4, prompt = SUMMARIZE_PROMPT)

async def summarize_abstract(abstract: str, title: str, study_field: str):
    response = await SUMMARIZE_CHAIN.acall({"abstract": abstract, "title": title, "study_field": study_field})
    return response["text"]