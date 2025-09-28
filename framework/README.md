# Framework Module

This folder contains the core logic for running the deep research pipeline. It provides the main entry point and the base framework for executing different research approaches using large language models (LLMs).

## Structure
- `main.py`: Example script to run the research pipeline. Initializes the LLM, sets the research topic, selects the approach, and prints the final report.
- `base_framework.py`: Contains the `run_pipeline` function, which orchestrates the research workflow.
- `approaches/`: Directory for different research strategies. Each subfolder (e.g., `zeroshot`, `plan_first`, `react`) implements a unique approach. The approach name in `main.py` must match the folder name here.
- `tools/`: Utility modules for search and other supporting functions.

## Usage
1. Set your `GOOGLE_API_KEY` in a `.env` file for LLM access.
2. Run `main.py` to execute the pipeline:
   ```bash
   python main.py
   ```
3. Modify the research topic or approach in `main.py` as needed.

## Customization
- To add a new approach, create a new folder in `approaches/` and implement the required logic.
- You can swap out the LLM in `main.py` for other models (e.g., OpenAI, Anthropic).

## Requirements
- Python 3.8+
- Required packages listed in the root `requirements.txt`

## License
See the main project LICENSE file for details.
