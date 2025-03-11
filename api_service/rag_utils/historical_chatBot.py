from langchain_community.llms import Ollama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.vectorstores import Weaviate
from weaviate_utils.initializer import client


class ChatbotRAG:

    def __init__(self, llm_config):

        self.ollama_llm = Ollama(
            base_url=f"{llm_config.ollama_host}:{llm_config.ollama_port}",
            model=f"{llm_config.model_name}"
        )
        self.client = client


    def weaviate_retriever(self):

        vectorStore = Weaviate(client=self.client, index_name="your_weaviate_index", text_key="your_text_key")
        vector_retriever = vectorStore.as_retriever(search_type="similarity",
                                                    search_kwargs={
                                                        "k": 10
                                                    })

        return vector_retriever

    def history_aware_retriever(self):

        contextualize_q_system_prompt = """Given a chat history and the latest user question \
                which might reference context in the chat history, formulate a standalone question \
                which can be understood without the chat history. Do NOT answer the question, \
                just reformulate it if needed and otherwise return it as is."""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        retriever = self.weaviate_retriever()

        history_aware_retriever = create_history_aware_retriever(
            self.ollama_llm, retriever, contextualize_q_prompt
        )

        return history_aware_retriever

    def conversational_chat(self, query):

        qa_system_prompt = """
            You are an advanced Persian AI assistant capable of answering questions based on retrieved news content. 
            Your primary tasks are:
            1. Use the given context to accurately answer the user's question.
            2. Provide clear, concise, and fact-based answers using the provided data.
            3. If the information is insufficient or irrelevant, state that you cannot answer the question.

            Guidelines:
            - Use no more than 20 sentences in your answer.
            - Always include relevant context or source references from the retrieved data when possible.
            - If the user references prior questions, utilize the chat history to provide a coherent response.

            {context}
        """

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # generate answer
        question_answer_chain = create_stuff_documents_chain(self.ollama_llm, qa_prompt)

        store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        history_aware_retriever = self.history_aware_retriever()

        # RAG
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        answer = conversational_rag_chain.invoke(
            {"input": query},
            config={
                "configurable": {"session_id": "abc123"}
            },
        )["answer"]
        return answer


        while True:
            print("inset next query:")
            query_x = input()

            answer = conversational_rag_chain.invoke(
                {"input": query_x},
                config={
                    "configurable": {"session_id": "abc123"}
                },
            )["answer"]

            print(f"query_answer:\n\n{answer}")

