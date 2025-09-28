# main.py

import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from base_framework import run_pipeline

def main():
    """
    Runs a batch processing pipeline that reads research prompts from a JSONL file,
    executes the research pipeline for each, and saves the results to an output JSONL file.
    """
    # Load environment variables from .env file (for GOOGLE_API_KEY)
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    # --- Configuration ---
    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    # 2. Choose the approach to use
    selected_approach = "zeroshot"

    # 3. Define input and output files
    input_file = "query.jsonl"
    output_dir = "outputs"
    output_file = os.path.join(output_dir, f"{selected_approach}.jsonl")

    # --- File Handling ---
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found.")
        print("Please create it with one JSON object per line, like:")
        print('{"id": 1, "prompt": "Your research topic here"}')
        return

    # --- Batch Processing ---
    print(f"🚀 Starting batch processing from '{input_file}'...")
    print(f"Output will be saved to '{output_file}'.")

    try:
        # Use 'a' for append mode to make the process resumable
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'a', encoding='utf-8') as f_out:
            
            for line in f_in:
                try:
                    # Load the JSON object from the line
                    data = json.loads(line.strip())
                    query_id = data["id"]
                    research_prompt = data["prompt"]

                    print(f"\nProcessing ID: {query_id} | Prompt: '{research_prompt[:50]}...'")

                    # Run the pipeline using the prompt from the file
                    final_report = run_pipeline(
                        topic=research_prompt,
                        model=llm,
                        approach_name=selected_approach
                    )

                    # Create the output record
                    output_record = {
                        "id": query_id,
                        "prompt": research_prompt,
                        "article": final_report
                    }

                    # Write the result as a new line in the output file
                    f_out.write(json.dumps(output_record) + '\n')
                    print(f"✅ Successfully processed and saved ID: {query_id}")

                except json.JSONDecodeError:
                    print(f"⚠️ Warning: Skipping malformed line: {line.strip()}")
                except KeyError:
                    print(f"⚠️ Warning: Skipping line with missing 'id' or 'prompt': {line.strip()}")
                except Exception as e:
                    print(f"❌ An unexpected error occurred while processing a line: {e}")

    except Exception as e:
        print(f"❌ A critical error occurred: {e}")

    print("\n🎉 Batch processing complete.")

if __name__ == "__main__":
    main()