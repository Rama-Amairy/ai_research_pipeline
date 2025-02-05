import subprocess
import argparse
import logging
from pipeline import execute_pipeline


def setup_logging():
    logging.basicConfig(
        filename='logs/pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_api():
    """
    Run the Flask API.
    """
    print("Starting Flask API...")
    subprocess.run(['python', 'api.py'])

def run_pipeline():
    """
    Run the full pipeline manually.
    """
    setup_logging()
    logging.info("Running the pipeline manually.")

    # Default example keyword and question (can be changed)
    keyword = input("Enter the keyword to search on Wikipedia: ")
    question = input("Enter the question you want to ask: ")

    result = execute_pipeline(keyword, question)
    print("\nPipeline Execution Completed.")
    print("\nAnswers:")
    print(result)

if __name__ == "__main__":
    # Argument parser to switch between API or manual execution
    parser = argparse.ArgumentParser(description="Run the Q&A pipeline or API.")
    parser.add_argument(
        "--mode",
        choices=["api", "pipeline"],
        default="api",
        help="Choose to run the Flask API or execute the pipeline manually."
    )

    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "pipeline":
        run_pipeline()