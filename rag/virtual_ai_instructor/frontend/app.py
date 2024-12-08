import streamlit as st
from retrieve_and_generate import retrieve_results, generate_response

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

        search_results = retrieve_results(query, collection_option)
        
        # Display results
        st.subheader("Search Results")
        if search_results:
            for result in search_results:
                st.write(f"**Chunk ID:** {result.id}")
                st.write(f"**Similarity Score:** {result.score:.2f}")
                st.write(f"**Payload:** {result.payload}")
                st.write("---")
                generated_response = generate_response(query, result.payload)
                st.write(f"**Generated response for this search result**: {generated_response}")
        else:
            st.write("No results found. Try a different query.")

# Footer
st.write("Powered by [Qdrant](https://qdrant.tech/) and [Streamlit](https://streamlit.io/)")
