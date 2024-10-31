from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

from pydantic import SecretStr
from langchain_qdrant import Qdrant



def format_docs(docs: list[Document]):
    return "\n\n".join(doc.page_content for doc in docs)


def generate_response(
    documents: list[str], openai_api_key: SecretStr, query_text: str
) -> str:
    if documents:
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.create_documents(documents)

        docs = text_splitter.split_documents(texts)

        llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", api_key=openai_api_key.get_secret_value()
        )

        qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            url="http://qdrant:6333",
            collection_name="data_documents",
        )

        retriever = qdrant.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        response: str = rag_chain.invoke(query_text)
        return response

    return ""
