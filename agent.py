from __future__ import annotations

from langchain.schema import Document as LangChainDocument
from langchain.agents import AgentType, initialize_agent, AgentExecutor
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
#from langchain.tools.tavily_search import TavilySearchResults
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchResults
#from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from vector_storage import ZillizVectorDatabase
from langchain.prompts import PromptTemplate

from constant import LLM_MODEL_4

AGENT_PREFIX_PROMPT = PromptTemplate(
    
)


class ResearchAssistant:
    agent: AgentExecutor | None = None
    llm_model: ChatOpenAI = LLM_MODEL_4
    greeting_message: str = ""
    conversational_memory: ConversationBufferWindowMemory
    vector_db: ZillizVectorDatabase
    
    def __init__(
        self,
        name: str = "Huy Mo",
        using_ddg: bool = True,
        using_tavily: bool = True,
    ):
        self.assistant_name = name
        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            return_messages = True,
            output_key="output"
        )
        if using_ddg:
            ddg_search = DuckDuckGoSearchAPIWrapper(max_results = 100)
            self.ddg_tool = DuckDuckGoSearchResults(api_wrapper=ddg_search, max_results = 100)
        
        self.vector_db = ZillizVectorDatabase()
        self.tool_list = [
            Tool(
                name = "DuckDuckGo Search",
                func=self.ddg_tool.run,
                description="Search the web for relevant results.",
            )
        ]
        self.agent = initialize_agent(
            agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            name=name,
            llm=self.llm_model,
            conversational_memory=self.conversational_memory,
            tool_list=self.tool_list,
            vector_db=self.vector_db,
            tools = self.tool_list,
            
        )
    
    def query(self, query):
        self.agent.run(query)


bot = ResearchAssistant()
bot.query("Give me a bibliometrics with around 20 research papers, articles, journals or publication that related to the topic: Unleashing the Metaverse: Extended Reality (XR) in Marketing. Return the result in a table")