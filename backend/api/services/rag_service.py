"""
RAG Service using LangChain, ChromaDB, and Tavily for internet search
"""
import os
from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class RAGService:
    """
    RAG Service combining ChromaDB vector store with Tavily internet search.
    """
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

        # Lazy-loaded components
        self._llm = None
        self._embeddings = None
        self._vector_store = None
        self._tools = None
        self._agent_executor = None
        self._prompt = None

    @property
    def llm(self):
        """Lazy load the LLM"""
        if self._llm is None:
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            self._llm = ChatGroq(
                api_key=self.groq_api_key,
                model_name="llama-3.3-70b-versatile",
                temperature=0.7,
            )
        return self._llm

    @property
    def embeddings(self):
        """Lazy load the embeddings model"""
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        return self._embeddings

    @property
    def vector_store(self):
        """Lazy load the vector store"""
        if self._vector_store is None:
            self._vector_store = Chroma(
                collection_name="mzeechakula_knowledge",
                embedding_function=self.embeddings,
                persist_directory="./chroma_db"
            )
        return self._vector_store

    @property
    def tools(self):
        """Lazy load the search tools"""
        if self._tools is None:
            self._tools = []
            if self.tavily_api_key:
                search_tool = TavilySearchResults(
                    api_key=self.tavily_api_key,
                    max_results=3
                )
                self._tools.append(search_tool)
        return self._tools

    @property
    def prompt(self):
        """Get the agent prompt template"""
        if self._prompt is None:
            self._prompt = ChatPromptTemplate.from_messages([
                ("system", """You are MzeeChakula, a nutrition and food expert assistant.

You have access to:
1. A knowledge base about nutrition, foods, and health
2. Internet search capabilities to find current information

When answering questions:
- First check your knowledge base for relevant information
- Use internet search for current events, recent research, or information not in your knowledge base
- Provide accurate, helpful, and culturally relevant nutrition advice
- Always cite your sources when using search results

Be friendly, informative, and focus on practical nutrition guidance."""),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
        return self._prompt

    @property
    def agent_executor(self):
        """Lazy load the agent executor"""
        if self._agent_executor is None and self.tools:
            # Create react agent with langgraph
            self._agent_executor = create_react_agent(
                self.llm,
                self.tools
            )
        return self._agent_executor
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict]] = None):
        """
        Add documents to the vector store.
        
        Args:
            texts: List of text documents to add
            metadatas: Optional list of metadata dicts for each document
        """
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)
    
    async def search_knowledge_base(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search the knowledge base for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]
    
    async def answer_query(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        use_search: bool = True
    ) -> Dict:
        """
        Answer a query using RAG with optional internet search.
        
        Args:
            query: User query
            chat_history: Optional chat history
            use_search: Whether to use internet search
            
        Returns:
            Dict with 'answer' and 'sources'
        """
        # Search knowledge base
        kb_results = await self.search_knowledge_base(query)
        
        # If agent is available and search is enabled, use it
        if use_search and self.tools and self.agent_executor:
            # Build messages for langgraph agent
            messages = [
                SystemMessage(content="""You are MzeeChakula, a nutrition and food expert assistant.
Provide accurate, helpful, and culturally relevant nutrition advice for elderly care in Uganda.""")
            ]

            # Add chat history
            if chat_history:
                for msg in chat_history:
                    if msg.get("role") == "user":
                        messages.append(HumanMessage(content=msg.get("content", "")))
                    elif msg.get("role") == "assistant":
                        messages.append(AIMessage(content=msg.get("content", "")))

            # Add current query
            messages.append(HumanMessage(content=query))

            # Run agent - langgraph returns a state dict with 'messages'
            result = await self.agent_executor.ainvoke({"messages": messages})

            # Extract the last AI message
            last_message = result["messages"][-1].content if result.get("messages") else query

            return {
                "answer": last_message,
                "sources": [
                    {"type": "knowledge_base", "content": doc["content"]}
                    for doc in kb_results
                ]
            }
        else:
            # Fallback: Use knowledge base only
            context = "\n\n".join([doc["content"] for doc in kb_results])
            
            prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
            
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            return {
                "answer": response.content,
                "sources": [
                    {"type": "knowledge_base", "content": doc["content"]} 
                    for doc in kb_results
                ]
            }


# Singleton pattern with lazy loading
_rag_service_instance = None

def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton instance"""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
