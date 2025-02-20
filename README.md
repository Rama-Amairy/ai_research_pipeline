# AI Research Pipeline

A simple, modular **Question Answering (QA)** pipeline that fetches content from Wikipedia, processes it, and uses AI models to generate answers to user questions.

---

## Features

- **Wikipedia Data Fetching**: Retrieve relevant data using keywords.
- **Data Transformation**: Structure the retrieved content into pages.
- **Question Answering**: Use AI models (e.g., HuggingFace or OpenRouter-based models) to answer questions based on the structured content.
- **Flask API**: Serve the pipeline through a RESTful API.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Rama-Amairy/ai_research_pipeline.git
   cd ai_research_pipeline
   ```

2. **Set Up a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Command-Line Mode

Run the pipeline directly in the terminal:

```bash
python main.py --mode=pipeline

you can see the output in diffrent formats, choices=["plain", "tabulate","rich"], default="plain"

python main.py --mode=pipeline --output-format=rich
```

You will be prompted to enter a **keyword** and a **question**. The pipeline will load Wikipedia data, transform it, and generate answers.

### 2. API Mode

Start the Flask API:

```bash
python main.py --mode=api

or
python src/api/api.py
```

Then, you can send POST requests to the API endpoint:

```bash
curl -X POST http://localhost:5000/qa \
     -H "Content-Type: application/json" \
     -d '{"keyword": "Python (programming language)", "question": "Who created Python?"}'
```

---



## Configuration

Update model settings in `config.yaml` if needed:

```yaml

# Model handler configurations
qa_stage:
  model_name: "deepseek/deepseek-chat:free"  # Default Q&A model used in QATransformStage
  model_type: "deepseek"  # Can be "qa" (HuggingFace) or "deepseek" (OpenRouter)
  api_key: "openRouter_key"  # If using DeepSeek through OpenRouter

```

---


## Future Enhancements


Advanced Context Summarization: Implement an optional summarization step to reduce large contexts before passing them to the QA model.

Embedding-Based Retrieval: Integrate a vector database to retrieve the most relevant passages for the given question, optimizing the pipeline for larger datasets.

Multi-Source Data Fetching: Extend the pipeline to fetch and merge content from additional sources like scholarly databases, news websites, or local documents.

Parallel Processing: Enable parallel execution of pipeline stages to improve performance for large-scale data processing.

Model Auto-Selection: Dynamically select the best model (e.g., local or remote) based on the complexity of the question or context length.

Enhanced Error Handling: Add more robust mechanisms for catching and retrying failed API calls or handling network timeouts.

----

## Author

[Rama Amairy](https://github.com/Rama-Amairy)

---



