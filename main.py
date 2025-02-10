import subprocess
import argparse
import logging
import os
import yaml
from tabulate import tabulate
from rich.console import Console
from rich.table import Table

# Import your fixed-stage pipeline
from src.pipeline.pipeline import Pipeline  # pipeline with load->transform->QA

MAIN_DIR = os.path.abspath(os.path.dirname(__file__))

def load_config():
    """
    Load the configuration from the YAML file for the model settings.
    (We do NOT load pipeline stages from config; they are fixed in the code.)
    """
    config_path = os.path.join(MAIN_DIR, "config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

def run_pipeline(config, output_format="plain"):
    """
    1) Instantiate the pipeline with the model info (model_name, model_type, api_key).
    2) Get user input for 'keyword' and 'question'.
    3) Run the pipeline and display results.
    """
    # Retrieve model details from config (just for the model, not pipeline stages)
    model_name = config['qa_stage']['model_name']
    model_type = config['qa_stage']['model_type']
    api_key = config['qa_stage'].get('api_key', None)

    # Instantiate the pipeline with your chosen model
    pipeline = Pipeline(
        model_name=model_name,
        model_type=model_type,
        api_key=api_key
    )

    logging.info("Running the pipeline manually.")

    # Collect user input
    keyword = input("Enter the keyword to search: ")
    question = input("Enter the question you want to ask: ")

    # Execute the pipeline
    result_df = pipeline.run(keyword, question)

    # Display results
    display_results(result_df, output_format)

def display_results(result, output_format="plain"):
    """
    Display the Q&A pipeline results in a chosen format.
    """
    print("\nPipeline Execution Completed.\n")
    if output_format == "tabulate":
        # e.g. fancy grid
        print(tabulate(result[['answer', 'confidence']], headers='keys', tablefmt='fancy_grid'))
    elif output_format=="rich":
        # Create a console for Rich
        console = Console()

        # Create a table with a title
        table = Table(title="Q&A Results")

        # Define columns
        table.add_column("Answer", justify="left", style="cyan", no_wrap=True)
        table.add_column("Confidence", justify="right", style="green")

        # Add rows from the DataFrame
        for _, row in result.iterrows():
            answer_str = str(row.get("answer", "N/A"))
            confidence_str = f"{row.get('confidence', 0.0):.4f}"
            table.add_row(answer_str, confidence_str)

        # Print the table
        console.print(table)
    else:
        print(result[['answer', 'confidence']].to_string(index=False))


def run_api():
    """
    Run the Flask API (or FastAPI, etc.) by calling your 'api.py'.
    """
    print("Starting Flask API...")
    subprocess.run(['python', 'src/api/api.py'])

def main():
    """
    Main entry point to parse arguments and run the pipeline or API.
    """
    config = load_config()

    # Argument parser to switch between API or manual execution
    parser = argparse.ArgumentParser(description="Run the Q&A pipeline or API.")
    parser.add_argument("--mode", choices=["api", "pipeline"], default="pipeline",
                        help="Run Flask API or pipeline.")
    parser.add_argument("--output-format", choices=["plain", "tabulate","rich"], default="plain",
                        help="Output format.")

    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    else:  # "pipeline"
        run_pipeline(config, args.output_format)

if __name__ == "__main__":
    # Set up basic logging to console (you can also configure a file handler in pipeline)
    logging.basicConfig(level=logging.INFO)
    main()
