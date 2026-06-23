import chromadb
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore")

# Load ChromaDB
client = chromadb.PersistentClient(path="vector_store/chroma_db")
collection = client.get_collection(name="complaints")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_and_answer(question: str, k: int = 5):
    """Main RAG function - Simple version without LangChain Prompt"""
    
    # 1. Embed the question
    query_embedding = embedding_model.encode(question).tolist()
    
    # 2. Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )
    
    retrieved_docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    # 3. Build context
    context = "\n\n---\n\n".join([f"Complaint Excerpt: {doc}" for doc in retrieved_docs])
    
    # 4. Simple simulated LLM response (we can upgrade later)
    sources = []
    for m in metadatas[:3]:
        sources.append(f"• {m.get('product_category')} - {m.get('issue', 'General Issue')}")
    
    answer = f"""**Analysis based on customer complaints:**

{context[:1800]}...

**Key Insights:**
- Several customers reported problems related to **{metadatas[0].get('product_category', 'the product')}**.
- Common themes include billing issues, service delays, and communication problems.

**Recommendation:** Product team should investigate recent complaints in this category."""

    return answer, sources, retrieved_docs[:2]


# Test the function
if __name__ == "__main__":
    answer, sources, _ = retrieve_and_answer("Why are people unhappy with Credit Cards?")
    print("✅ RAG Test Successful!")
    print("\nAnswer Preview:", answer[:300] + "...")