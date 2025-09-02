# Text Annotation & LLM Evaluation Toolkit

**A Python-based toolkit designed for efficient text annotation and evaluation, tailored for Large Language Model (LLM) applications. This toolkit supports multi-label and multi-format annotation, enabling seamless integration into various data processing pipelines.**

## Features 🚀

## Features 🚀
 - Multi-Format Input Support: Annotate text data from JSON, CSV, and Markdown files.

 - Multi-Label Annotation: Assign multiple labels to each text entry, accommodating complex categorization needs.

 - Standardized Output: Export annotations in a consistent JSON format for downstream processing.

 - Evaluation Metrics: Assess annotation quality using accuracy, precision, recall, and F1-score.

 - Interactive CLI: Use command-line interface for batch processing and automation.

 - GPU Acceleration: Optional GPU support for faster image annotation using Hugging Face models.

 - Async & Batching: Process large image datasets efficiently with asynchronous execution and configurable batch sizes.

 - Benchmarking: Built-in tools to measure annotation performance over different dataset sizes.


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
from src.annotator import annotate_file

annotations = annotate_file(
    input_path="data/input.json",
    output_path="data/output.json",
    labels=["general", "technical"]
)

from src.evaluator import evaluate_file

evaluation = evaluate_file(
    predicted_path="data/pred.json",
    reference_path="data/ref.json"
)

print(f"Accuracy: {evaluation['accuracy'] * 100:.2f}%")

```
**CLI example:**
```bash
# Annotate a text file
python src/cli.py annotate --input data/input.json --output data/output.json

# Evaluate LLM outputs
python src/cli.py evaluate --pred data/pred.json --ref data/ref.json
```
## Input Formats
JSON: An array of strings or objects containing a "text" field.

CSV: A file with a "text" column.

Markdown: A plain text file with one entry per line.

## Evaluation Metrics
Accuracy: Percentage of exact matches between predicted and reference labels.

Precision: Proportion of true positive predictions among all positive predictions.

Recall: Proportion of true positive predictions among all actual positives.

## Multimodal Support
The toolkit now supports image annotation alongside text:

Input Directory: Accepts a folder of images (.png, .jpg, .jpeg) in data/images/.

Annotation: Assign multiple labels to each image (multi-label support).

Output: Export annotations in JSON or CSV format (data/image_output.json or data/image_output.csv).

Batching & Limits: Configure batch size and optionally limit the number of images processed for testing or benchmarking.

Synthetic Images: You can generate sample images using Python (PIL) for testing purposes.

Benchmarking: Use the `tests/test_image_annotator.py` to benchmark annotation speed over different dataset sizes (10, 20, 50 images).

## Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your proposed changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

