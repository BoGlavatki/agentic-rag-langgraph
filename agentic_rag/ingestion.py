from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_postgres import PGVector
import os
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv(find_dotenv())

urls = [
    "https://python.langchain.com/docs/integrations/document_loaders/",
    "https://python.langchain.com/docs/integrations/retrievers/",
    "https://python.langchain.com/docs/integrations/vectorstores/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/"
]

embedding_model = AzureOpenAIEmbeddings(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=25)
connection = os.getenv("POSTGRES_CONNECTION_STRING")

doc_splits = text_splitter.split_documents(docs_list)

# pg_vector = PGVector(
#     collection_name="agentic_rag",
#     embeddings=embedding_model,
#     connection=connection,
#     use_jsonb=True,
# )

# pg_vector.add_documents(doc_splits, ids=[str(i) for i in range(len(doc_splits))])

vector_store = PGVector(
    embeddings=embedding_model,
    collection_name="agentic_rag",
    connection=connection,
    use_jsonb=True,
)

retriever = vector_store.as_retriever()

# retriever.get_relevant_documents("What is a retriever?", k=3)

# for i, doc in enumerate(retriever.get_relevant_documents("What is a retriever?", k=3)):
#     print(f"\n\nDocument {i}: {doc}\n\n")

# results = vector_store.similarity_search_with_score("What is a retriever?", k=3)

# for result, score in results:
#     print(f"\n\nScore: {score} Found document: {result} \n\n")
