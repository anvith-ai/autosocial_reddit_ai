import os
import logging
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def delete_all_files_from_vector_store(vector_store_id):
    """Delete all files from the specified vector store."""
    logging.info(f"Deleting all files from vector store: {vector_store_id}")

    try:
        # List all files in the vector store
        files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)

        # Delete each file
        for file in files.data:
            client.beta.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=file.id
            )
            logging.info(f"Deleted file: {file.id}")

        logging.info("All files deleted from the vector store")
    except Exception as e:
        logging.error(f"Error deleting files from vector store: {str(e)}")
        raise

def create_or_update_vector_store(name, file_paths):
    """Create a new vector store or update an existing one with the provided files."""
    logging.info(f"Creating or updating vector store: {name}")

    try:
        # Check if the vector store already exists
        vector_stores = client.beta.vector_stores.list()
        existing_store = next((vs for vs in vector_stores.data if vs.name == name), None)

        if existing_store:
            vector_store_id = existing_store.id
            logging.info(f"Updating existing vector store: {vector_store_id}")
        else:
            vector_store = client.beta.vector_stores.create(name=name)
            vector_store_id = vector_store.id
            logging.info(f"Created new vector store: {vector_store_id}")

        # Upload files to the vector store
        file_ids = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                continue

            try:
                with open(file_path, "rb") as file:
                    uploaded_file = client.files.create(
                        file=file,
                        purpose="user_data"
                    )
                client.beta.vector_stores.files.create(
                    vector_store_id=vector_store_id,
                    file_id=uploaded_file.id
                )
                file_ids.append(uploaded_file.id)
                logging.info(f"Uploaded file: {file_path}")
            except Exception as e:
                logging.error(f"Error uploading file {file_path}: {str(e)}")

        return vector_store_id
    except Exception as e:
        logging.error(f"Error creating or updating vector store: {str(e)}")
        raise

def clear_vector_store(name):
    """Clear all files from the specified vector store."""
    try:
        # Get the vector store
        vector_stores = client.beta.vector_stores.list()
        existing_store = next((vs for vs in vector_stores.data if vs.name == name), None)

        if existing_store:
            delete_all_files_from_vector_store(existing_store.id)
            logging.info(f"Cleared all files from vector store: {name}")
        else:
            logging.info(f"Vector store '{name}' not found. Nothing to clear.")
    except Exception as e:
        logging.error(f"Error clearing vector store: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Manage vector store for Reddit Context Training")
    parser.add_argument("--clear", action="store_true", help="Clear all files from the vector store")
    parser.add_argument("--upload", action="store_true", help="Upload files to the vector store")
    parser.add_argument("--files", nargs="+", help="List of files to upload")
    args = parser.parse_args()

    vector_store_name = "Reddit Context Training"

    if args.clear:
        clear_vector_store(vector_store_name)

    if args.upload:
        if not args.files:
            print("Please specify files to upload using --files")
            return

        vector_store_id = create_or_update_vector_store(vector_store_name, args.files)
        print(f"Vector store ID: {vector_store_id}")

    if not args.clear and not args.upload:
        print("Please specify either --clear or --upload")

if __name__ == "__main__":
    main()