from dotenv import load_dotenv
from phi.assistant import Assistant
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector2

load_dotenv()

def ask_question(prompt):
    # load pdfs
    pdf_knowledge_base = PDFKnowledgeBase(
        path="files",
        # Table name: ai.pdf_documents
        vector_db=PgVector2(
            collection="files",
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        ),
        reader=PDFReader(chunk=True),
    )
    
    pdf_knowledge_base.load(recreate=False)
    
    assistant = Assistant(
        knowledge_base=pdf_knowledge_base,
        # The add_references_to_prompt will update the prompt with references from the knowledge base.
        add_references_to_prompt=True,
        debug_mode=True,
    )
    
    result = assistant.run(prompt, stream=False)
    return result;
    
def update_knowledge_base():
    pdf_knowledge_base = PDFKnowledgeBase(
        path="files",
        vector_db=PgVector2(
            collection="files",
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        ),
        reader=PDFReader(chunk=True),
    )
    
    pdf_knowledge_base.load(recreate=True)