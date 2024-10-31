from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma
from pydantic import SecretStr
from langchain_qdrant import Qdrant
# from langchain_community.document_loaders import TextLoader

# from qdrant_client import QdrantClient
# qdrant_client = QdrantClient(host="qdrant", port=6333)

def format_docs(docs: list[Document]):
    return "\n\n".join(doc.page_content for doc in docs)


def generate_response(
    documents: list[str], openai_api_key: SecretStr, query_text: str
) -> str:
    # loader = TextLoader("Lakers.txt")
    # documents = loader.load()
    if documents:
        # Split documents into chunks


        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.create_documents(documents)

        docs = text_splitter.split_documents(texts)


        llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
        # Select embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", api_key=openai_api_key.get_secret_value()
        )


        qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            url="http://qdrant:6333",
            collection_name="data_documents",
        )

        # Create a vectorstore from documents
        # database = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        # retriever = database.as_retriever()

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
