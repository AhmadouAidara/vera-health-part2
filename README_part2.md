# Vera Health Challenge — Part 2

## Goal

Build a pipeline that retrieves the most relevant and reliable scientific papers for each of 11 clinical questions using Zero-Entropy and OpenAI APIs.

## Project Structure

```
vera-part2/
├── main.py                   # Entry point for the pipeline
├── .env                      # Environment variables with API keys
├── requirements.txt          # Required dependencies
├── data/
│   └── journals.py           # Journal metadata parsing and merging
│   └── journals.ts
├── src/
│   ├── retrieval.py          # ZeroEntropy document retrieval
│   ├── gpt_filter.py         # GPT-based relevance filtering
│   ├── scoring.py            # Reliability scoring
│   ├── selection.py          # Top-15 document selection
│   └── text_fetcher.py       # Fallback method to fetch document text
│
└── results/
    └── top_15_papers.csv     # Final output for each question
```

## How to Run

1. Set your API keys in a `.env` file:
```
OPENAI_API_KEY=your-openai-key
ZEROENTROPY_API_KEY=your-zeroentropy-key
```

2. Create and activate a virtual environment, then install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the pipeline:
```bash
python main.py
```

The top 15 papers per question will be saved in `results/top_15_papers.csv`.

## Deliverables

- Top-15 papers per question with combined relevance and reliability scores.
- Fully functional pipeline using both retrieval (ZeroEntropy) and GPT-based filtering.
- Clean and modular code.
- Documentation of methodology and design decisions in this README.

## Methodology Overview

1. **Retrieval**: Retrieve documents for each clinical question using multiple ZeroEntropy filters.
2. **Filtering**: Use GPT to assess the relevance of each document to the clinical question.
3. **Scoring**: Apply a reliability scoring function using weights from Part 1 and optional journal metadata (SJR).
4. **Selection**: Output the 15 best-scored documents per question.

This system ensures only the most relevant, reliable, and recent medical evidence is returned.

