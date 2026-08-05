import argparse
import json
import ollama
import os
from datetime import datetime   

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient

def load_config(config_file):

    with open(config_file, "r") as file:
        return json.load(file)

def initialize_components(config):

    qdrant_config = config["qdrant"]

    collection_name = qdrant_config["collection_name"]

    llm_config = config["llm"]

    model_name = llm_config["model"]

    print("Connecting to Qdrant...")

    client = QdrantClient(
        path="vector_db/qdrant_data"
    )

    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return client, model, collection_name, model_name


def retrieve_logs(client,model,collection_name,query):

    query_embedding = model.encode(query).tolist()

    print("\nSearching relevant logs...")

    results = client.query_points(collection_name=collection_name,query=query_embedding,limit=5).points

    retrieved_logs=[]

    for result in results:

        payload=result.payload

        metadata=payload.get("metadata",{})

        log=f"""
    File : {metadata.get('file')}
    Level : {metadata.get('level')}
    Type : {metadata.get('type')}
    Content : {payload.get('content')}
    """

        retrieved_logs.append({

            "score":round(result.score,4),

            "content":log
        })

    return retrieved_logs


def build_prompt(query,retrieved_logs):

    context = ""

    for log in retrieved_logs:

        context += (

            f"Similarity Score : {log['score']}\n"

            f"{log['content']}\n\n"

        )

    prompt = f"""
        You are a Senior AI Log Analysis Engineer with expertise in debugging hardware verification, UVM simulation logs, networking, embedded systems, distributed software systems and more.

        IMPORTANT RULES:

        1. Analyze ONLY the retrieved logs.
        2. Never invent information that is not present.
        3. If the retrieved logs are insufficient, clearly mention that.
        4. Support every conclusion using evidence from the logs.
        5. Keep the explanation professional and concise.

        Retrieved Logs:
        {context}

        User Question:
        {query}

        Generate a professional log analysis report in the following format:

        ==================================================

        Executive Summary

        Root Cause Analysis

        Error Severity
        (Low / Medium / High / Critical)

        Supporting Evidence
        (List the relevant log messages)

        Affected Components

        Possible Impact

        Recommended Resolution
        (Numbered troubleshooting steps)

        Confidence Score
        (0-100%)

        ==================================================
        """

    return prompt


def generate_response(prompt, model_name):
    
    print("\nGenerating AI analysis...\n")

    response = ollama.chat(

        model=model_name,

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )

    analysis = response["message"]["content"]

    return analysis


def save_report(query,retrieved_logs,analysis):

    os.makedirs("output_report",exist_ok=True)

    report = {

        "timestamp":

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "question": query,

        "retrieved_logs": retrieved_logs,

        "analysis": analysis

    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = os.path.join("output_report",f"analysis_{timestamp}.json")

    with open(output_file,"w",encoding="utf-8") as file:

        json.dump(report,file,indent=4,ensure_ascii=False)

    print(f"\nAnalysis report saved to: {output_file}")


def run_agent(config_file):

    config = load_config(config_file)

    client, model, collection_name, model_name = initialize_components(config)

    print("\n" + "=" * 70)
    print("        AI LOG ANALYSIS AGENT (RAG Powered)")
    print("=" * 70)
    print("\nType 'exit' anytime to quit.")

    while True:

        query = input("\nAsk your question (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("\nThank you for using AI Log Analysis Agent.")
            break

        retrieved_logs = retrieve_logs(
            client,
            model,
            collection_name,
            query
        )

        prompt = build_prompt(
            query,
            retrieved_logs
        )

        try:

            analysis = generate_response(prompt,model_name)

            print("=" * 70)
            print("AI LOG ANALYSIS")
            print("=" * 70)
            print(analysis)

            save_report(
                query,
                retrieved_logs,
                analysis
            )

        except Exception as e:

            print("\nFailed to generate AI analysis.")

            print(e)

        print("\n" + "-" * 70)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="AI Log Analysis Agent"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration file"
    )

    args = parser.parse_args()

    run_agent(args.config)
