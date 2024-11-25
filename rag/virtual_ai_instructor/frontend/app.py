import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Qdrant setup
QDRANT_HOST = "localhost"  # Replace with your Qdrant instance address
QDRANT_PORT = 6333         # Default port for Qdrant

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Embedding model setup (using SentenceTransformers as an example)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model

# Streamlit UI
st.title("Qdrant Query Interface")
st.write("Type a query below to search the transcript database.")

# User query input
query = st.text_input("Enter your query:", "")

# Sidebar options
st.sidebar.header("Query Options")
collection_option = st.sidebar.selectbox(
    "Select a collection to query:",
    options=["semantic_chunks", "abstractive_summary"],
    index=0,
)

# Search on button click
if st.button("Search") and query:
    with st.spinner("Searching..."):
        # Generate vector for the user query
        query_vector = embedding_model.encode(query).tolist()
        
        # Perform a similarity search in Qdrant
        search_results = qdrant_client.search(
            collection_name=collection_option,
            query_vector=query_vector,
            limit=5,  # Return top 5 results
        )
        
        # Display results
        st.subheader("Search Results")
        if search_results:
            for result in search_results:
                st.write(f"**Chunk ID:** {result.id}")
                st.write(f"**Similarity Score:** {result.score:.2f}")
                st.write(f"**Payload:** {result.payload}")
                st.write("---")
        else:
            st.write("No results found. Try a different query.")

# Footer
st.write("Powered by [Qdrant](https://qdrant.tech/) and [Streamlit](https://streamlit.io/)")
