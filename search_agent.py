import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_vector_store(file_paths):
        vector_store = client.beta.vector_stores.create(name="Reddit Context Training")

        file_ids = []
        for file_path in file_paths:
                with open(file_path, "rb") as file:
                        uploaded_file = client.files.create(file=file, purpose="assistants")
                        file_ids.append(uploaded_file.id)

        client.beta.vector_stores.file_batches.create_and_poll(
               vector_store_id=vector_store.id,
               file_ids=file_ids 
        )

        return vector_store.id

def search_agent(query, vector_store_id):
        assistant = client.beta.assistants.create(
                name="Search Assistant",
                instructions="You are a search assistant. List the relevant content from the vector store for the given query. Only list the content found.",
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                tool_resources={
                        "file_search": {
                                "vector_store_ids": [vector_store_id]
                        }
                }
        )

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"Find relevant in-context training for this Reddit post: {query}"
        )

        run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == 'completed':
                   break
            
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        relevant_content = ""
        for message in messages.data:
               if message.role == "assistant":
                      relevant_content += message.content[0].text.value + "\n\n"

        # Clean up
        client.beta.assistants.delete(assistant.id)

        return relevant_content.strip()

def run_search_agent(query):
       vector_store_name = "Reddit Context Training"
       vector_stores = client.beta.vector_stores.list()
       vector_store = next((vs for vs in vector_stores.data if vs.name == vector_store_name), None)

       if not vector_store:
              raise ValueError(f"Vector store '{vector_store_name}' not found, Please run load.py first.")
       
       result = search_agent(query, vector_store.id)

       print(f"Relevant information found for query '{query}':")
       print(result)

       return result
        

