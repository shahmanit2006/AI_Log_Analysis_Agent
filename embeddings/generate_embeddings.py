import os
import json
import argparse

# to generate embeddings
from sentence_transformers import SentenceTransformer

# to show progress bar
from tqdm import tqdm

def load_config(config_file):
    """
    Load project configuration.
    """

    with open(config_file, "r") as file:
        return json.load(file)

def generate_embeddings(config_file):

    # Load configuration
    config = load_config(config_file)

    # Knowledge Base file
    kb_file = os.path.join(
        "knowledge_base",
        "knowledge_base.json"
    )

    print("Loading Knowledge Base...")

    # Read knowledge base
    with open(kb_file, "r") as file:

        documents = json.load(file)

    print(f"Total Documents : {len(documents)}")

    print("Loading Embedding Model...")

    # Load embedding model
    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Embedding Model Loaded Successfully.")

    # Store all embeddings
    embeddings = []

    print("Generating Embeddings...")

    # Generate embedding for every document
    for document in tqdm(documents):

        # Extract text from document
        text = document["content"]

        # Generate embedding vector
        vector = model.encode(text)

        # Store embedding
        embeddings.append({

            "id": document["id"],

            "content": text,

            "embedding": vector.tolist(),

            "metadata": document["metadata"]

        })
    
    # Create embeddings folder if it doesn't exist
    os.makedirs("embeddings", exist_ok=True)

    # Output file
    output_file = os.path.join(
        "embeddings",
        "embeddings.json"
    )

    print("\nSaving Embeddings...")

    # Save embeddings
    with open(output_file, "w") as file:

        json.dump(
            embeddings,
            file,
            indent=4
        )

    print("===================================")
    print(f"Total Embeddings : {len(embeddings)}")
    print(f"Embedding Dimension : {len(embeddings[0]['embedding'])}")
    print(f"Saved To : {output_file}")
    print("===================================")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Embedding Generator"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration file"
    )

    args = parser.parse_args()

    generate_embeddings(args.config)