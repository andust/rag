# RAG

The **RAG** (Retrieval-Augmented Generation) project is a tool that enables the integration of document processing and retrieval functionalities using Qdrant and MongoDB databases.

## TODO

1. **Add Qdrant points to documents sent to MongoDB**
   - Implement functionality to add Qdrant points in MongoDB.

2. **Prevent submission of duplicate documents**
   - Develop a mechanism that detects and prevents the submission of duplicate documents to optimize resources and ensure uniqueness within the database.

3. **Scraping data from websites**
   - Create a web scraping module that allows for the retrieval and analysis of data from websites. This feature should include processing HTML content and extracting relevant information for further analysis or archiving.

4. **Sending PDFs**
   - Implement functionality to allow the submission of documents in PDF format to the database. This feature should handle PDF parsing and conversion to a format suitable for text processing and indexing.

## Installation

To run the project locally, follow these steps:

```bash

# Rename the .env.example file to .env
mv .env.example .env

# Add your OpenAI API key to the .env file
OPENAI_API_KEY=your_openai_api_key

# Start the project using Docker Compose
docker compose up
```

# Adding a sample user locally:

```bash
# Run the following command to build the necessary script:
make build-script

# Access the rag_user_srv container:
docker compose exec rag_user_srv sh

# Execute the script to add sample data:
./scripts/migrate-dev-data
```