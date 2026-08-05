import os
import json
import argparse

# Import parser function from parser module
from Parser.log_parsing import parse_log_line

def load_config(config_file):
    """
    Load project configuration.
    """

    with open(config_file, "r") as file:
        return json.load(file)


def create_knowledge_base(config_file):

    config = load_config(config_file)

    work_dir = config["work_dir"]

    log_files = config["logs"]

    documents = []
    # Starts document_id from 1
    document_id = 1
    
    # Read each log file
    for file_name in log_files:
        
        # Create complete file path
        file_path = os.path.join(work_dir, file_name)

        print(f"\nReading {file_name}...")

        # Open current log file
        with open(file_path, "r") as file:
            
            # Read one line at a time
            for line in file:
                
                # Parse current log line
                parsed_data = parse_log_line(line)
                # print(parsed_data)

                # Skip unknown logs
                if not parsed_data["matched"]:
                    continue

                # Create one knowledge base document
                document = {

                    "id": document_id,

                    "content": parsed_data.get("message", ""),

                    "metadata": {

                        "date": parsed_data.get("date"),

                        "time": parsed_data.get("time"),

                        "level": parsed_data.get("level"),

                        "type": parsed_data.get("type"),

                        "parser": parsed_data.get("parser"),

                        "file": file_name,

                        "fields": parsed_data.get("fields", {})
                    }
                }

                # Store document
                documents.append(document)

                # Next document ID
                document_id += 1
    
    # Create knowledge_base folder if it doesn't exist
    os.makedirs("knowledge_base", exist_ok=True)

    # Output file path
    output_file = os.path.join(
        "knowledge_base",
        "knowledge_base.json"
    )

    # Save all documents
    with open(output_file, "w") as file:

        json.dump(
            documents,
            file,
            indent=4
        )

    print("\n===================================")
    print(f"Total Documents : {len(documents)}")
    print(f"Knowledge Base Saved : {output_file}")
    print("===================================")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Knowledge Base Generator"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration file"
    )

    args = parser.parse_args()

    create_knowledge_base(args.config)

# To run as argparse script in terminal:

# python -m knowledge_base.create_knowledge_base --config test_config.json
# python -m knowledge_base.create_knowledge_base --config config.json

