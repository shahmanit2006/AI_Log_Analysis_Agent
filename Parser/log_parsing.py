# ==========================================================
# IMPORTS
# ==========================================================

# Used to read command-line arguments like --config config.json
import argparse

# Used to read and parse the config.json file
import json

# Used to create file paths in an operating system independent way
import os

# Used for pattern matching in log parsing
import re



# ==========================================================
# REGEX PATTERNS
# ==========================================================
# Common log levels supported by all log formats
LOG_LEVELS = r"INFO|WARNING|ERROR|DEBUG|CRITICAL"
LOG_PATTERNS=[]

LOG_PATTERNS = [
    {
        "name": "uvm_info_simple",
        "type": "uvm",
        "pattern": re.compile(
            r'^#\s+'
            r'(?P<level>UVM_(?:INFO|WARNING|ERROR|FATAL))'
            r'\s+@\s+'
            r'(?P<time>\d+)'
            r':\s+'
            r'(?P<component>[^[]+)'
            r'\[(?P<tag>[^\]]+)\]\s*'
            r'(?P<remaining>.*)$'
        )
    },

    {
        "name": "uvm_source",
        "type": "uvm",
        "pattern": re.compile(
            r'^#\s+'
            r'(?P<level>UVM_(?:INFO|WARNING|ERROR|FATAL))'
            r'\s+'
            r'(?P<source>.+?)'
            r'\s+@\s+'
            r'(?P<time>\d+)'
            r':\s+'
            r'(?P<component>[^\[]+)'
            r'\[(?P<tag>[^\]]+)\]\s*'
            r'(?P<remaining>.*)$'
        )
    },



    {
        "name": "uvm_info_path",
        "type": "uvm",
        "pattern": re.compile(
            r'^#\s+'
            r'(?P<level>UVM_(?:INFO|WARNING|ERROR|FATAL))'
            r'\s+'
            r'(?P<source>.+?)'
            r'\s+@\s+'
            r'(?P<time>\d+)'
            r':\s+'
            r'(?P<component>[^[]+)'
            r'\[(?P<tag>[^\]]+)\]\s*'
            r'(?P<remaining>.*)$'
        )
    },

    {
        "name": "loading",
        "type": "loading",
        "pattern": re.compile(
            r'^#\s+Loading\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "start_time",
        "type": "metadata",
        "pattern": re.compile(
            r'^#\s+Start time:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "end_time",
        "type": "metadata",
        "pattern": re.compile(
            r'^#\s+End time:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "elapsed_time",
        "type": "metadata",
        "pattern": re.compile(
            r'^#\s+Elapsed time:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "seed",
        "type": "metadata",
        "pattern": re.compile(
            r'^#\s+Sv_Seed\s*=\s*(?P<remaining>.+)$'
        )
    },

    {
        "name": "run",
        "type": "command",
        "pattern": re.compile(
            r'^#\s+(?P<remaining>run.*)$'
        )
    },

    {
        "name": "vsim",
        "type": "command",
        "pattern": re.compile(
            r'^#\s+(?P<remaining>vsim.*)$'
        )
    },

    {
        "name": "comment",
        "type": "comment",
        "pattern": re.compile(
            r'^#\s*//\s*(?P<remaining>.*)$'
        )
    },

    # {
    #     "name": "separator",
    #     "type": "separator",
    #     "pattern": re.compile(
    #         r'^#\s*-{3,}\s*$'
    #     )
    # },

    {
        "name": "blank",
        "type": "blank",
        "pattern": re.compile(
            r'^#\s*$'
        )
    },

    {
        "name": "release_notes",
        "type": "release_notes",
        "pattern": re.compile(
            r'^#\s+(?P<remaining>(UVM-|IMPORTANT RELEASE NOTES|See http|You are using|with `|Specify \+UVM).*)$'
        )
    },

    {
        "name": "copyright",
        "type": "copyright",
        "pattern": re.compile(
            r'^#\s+\(C\)\s+(?P<remaining>.+)$'
        )   
    },

    {
        "name": "table_header",
        "type": "table",
        "pattern": re.compile(
            r'^#\s+Name\s+Type\s+Size\s+Value.*$'
        )
    },

    {
        "name": "hierarchy_row",
        "type": "hierarchy",
        "pattern": re.compile(
                r'^#\s+(?P<remaining>[A-Za-z0-9_@\-\.\']+\s+.+)$'
        )
    },

    # {
    #     "name": "llp_packet",
    #     "type": "packet",
    #     "pattern": re.compile(
    #         r'^#\s+(?P<remaining>LLP_.*)$'
    #     )
    # },

    # {
    #     "name": "tlp_packet",
    #     "type": "packet",
    #     "pattern": re.compile(
    #         r'^#\s+(?P<remaining>TLP_.*)$'
    #     )
    # },

    {
        "name": "vsim_note",
        "type": "simulator_note",
        "pattern": re.compile(
            r'^#\s+\*\*\s+Note:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "hierarchy_header",
        "type": "hierarchy",
        "pattern": re.compile(
            r'^#\s+Hierarchy:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "vsim_error",
        "type": "simulator_error",
        "pattern": re.compile(
            r'^#\s+\*\*\s+Error:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "time_region",
        "type": "simulator_time",
        "pattern": re.compile(
            r'^#\s+Time:\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "report_header",
        "type": "report",
        "pattern": re.compile(
            r'^#\s+\*\*\s+Report\s+(?P<remaining>.+)$'
        )
    },

    {
        "name": "statistics",
        "type": "statistics",
        "pattern": re.compile(
            r'^#\s+\[(?P<category>.+)\]\s+(?P<count>\d+)\s*$'
        )
    },

    {
        "name": "summary",
        "type": "summary",
        "pattern": re.compile(
            r'^#\s+Errors:\s+(?P<errors>\d+),\s+Warnings:\s+(?P<warnings>\d+)$'
        )
    },

    # {
    #     "name": "equal_separator",
    #     "type": "separator",
    #     "pattern": re.compile(
    #         r'^#\s*[=]{5,}\s*$'
    #     )
    # },

    {
        "name": "separator",
        "type": "separator",
        "pattern": re.compile(
            r'^#\s*[-=*]{5,}\s*$'
        )
    },

    {
        "name": "release_banner",
        "type": "release_notes",
        "pattern": re.compile(
            r'^#\s+\*+\s+IMPORTANT RELEASE NOTES\s+\*+\s*$'
        )
    },

    {
        "name": "uvm_option",
        "type": "release_notes",
        "pattern": re.compile(
            r'^#\s+\(Specify\s+(?P<remaining>.+)\)\s*$'
        )
    },


    {
        "name": "standard_log",
        "type": "application",
        "description": "YYYY-MM-DD HH:MM:SS LEVEL Message",
        "pattern": re.compile(
            rf"^(?P<date>\d{{4}}-\d{{2}}-\d{{2}})\s+"
            rf"(?P<time>\d{{2}}:\d{{2}}:\d{{2}})\s+"
            rf"(?P<level>{LOG_LEVELS})\s+"
            rf"(?P<remaining>.*)$"
        )
    },

    {
        "name": "bracket_log",
        "type": "application",
        "description": "[YYYY-MM-DD HH:MM:SS] LEVEL Message",
        "pattern": re.compile(
            rf"^\[(?P<date>\d{{4}}-\d{{2}}-\d{{2}})\s+"
            rf"(?P<time>\d{{2}}:\d{{2}}:\d{{2}})\]\s+"
            rf"(?P<level>{LOG_LEVELS})\s+"
            rf"(?P<remaining>.*)$"
        )
    },

    {
        "name": "slash_date_log",
        "type": "application",
        "description": "YYYY/MM/DD HH:MM:SS LEVEL Message",
        "pattern": re.compile(
            rf"^(?P<date>\d{{4}}/\d{{2}}/\d{{2}})\s+"
            rf"(?P<time>\d{{2}}:\d{{2}}:\d{{2}})\s+"
            rf"(?P<level>{LOG_LEVELS})\s+"
            rf"(?P<remaining>.*)$"
        )
    },

    {
        "name": "iso8601_log",
        "type": "application",
        "description": "YYYY-MM-DDTHH:MM:SSZ LEVEL Message",
        "pattern": re.compile(
            rf"^(?P<date>\d{{4}}-\d{{2}}-\d{{2}})"
            rf"T"
            rf"(?P<time>\d{{2}}:\d{{2}}:\d{{2}})"
            rf"Z\s+"
            rf"(?P<level>{LOG_LEVELS})\s+"
            rf"(?P<remaining>.*)$"
        )
    },
]





# ==========================================================
# PARSER FUNCTIONS
# ==========================================================

def parse_log_line(line):
    """
    Parse one log entry using available regex patterns.
    """

    for log_pattern in LOG_PATTERNS:

        pattern = log_pattern["pattern"]

        match = pattern.match(line)

        if match:
            parsed_data = match.groupdict() # Extract all named regex matches like (date, time, level, remaining) into a dictionary

            # store message words
            message=[]

            # STORE dynamic key=value fields
            fields={}

            # Split remaining text into individual words if exists, otherwise use an empty string to avoid errors
            words = parsed_data.get("remaining", "").split()

            for word in words:
                if "=" in word: # If the word contains '=', treat it as a key-value pair
                    key, value = word.split("=", 1) # Split only on the first '=' to handle cases where value contains '='
                    fields[key] = value
                else:
                    message.append(word) # Add normal words to the message list
            

            # Convert message list into a single string
            parsed_data["message"] = " ".join(message)

            # Store all extracted key=value fields
            parsed_data["fields"] = fields

            # Remove temporary remaining text if present("If remaining exists, delete it. Otherwise, do nothing."No crash.)
            parsed_data.pop("remaining", None)


            parsed_data["matched"] = True
            parsed_data["type"] = log_pattern["type"]
            parsed_data["parser"] = log_pattern["name"]
            return parsed_data

    return {
        "matched": False,
        "raw_line": line.strip()
    }


# ==========================================================
# ANALYZER FUNCTIONS
# ==========================================================

def update_statistics(stats, parsed_data):

    # Count total logs
    stats["total_logs"] += 1

    # Handle unknown logs
    if not parsed_data["matched"]:
        stats["unknown_logs"] += 1

        stats.setdefault("unknown_lines", []).append(
            parsed_data["raw_line"]
        )
        return

    # Count line types
    line_type = parsed_data.get("type", "unknown")

    stats["line_types"][line_type] = (
        stats["line_types"].get(line_type, 0) + 1
    )

    # Count log levels
    level = parsed_data.get("level")

    if level:
        stats["levels"][level] = (
            stats["levels"].get(level, 0) + 1
        )

    # -------------------------------------------------
    # Process UVM ERROR / FATAL and Simulator Errors
    # -------------------------------------------------

    is_error = (
        (level and ("ERROR" in level or "FATAL" in level))
        or
        line_type == "simulator_error"
    )

    if is_error:

        error_message = parsed_data.get("message", "Unknown Error")

        # Store original error
        stats["error_details"].append({

            "date": parsed_data.get("date"),

            "time": parsed_data.get("time"),

            "message": error_message,

            "fields": parsed_data.get("fields", {})
        })

        # -----------------------------
        # Normalize error type
        # -----------------------------

        error_type = error_message

        # Illegal state bin
        if "Illegal state bin was hit" in error_type:
            error_type = "Illegal State Bin"

        # Packet NOT-FOUND
        elif "NOT-FOUND" in error_type:
            error_type = "Packet NOT-FOUND"

        # Single Bit Error
        elif "SINGLE BIT ERROR" in error_type:
            error_type = "Single Bit Error"

        # Merge both double-bit messages
        elif (
            "DOUBLE BIT ERROR" in error_type
            or
            "Double bit error detected" in error_type
        ):
            error_type = "Double Bit Error"

        # Remove long binary strings
        error_type = re.sub(
            r"[01]{16,}",
            "<DATA>",
            error_type
        )

        # Remove changing numbers
        error_type = re.sub(
            r"\bis\s+\d+\b",
            "is <NUM>",
            error_type
        )

        # Count unique error types
        stats["unique_errors"][error_type] = (
            stats["unique_errors"].get(error_type, 0) + 1
        )



# ==========================================================
# COMMAND LINE ARGUMENTS
# ==========================================================

# Create an argument parser
parser = argparse.ArgumentParser(
    description="Parse multiple log files using a configuration file."
)

# Add configuration file argument(tells --config is valid argument)
parser.add_argument(
    "--config",
    required=True,
    help="Path to the configuration JSON file"
)

# Read command-line arguments
args = parser.parse_args()


# ==========================================================
# LOAD CONFIGURATION
# ==========================================================

with open(args.config, "r") as file:
    config = json.load(file)


# ==========================================================
# READ CONFIGURATION VALUES
# ==========================================================

work_dir = config["work_dir"]
log_files = config["logs"]

# Output folder for summary JSON files
output_dir = "output"

# Create output folder if it does not exist
os.makedirs(output_dir, exist_ok=True)


# ==========================================================
# PROCESS LOG FILES
# ==========================================================

for file_name in log_files:

    # Create full path of log file
    file_path = os.path.join(work_dir, file_name)

    # Initialize statistics dictionary
    stats = {
    "total_logs": 0,
    
    # Dynamic counters
    "levels": {},
    "line_types": {},
    "unknown_logs": 0,
    "error_details": [],
    "unique_errors": {},
    "unknown_lines": []
    }


    print("\n" + "=" * 60)
    print(f"Reading File : {file_name}")
    print("=" * 60)

    # Read log file line by line (Streaming)
    with open(file_path, "r") as file:

        for line in file:

            parsed_data = parse_log_line(line)
            update_statistics(stats, parsed_data)

            # Later:
            # analyze_log(parsed_data)

    print(f"Total Logs : {stats['total_logs']}")
    print(f"Unknown Logs : {stats['unknown_logs']}")

    print("\nLog Levels")
    print("\nUnique Errors")
    print("-" * 30)

    print("Total Unique Errors :", len(stats["unique_errors"]))

    for level, count in stats["levels"].items():
        print(f"{level} : {count}")

    print("\nLine Types")
    print("-" * 30)

    for line_type, count in stats["line_types"].items():
        print(f"{line_type} : {count}")

    print("=" * 60)

    unique_error_list = []

    for message, count in stats["unique_errors"].items():
        unique_error_list.append({
            "message": message,
            "count": count
        })
    
    # Create summary report for current log file
    summary = {
        "file_name": file_name,
        #"processed_file": file_path,
        "generated_by": "Log Parser Engine",
        "statistics": {**stats,"unique_errors": unique_error_list}
        }

    # Save summary statistics to a JSON file
    summary_file = file_name.replace(".log", "_summary.json")
    summary_path = os.path.join(output_dir, summary_file)

    with open(summary_path, "w") as file:
        json.dump(summary, file, indent=4)

    print(f"Summary saved to: {summary_path}")
    print("=" * 60)