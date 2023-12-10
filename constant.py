from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.schema import StrOutputParser
import streamlit as st


LLM_MODEL_4 = ChatOpenAI(
    model_name="gpt-4-1106-preview",
    temperature=0.2,
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    # frequency_penalty=0.5,
    # presence_penalty=0.5,
    callbacks=[StreamingStdOutCallbackHandler()],
    streaming=True,
)

EMBEDDING_FUNC = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model="text-embedding-ada-002",
)

