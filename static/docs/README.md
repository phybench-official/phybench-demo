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
- 🎯 **EED Metric**: Continuous scoring (0-100) measuring expression tree similarity, capturing partial correctness
- 🏋️ **Difficulty Spectrum**: high school, undergraduate, Physics Olympiad-level problems
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

1. **Expert Creation & Initial Screening**  
   - 178 PKU physics students contributed problems from:
     - 80% non-public sources (internal competition materials/custom puzzles)
     - 20% public textbooks/Olympiad archives
   - Strict requirements:
     - Single unambiguous symbolic answer (e.g., `T=2mg+4mv₀²/l`)
     - Text-only solvability (no diagrams/multimodal inputs)

2. **Multi-Round Academic Review**  
   - Dedicated internal platform for peer review:
     ![Review Interface](https://example.com/review-platform.png)
   - 3-tier verification process:
     | Stage | Checkpoints | 
      | --- | --- | 
      | 1 | Physics validity, Answer uniqueness | 
      | 2 | LLM-ambiguous phrasing elimination | 
      | 3 | SymPy computability verification | 

### 3. **Human Expert Finalization**  
- **109 PKU students completed:**  
  - **8-problem validation sets (20% overlap for consistency)**  
    A total of 109 students from Peking University participated in the final validation phase. Each student was assigned a set of 8 problems designed to evaluate the clarity, accuracy, and comprehensiveness of the questions. To ensure consistency and reliability in the evaluation process, 20% of the problems in each set overlapped with those in other sets. This overlap allowed the researchers to compare and verify the consistency of the feedback provided by different students, thereby ensuring the high quality and reliability of the final benchmark.

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
- 116% higher sample efficiency vs binary metrics  
- Distinguishes coefficient errors (EED=50-90) vs structural errors (EED<30)

### Human Baseline

- **Participants**: 70 PKU physics students  
- **Protocol**:  
  - **20% overlap problems for consistency checking**: To ensure the reliability of the human evaluation, 20% of the problems in the validation sets were overlapping. This allowed the researchers to check the consistency of the students' answers across different sets.  
  - **Time-constrained solving (15min/problem average)**: Students were given an average of 15 minutes per problem to solve, simulating a realistic test environment.  
  - **Achieved 70%  accuracy vs SOTA models' 34.8% (Gemini-2.5-Pro)**: The human participants achieved an average accuracy of 70%, with a margin of error of ±5%. This is significantly higher than the state-of-the-art models, with the highest-performing model (Gemini-2.5-Pro) achieving only 34.8% accuracy.

## 🚩 Citation
```bibtex
@article{
}
