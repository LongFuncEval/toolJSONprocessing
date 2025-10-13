# Long Structured (JSON) Tool Response Dataset
This dataset contains JSON API responses and associated question and answer pairs where the answer to a question is found in the JSON file. 

## Quick Start
To (re)generate the QA pairs, run `qa_pairs_generation.py` with the Working Directory set to `toolJSONprocessing` or using `python -m generate_qa_pairs.qa_pairs_generation`. 


## Question Types
We create question templates that were grouped into three main categories:
- Extractive - extracting a single value for a given key in the JSON response
- Filtering - retrieving one or more
entries based on some filtering criteria
- Aggregation -  aggregating multiple entries by performing an aggregation operation to obtain the final answer (e.g., average, sum, etc.)

## Metrics
Based on the type of question, we adopt an appropriate metric to compare the ground truth answer to the predict answer:
- String match - exact match on the string
- Unordered list match - compare items in two lists ignoring order
- Approximate number match - compare to floating point numbers accounting for rounding

