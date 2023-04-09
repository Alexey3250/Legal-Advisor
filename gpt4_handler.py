from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os


def setup_gpt4_handler():
    # Load the keys.env file
    load_dotenv("keys.env")

    # Access the keys
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # Set environment variables
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Read data from the file and put them into a variable called raw_text
    reader = PdfReader(r'C:\Users\Alex\repos\Legal-Advisor\pdfs\en-legislation.pdf')
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    # Initialize the OpenAIEmbeddings class
    embeddings = OpenAIEmbeddings()

    # Create a FAISS index from the texts
    docsearch = FAISS.from_texts(texts, embeddings)

    # Load a question-answering (QA) chain
    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    return docsearch, chain


def get_gpt4_response(query, docsearch, chain):
    # Perform a similarity search
    docs = docsearch.similarity_search(query)

    # Run the question-answering (QA) chain
    answer = chain.run(input_documents=docs, question=query)

    return answer
