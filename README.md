# Text Annotation & LLM Evaluation Toolkit

**Toolkit for text annotation and evaluation of Large Language Model (LLM) outputs.**

## Features

- Annotate text in multiple formats: JSON, CSV, XML, Markdown.
- Evaluate LLM-generated text for grammar, style, and factual correctness.
- Command-line interface (CLI) for batch annotation and evaluation.
- Regex utilities for text parsing and content extraction.
- Export annotations and evaluation reports in standard formats.

## Installation

```bash
# Clone the repository
git clone https://github.com/kanmanivj/Text-Annotation-LLM-Toolkit.git
cd Text-Annotation-LLM-Toolkit

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```
## Usage

You can use the toolkit either via Python or via the command-line interface (CLI).

**Python example:**

```python
from src.annotator import annotate_text
from src.evaluator import evaluate_llm_output

# Annotate text
data = ["Amazon is hiring AI experts.", "Python is fun!"]
annotations = [annotate_text(t, "label") for t in data]
print("Annotations:", annotations)

# Evaluate LLM output
score = evaluate_llm_output("Prediction text", "Reference text")
print("Evaluation score:", score)
```
**CLI example:**
```bash
# Annotate a text file
python src/cli.py annotate --input data/input.json --output data/output.json

# Evaluate LLM outputs
python src/cli.py evaluate --pred data/pred.json --ref data/ref.json
```


