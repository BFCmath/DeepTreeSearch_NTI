# HOW_TO_USE.md

## Purpose

This guide explains how to use DeepResearch Bench to evaluate different deep research agent approaches, focusing on **RACE evaluation** for about **10 English questions**.

---

## 1. Select Evaluation Questions

- Benchmark queries are in `data/prompt_data/query.jsonl`.
- Each line is a JSON object with `"language": "en"` for English.
- To evaluate only 10 questions:
  - Manually select 10 English queries from this file.
  - Or use the `--limit` and `--only_en` options in the script.

---

## 2. Prepare Model Outputs

- Run your agent on the selected queries.
- Save results in: `data/test_data/raw_data/<your_model_name>.jsonl`
- **Format for each line:**
  ```json
  {
    "id": "task_id",
    "prompt": "original_query_text",
    "article": "generated_research_article_with_citations"
  }
  ```

---

## 3. API Setup

- **Gemini API key** is required for RACE evaluation.
- Set it as an environment variable:
  - On Linux/macOS:
    ```bash
    export GEMINI_API_KEY="your_gemini_api_key_here"
    ```
  - On Windows PowerShell:
    ```powershell
    $env:GEMINI_API_KEY="your_gemini_api_key_here"
    $env:TAVILY_API_KEY="your_tavily_api_key_here"
    ```

---

## 4. Run RACE Evaluation

- Edit `run_benchmark.sh`:
  - Add your model name to `TARGET_MODELS`.
  - Uncomment or set:
    ```bash
    LIMIT="--limit 10"
    ONLY_EN="--only_en"
    ```
- Run the script:
  - On Linux/macOS:
    ```bash
    bash run_benchmark.sh
    ```
  - On Windows, use WSL/bash or adapt commands for PowerShell.

- Only RACE will be run (FACT is separate).

---

## 5. How RACE Evaluation Works

- The script calls `deepresearch_bench_race.py`.
- For each query:
  - Loads evaluation criteria and reference answers.
  - Uses Gemini API to score your agent’s output on multiple dimensions (comprehensiveness, depth, instruction-following, readability).
  - Aggregates and saves results to:
    - `results/race/<your_model_name>/race_result.txt`

---

## Summary Checklist

- [ ] Select 10 English queries from `query.jsonl`
- [ ] Run your agent, save results in required format
- [ ] Set `GEMINI_API_KEY`
- [ ] Edit `run_benchmark.sh` for your model and options
- [ ] Run the script to get RACE results

---

For more details, see the project’s `README.md`. If you want to use other LLMs for evaluation, modify `AIClient` in `utils/api.py`.
