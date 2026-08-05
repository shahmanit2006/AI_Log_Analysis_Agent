import os
import json
import argparse

# Connection between Qdrant and python
from qdrant_client import QdrantClient

from qdrant_client.models import Distance, VectorParams, PointStruct

def load_config(config_file):
    """
    Load project configuration.
    """

    with open(config_file, "r") as file:
        return json.load(file)

def store_embeddings(config_file):

    # Load configuration
    config = load_config(config_file)

    # Read Qdrant settings
    qdrant_config = config["qdrant"]

    collection_name = qdrant_config["collection_name"]

    embedding_dimension = qdrant_config["embedding_dimension"]

    print("Loading Embeddings...")

    # Path of embeddings file
    embedding_file = os.path.join(
        "embeddings",
        "embeddings.json"
    )

    # Read embeddings
    with open(embedding_file, "r") as file:

        embeddings = json.load(file)

    print(f"Total Embeddings : {len(embeddings)}")

    print("Connecting to Qdrant...")

    # Create a persistent local Qdrant database
    client = QdrantClient(
    path="vector_db/qdrant_data"
    )

    print("Connected Successfully.")

    print("Creating Collection...")

    # Delete old collection if it already exists
    if client.collection_exists(collection_name):

        client.delete_collection(collection_name)

    # Create a new collection
    client.create_collection(

        collection_name=collection_name,

        vectors_config=VectorParams(

            size=embedding_dimension,

            distance=Distance.COSINE
        )
    )

    print("Collection Created Successfully.")

    print("Uploading Embeddings...")

    points = []

    # Convert every embedding into a Qdrant Point
    for document in embeddings:

        point = PointStruct(

            id=document["id"],

            vector=document["embedding"],

            payload={

                "content": document["content"],

                "metadata": document["metadata"]
            }
        )

        points.append(point)

    # Upload all points
    client.upsert(

        collection_name=collection_name,

        points=points
    )

    print("Upload Completed Successfully.")

    collection_info = client.get_collection(collection_name)

    print("====================================")
    print(f"Collection : {collection_name}")
    print(f"Stored Points : {collection_info.points_count}")
    print("====================================")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Qdrant Vector Database Loader"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration file"
    )

    args = parser.parse_args()

    store_embeddings(args.config)