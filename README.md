# JSON Processor

This is the repo for the paper [How Good Are LLMs at Processing Tool Outputs?](https://arxiv.org/pdf/2510.15955)

## Quick Start

### Local install:

```bash
pip install .
```

### QA data

The directory `generate_qa_pairs` contains the dataset creation code. Specifically, `generate_qa_pairs/tasks` has Python scripts to create the QA pairs for each of the API endpoints. 
The source API responses for all the booking.com endpoints are derived from [ComplexFuncBench](https://huggingface.co/datasets/THUDM/ComplexFuncBench/tree/main).


### Experiments

All the experiment settings can be run by executing `experimental_scripts/qa_inference.py`

To determine the accuracy of the predictions, run `experimental_scripts/qa_evaluation.py`

#### Setups
- Answer generation in the paper refers to the `direct_prompting_*` setup type in the code.
- Code generation in the paper refers to the `code_generation_*` setup type in the code. 
- Results in the `Simplify JSON` subsection in the paper are obtained by setting `setup_type` to `direct_prompting_schema_cfx2` and `code_generation_schema_cfx2`

## Cite as
```
@misc{kate2025how,
      title={How Good Are LLMs at Processing Tool Outputs?}, 
      author={Kiran Kate and Yara Rizk and Poulami Ghosh and Ashu Gulati and Tathagata Chakraborti and Zidane Wright and Mayank Agarwal},
      year={2025},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={},
      url={}, 
}
```