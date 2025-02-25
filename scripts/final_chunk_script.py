# -*- coding: utf-8 -*-
"""final_chunk_script.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MLiAvyRL8amg2ToVoHYBmpuP_VzSbWS8
"""

#installations
!pip install langchain-community
!pip install transformers
!pip install sentence_transformers
!pip install chromadb
!pip install langchain_experimental
!pip install tiktoken
!pip install sympy==1.12
!pip install protobuf==3.20.3

#imports
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

class ConversationRAG:
    def __init__(self, persist_directory):
        self.persist_directory = persist_directory
        self.hf_embeddings = HuggingFaceEmbeddings()
        self.vectordb_k = 8

    def load_and_get_conversation_documents(self, filename):
        pass

    def persist_documents_in_chroma(self, docs):
        print(f'ConversationRAG: Persisting to :{self.persist_directory}')
        vectordb = Chroma.from_documents(
            documents=docs, embedding=self.hf_embeddings, persist_directory=self.persist_directory
        )
        vectordb.persist()

    def generate_question_chunks(self, questions=[]):
        print(f'ConversationRAG: Generating question chunks for :{questions} \| Reading from {self.persist_directory} \| Using vectordb k={self.vectordb_k}')
        vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=self.hf_embeddings)
        question_chunk_map = {}
        for question in questions:
          search = vectordb.similarity_search(question, k=self.vectordb_k)
          question_chunk_map[question] = search

        return question_chunk_map

    def run_rag_process(self, inputfile_name, questions=[]):
        print(f'ConversationRAG: Running RAG process for :{inputfile_name} \| Reading from {self.persist_directory} \| Using vectordb k={self.vectordb_k}')
        print(f'ConversationRAG: Loading and Getting Conversation Documents')
        docs = self.load_and_get_conversation_documents(inputfile_name)

        print(f'ConversationRAG: Persisting Documents in Chroma')
        self.persist_documents_in_chroma(docs)

        print(f'ConversationRAG: Generating Question Chunks')
        question_chunk_map = self.generate_question_chunks(questions)
        return question_chunk_map

class FixedChunkRAG(ConversationRAG):
    def __init__(self, persist_directory):
        super().__init__(persist_directory)
        self.chunk_size = 0
        self.chunk_overlap = 0
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    def set_chunk_size_and_overlap(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_loaded_pages_from_file(self, filename):
        print(f'FixedChunkRAG: Using TextLoader to load file :{filename}')
        loader = TextLoader(filename)
        pages = loader.load()
        return pages

    def get_text_splitter(self):
        """Needs to be overriden"""
        pass

    def load_and_get_conversation_documents(self, filename):
        print(f'FixedChunkRAG: Loading and getting conversation documents from file :{filename}')
        pages = self.get_loaded_pages_from_file(filename)
        text_split = self.get_text_splitter()

        print(f'FixedChunkRAG: Splitting pages into documents using text splitter')
        return text_split.split_documents(pages)


    def run_rag_process_with_chunk_pairs(self, inputfile_name, questions=[], chunk_overlap_pairs=[()]):

        chunk_size_overlap_map = {}
        for chunk_size, chunk_overlap in chunk_overlap_pairs:

            print(f'FixedChunkRAG: Running RAG process for chunk_size={chunk_size} and chunk_overlap={chunk_overlap}')
            self.set_chunk_size_and_overlap(chunk_size, chunk_overlap)

            chunk_size_overlap_map[(chunk_size, chunk_overlap)] = super().run_rag_process(inputfile_name, questions)
        return chunk_size_overlap_map

class RecursiveChunkRAG(FixedChunkRAG):
    def __init__(self):
        super().__init__('recursive_saved_vdb')

    def get_text_splitter(self):
        return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.tokenizer, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )


class TokenChunkRAG(FixedChunkRAG):
    def __init__(self):
        super().__init__('token_chunk_saved_vdb')

    def get_text_splitter(self):
        return TokenTextSplitter.from_huggingface_tokenizer(
            self.tokenizer, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

class SemanticChunkRAG(ConversationRAG):
    def __init__(self):
        super().__init__('semantic_saved_vdb')
        self.semantic_chunker = SemanticChunker(self.hf_embeddings)

    def load_and_get_conversation_documents(self, filename):
        with open(filename, 'r') as file:
            text = file.read()

        return self.semantic_chunker.create_documents([text])

questions_fbi = ['What is the main legal issue in Case 22-1178 between the FBI and Yonas Fikre?',
            'What argument does Sopan Joshi present to support the claim of mootness?',
            "How does Joshi respond to the Ninth Circuit's view on mootness?",
            "What does Justice Clarence Thomas ask regarding the procedures used to place Fikre on the list?",
            "How does Joshi respond to concerns about procedural challenges in Fikre's case?",
            "What hypothetical scenario does Justice Sonia Sotomayor present to question the declaration’s effectiveness?",
            "How does Joshi respond to Justice Sotomayor's hypothetical about re-listing Fikre for similar activities?",
            "What concern does Justice Samuel Alito raise regarding the mootness of the case?",
            "What is Joshi's main defense regarding the unlikelihood of Fikre's return to the No Fly List?",
            "What clarification does Justice Elena Kagan seek regarding the declaration's commitment?",
            "What does Brett M. Kavanaugh question about Sopan Joshi's argument on recurring threats?"]


questions_usa = ["What is the main legal issue being discussed in this case?",
                 "What is the role of the Bank Merger Act of 1966 in this case?",
                 "What specific argument does Mr. Turner present regarding the court’s review of banking agency determinations?",
                 "How does Justice Brennan question the significance of the terms 'trial de novo' and 'review de novo'?",
                 "What was the primary purpose of the Bank Merger Act according to Donald F. Turner?",
                 "What issue did Abe Fortas raise regarding uniformity in the banking industry?",
                 "What was William J. Brennan, Jr.’s interpretation of the government's stance on agency roles in court?",
                 "What concern did David T. Searls express regarding the burden of proof?",
                 "What was the position of the Department of Justice in the trial courts on the standards to be applied to bank mergers?",
                 "How did the California three-judge court rule regarding the Department of Justice's interpretation of the Bank Merger Act?"]


questions_donald = ["What is the main argument presented by Mr. Mitchell regarding Section 3 of the Fourteenth Amendment?",
                    "How does Mr. Mitchell interpret the term 'officer of the United States' in the Constitution?",
                    "Why does Mr. Mitchell believe the Colorado Supreme Court's decision should be reversed?",
                    "What example does Mr. Mitchell give to argue that states cannot impose additional qualifications for federal office?",
                    "How does Justice Thomas question Mr. Mitchell regarding Section 3’s implementation?",
                    "What is Mr. Mitchell’s stance on the self-execution of Section 3?",
                    "What example does Mr. Mitchell give from history to support his argument?",
                    "What does Justice Sotomayor challenge in Mr. Mitchell’s argument about self-execution?",
                    "What distinction does Mr. Mitchell make between Griffin's Case and other Fourteenth Amendment provisions?",
                    "What does Justice Kagan clarify about Mr. Mitchell’s argument on statutory versus constitutional grounds?"]

model = TokenChunkRAG()
model.set_chunk_size_and_overlap(100,20)

output = model.run_rag_process('/content/DONALD J_ TRUMP, Petitioner, v_ NORMA ANDERSON, ET AL_, Respondents.txt',questions=questions_donald)

model = RecursiveChunkRAG()
model.set_chunk_size_and_overlap(100,20)

output = model.run_rag_process('/content/DONALD J_ TRUMP, Petitioner, v_ NORMA ANDERSON, ET AL_, Respondents.txt',questions=questions_donald)

model = SemanticChunkRAG()
output = model.run_rag_process('/content/DONALD J_ TRUMP, Petitioner, v_ NORMA ANDERSON, ET AL_, Respondents.txt',questions=questions_donald)

import json
def write_to_json(output, file):
  writeObj = {}
  for question in output:
    context = ""
    for documents in output[question]:
      context += documents.page_content
    writeObj[question] = context
  with open(file, 'w') as f:
    json.dump(writeObj, f)

write_to_json(output, 'output_Donald_Semantic_Chunk.json')