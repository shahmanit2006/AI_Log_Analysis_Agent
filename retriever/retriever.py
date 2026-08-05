import argparse
import json

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import Filter

def load_config(config_file):
    """
    Load project configuration.
    """

    with open(config_file, "r") as file:
        return json.load(file)

# Function Skeleton
def search_logs(config_file):

    config = load_config(config_file)

    qdrant_config = config["qdrant"]

    collection_name = qdrant_config["collection_name"]

    print("Connecting to Qdrant...")

    client = QdrantClient(path="vector_db/qdrant_data")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query = input("Enter your question: ")
    query_embedding = model.encode(query).tolist()

    print("Searching...")

    # "Search this collection using the query vector."
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=5
    ).points # extracts just the list of matching results, making it easier to iterate over.

    print("\nSearch Results")
    print("-" * 50)

    for i, result in enumerate(results, start=1):

        payload = result.payload
        metadata = payload.get("metadata", {})

        print(f"\nResult {i}")
        print(f"Score    : {result.score:.4f}")
        print(f"File     : {metadata.get('file')}")
        print(f"Parser   : {metadata.get('parser')}")
        print(f"Level    : {metadata.get('level')}")
        print(f"Type     : {metadata.get('type')}")
        print(f"Date     : {metadata.get('date')}")
        print(f"Time     : {metadata.get('time')}")
        print(f"Content  : {payload.get('content')}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Log Retriever"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration file"
    )

    args = parser.parse_args()

    search_logs(args.config)