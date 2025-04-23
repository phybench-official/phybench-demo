---
license: mit
task_categories:
- question-answering
- mathematical-reasoning
language:
- en
size_categories:
- 500<n<1K
---

<div align="center">
<img src='https://example.com/phybench-logo.png' width=300px> <!-- (Placeholder for actual logo) -->
  
<p align="center" style="font-size:28px"><b>PHYBench: Holistic Evaluation of Physical Perception and Reasoning in Large Language Models</b></p>
<p align="center">
<a href="https://phybench.ai">[🌐 Project]</a>
<a href="https://arxiv.org/abs/XXXX.XXXXX">[📄 Paper]</a>
<a href="https://github.com/PHYBench/PHYBench">[💻 Code]</a>
<a href="#-overview">[🌟 Overview]</a>
<a href="#-data-details">[🔧 Data Details]</a>
<a href="#-citation">[🚩 Citation]</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)

---

</div>

## 🌟 Overview

PHYBench is the first large-scale benchmark specifically designed to evaluate **physical perception** and **robust reasoning** capabilities in Large Language Models (LLMs). With **500 meticulously curated physics problems** spanning mechanics, electromagnetism, thermodynamics, optics, modern physics, and advanced physics, it challenges models to demonstrate:

- **Real-world grounding**: Problems based on tangible physical scenarios (e.g., ball inside a bowl, pendulum dynamics)
- **Multi-step reasoning**: Average solution length of 3,000 characters requiring 10+ intermediate steps
- **Symbolic precision**: Strict evaluation of LaTeX-formulated expressions through novel **Expression Edit Distance (EED) Score**

Key innovations:
- 🎯 **EED Metric**: Continuous scoring (0-100) measurement based on the edit-distance on expression tree
- 🏋️ **Difficulty Spectrum**: high school, undergraduate, Olympiad-level physics problems
- 🔍 **Error Taxonomy**: Explicit evaluation of Physical Perception (PP) vs Robust Reasoning (RR) failures

## 🔧 Data Details

### Dataset Component
| Category | Subdomains | 
| --- | --- | 
| Mechanics | Dynamics, Kinematics, Rotational | 
| Electromagnetism | Fields, Circuits, Relativistic EM | 
| Thermodynamics | Statistical Mechanics, Heat Engines | 
| Optics | Wave, Geometric, Quantum Optics | 
| Modern Physics | SR/GR, Quantum Mechanics | 
| Advanced Physics | Plasma, Condensed Matter | 


**Answer Types**:  
🔹 Strict symbolic expressions (e.g., `\sqrt{\frac{2g}{3R}}`)  
🔹 Multiple equivalent forms accepted  
🔹 No numerical approximations or equation chains  

## 🛠️ Data Curation

### 3-Stage Rigorous Validation Pipeline

1. **Expert Creation & Strict Screening**  
   - 178 PKU physics students contributed problems that are:
     - Almost entirely original/custom-created
     - None easily found through direct internet searches or standard reference materials
   - Strict requirements:
     - Single unambiguous symbolic answer (e.g., `T=2mg+4mv₀²/l`)
     - Text-only solvability (no diagrams/multimodal inputs)
     - Rigorously precise statements to avoid ambiguity
     - Solvable using only basic physics principles (no complex specialized knowledge required)
   - No requirements on AI test to avoid filtering for AI weaknesses

2. **Multi-Round Academic Review**  
   - Dedicated internal platform for peer review:
     ![Review Interface](https://example.com/review-platform.png)
   - 3-tier verification process:
     - Initial filtering: Reviewers assessed format validity and appropriateness (not filtering for AI weaknesses)
     - Ambiguity detection and revision: Reviewers analyzed LLM-generated solutions to identify potential ambiguities in problem statements
     - Iterative improvement cycle: Questions refined repeatedly until all LLMs can understand the question and follow the instructions to produce the expressions it believes to be right.

3. **Human Expert Finalization**
  - **81 PKU students participated:**
  - Each student independently solved 8 problems from the dataset
  - Evaluate question clarity, statement rigor, and answer correctness
  - Establish of human baseline performance meanwhile




## 📊 Evaluation Protocol

### Machine Evaluation
**Dual Metrics**:  
1. **Accuracy**: Binary correctness (expression equivalence via SymPy simplification)  
2. **EED Score**: Continuous assessment of expression tree similarity

The EED Score evaluates the similarity between the model-generated answer and the ground truth by leveraging the concept of expression tree edit distance. The process involves the following steps:

1. **Simplification of Expressions**:  
   Both the ground truth (`gt`) and the model-generated answer (`gen`) are first converted into simplified symbolic expressions using the `sympy.simplify()` function. This step ensures that equivalent forms of the same expression are recognized as identical.

2. **Equivalence Check**:  
   If the simplified expressions of `gt` and `gen` are identical, the EED Score is assigned a perfect score of 100, indicating complete correctness.

3. **Tree Conversion and Edit Distance Calculation**:  
   If the expressions are not identical, they are converted into tree structures. The edit distance between these trees is then calculated using an extended version of the Zhang-Shasha algorithm. This distance represents the minimum number of node-level operations (insertions, deletions, and updates) required to transform one tree into the other.

4. **Relative Edit Distance and Scoring**:  
   The relative edit distance \( r \) is computed as the ratio of the edit distance to the size of the ground truth tree. The EED Score is then determined based on this relative distance:
   - If \( r = 0 \) (i.e., the expressions are identical), the score is 100.
   - If \( 0 < r < 0.6 \), the score is calculated as \( 60 - 100r \).
   - If \( r \geq 0.6 \), the score is 0, indicating a significant discrepancy between the model-generated answer and the ground truth.

This scoring mechanism provides a continuous measure of similarity, allowing for a nuanced evaluation of the model's reasoning capabilities beyond binary correctness.

**Key Advantages**:  
- 204% higher sample efficiency vs binary metrics  
- Distinguishes coefficient errors (EED=30-60) vs structural errors (EED<30)

### Human Baseline

- **Participants**: 81 PKU physics students  
- **Protocol**:  
  - **8 problems per student**: Each student solved a set of 8 problems from PHYBench dataset  
  - **Time-constrained solving**: 3 hours.
- **Performance metrics**:
  - **61.9±2.1% average accuracy**
  - **70.4±1.8 average EED Score**
  - Top quartile reached 71.4% accuracy and 80.4 EED Score
  - Significant outperformance vs LLMs: Human experts outperformed all evaluated LLMs at 99% confidence level
  - Human experts significantly outperformed all evaluated LLMs (99.99% confidence level)


## 🚩 Citation
```bibtex
@article{
}
