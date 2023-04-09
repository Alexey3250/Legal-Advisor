from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

# load the kays
load_dotenv("keys.env")

# access the keys
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Set environment variables
os.environ["OPENAI_API_KEY"] = openai_api_key

# location of the pdf file/files. 
reader = PdfReader(r'C:\Users\Alex\repos\Legal-Advisor\pdfs\en-legislation.pdf')

# read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text
        
# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 

text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

# Print the second chunk and the total number of chunks to check if the text has been properly split
print("Total number of chunks:", len(texts))
print()

# Print information about the uploaded PDF
print("=== PDF Information ===")
print("File name:", "file.pdf")
print("Number of pages:", len(reader.pages))
print("PDF metadata:")
for key, value in reader.metadata.items():
    print(f"{key}: {value}")
print("======================")


# Download embeddings from OpenAI
# Initialize the OpenAIEmbeddings class, which is responsible for converting texts into embeddings
embeddings = OpenAIEmbeddings()

# Create a FAISS index from the texts using the downloaded embeddings
# The FAISS index allows for efficient similarity search in high dimensional space (e.g., searching for similar text chunks)
docsearch = FAISS.from_texts(texts, embeddings)

# Load a question-answering (QA) chain
# The QA chain is a sequence of models or components that work together to answer questions based on the input text
# The "stuff" chain type could be a specific sequence of models designed for answering questions on a particular domain or dataset
chain = load_qa_chain(OpenAI(), chain_type="stuff")

# Define the query you want to ask
query = "What do I need to do to build a house?"

# Perform a similarity search using the FAISS index to find relevant documents from the 'texts' variable
# This returns a list of documents (text chunks) that are most similar to the input query
docs = docsearch.similarity_search(query)

# Run the question-answering (QA) chain on the relevant documents and the input query
# This will generate an answer to the query based on the information in the 'docs' variable
answer = chain.run(input_documents=docs, question=query)

def divide_into_paragraphs(text, max_length):
    words = text.split()
    paragraphs = []
    current_paragraph = ""

    for word in words:
        if len(current_paragraph) + len(word) + 1 > max_length:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = ""

        current_paragraph += f" {word}"

    if current_paragraph.strip():
        paragraphs.append(current_paragraph.strip())

    return paragraphs

# Divide the answer into paragraphs after around 90 characters
formatted_answer = divide_into_paragraphs(answer, 90)

# Print the query, relevant documents, and the formatted answer
print("=== Query ===")
print(query)
print()

print("=== Relevant Documents ===")
for i, doc in enumerate(docs, start=1):
    print(f"Document {i}:")
    print(doc)
    print()

print("=== Answer ===")
for i, paragraph in enumerate(formatted_answer, start=1):
    print(paragraph)