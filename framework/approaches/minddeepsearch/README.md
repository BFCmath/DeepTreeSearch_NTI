# MindDeepSearch: Deep Research Optimization

## Overview

MindDeepSearch is an adaptation of MindSearch specifically optimized for deep research tasks. While maintaining the same multi-agent architecture, it enhances prompts and data flow to produce comprehensive, well-sourced research reports.

## Key Differences from MindSearch

### 1. **Enhanced Prompts**

#### Searcher Agent
- **Role**: Professional research assistant (not just intelligent assistant)
- **Principles**: Emphasizes comprehensiveness, depth, source quality, and citation rigor
- **Requirements**: Multiple searches, detailed answers with statistics/examples, structured responses
- **Example**: Deep research question with multi-angle investigation approach

#### Planner Agent
- **Role**: Senior research strategist (not just programmer)
- **Philosophy**: Systematic decomposition, multi-dimensional analysis, progressive depth
- **Task Design**: Identifies core dimensions, creates targeted questions, builds logical dependencies
- **Question Principles**: Specific, answerable, comprehensive, non-overlapping
- **Example**: Elderly care market research with progressive deepening

#### Final Report
- **Requirements**: Executive summary, logical sections, data-rich content, analytical insights
- **Citation Standards**: Every claim cited, professional tone, comprehensive coverage
- **Structure**: Formal report format with clear headings and depth

### 2. **Complete Data Inclusion**

The final report generation now receives:

```
# Deep Research Materials

## Original Research Topic
[User's question]

## Research Structure
For each sub-question investigated:
  ### Research Question: [question]
  **Answer:** [synthesized answer without inline citations]
  **Source Materials:** 
    - url1
    - url2
    ...
```

This ensures the LLM has:
1. The initial research topic
2. Each node's research question
3. Synthesized answers (without inline citations for cleaner evaluation)
4. **ALL raw source URLs** that were crawled for reference

### 3. **Architecture Unchanged**

The core MindSearch architecture remains identical:
- WebSearchGraph manages nodes and edges
- SearcherAgent conducts web searches with ReAct loop
- MindSearchAgent plans research strategy
- Parallel search execution via ThreadPoolExecutor
- Progressive depth: initial questions → follow-up questions → final synthesis

## Usage

The approach integrates seamlessly with the framework:

```python
from approaches.minddeepsearch.chain import get_chain

# Get the chain
research_chain = get_chain(model, search_tool)

# Run research
result = research_chain.invoke({"topic": "Your research question"})

# Access results
article = result["final_output"]["article"]
search_count = result["final_output"]["metadata"]["search_count"]
```

## Configuration in main.py

```python
selected_approach = "minddeepsearch"
```

## Expected Output Quality

MindDeepSearch should produce reports with:
- **Comprehensive coverage**: All aspects of the topic investigated
- **Rich detail**: Specific data, statistics, examples, case studies
- **Clean prose**: No inline citations (sources tracked separately)
- **Professional structure**: Executive summary, clear sections, logical flow
- **Analytical depth**: Not just facts, but trends, patterns, implications
- **Source transparency**: All URLs listed per research question for reference

## Comparison

| Aspect | MindSearch | MindDeepSearch |
|--------|-----------|----------------|
| **Target Task** | Multi-hop Q&A | Deep research reports |
| **Searcher Role** | Intelligent assistant | Professional researcher |
| **Question Style** | Specific, focused | Research-oriented, comprehensive |
| **Answer Style** | Direct answers | Detailed findings with analysis |
| **Final Output** | Synthesized answer | Professional research report |
| **Data Included** | Q&A pairs | Q&A + all source URLs |
| **Prompt Emphasis** | Accuracy | Comprehensiveness + depth |

## Files

- `chain.py`: Core implementation with enhanced data aggregation
- `prompts.py`: Optimized prompts for deep research
- `README.md`: This documentation 