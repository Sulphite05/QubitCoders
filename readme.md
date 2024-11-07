# QubitCoders - LeetCode Profile Analyzer

---
## Overview
QubitCoders is a web app designed for **CIS students at NEDUET** and aspiring coders to improve their problem-solving skills by analyzing their LeetCode profiles. The app provides personalized advice on how to improve based on contest ratings, the number of problems solved, and expertise level.

### Features
- **Ranking**: View the rankings of CIS students in the community.
- **Classifier**: Get your LeetCode profile classified based on your skills (Beginner, Intermediate, Advanced).
- **Recommendations**: Get personalized advice based on your LeetCode profile, including solved problems in Easy, Medium, and Hard categories.

---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [App Features](#app-features)
4. [Technologies Used](#technologies-used)
5. [Model Integration](#model-integration)
6. [Deployment](#deployment)
7. [Contributors](#contributors)

---

## Installation

To run the **QubitCoders** app locally, follow these steps:

### Prerequisites
- Python >= 3.7
- Streamlit
- HuggingFace Transformers (for LLaMA integration)

### Clone the repository
```bash
git clone https://github.com/yourusername/qubitcoders.git
cd qubitcoders
```

### Install dependencies
```bash
pip install -r requirements.txt
```
---
## Usage

1. Launch the app:
```bash
streamlit run app.py
```

2. Navigate through the app:
- On the Welcome Page, learn more about the QubitCoders community and its purpose.
- Ranking: View the leaderboard for CIS students in the department.
- Classifier: Enter your LeetCode username to classify your expertise level.
- Recommendations: Based on your LeetCode profile, get personalized advice for improvement.

---
## App Features

### Ranking
View the leaderboard to see how you rank compared to other CIS students at NEDUET.

### Classifier
Enter your LeetCode profile to classify your expertise level:
- Beginner
- Intermediate
- Advanced
- Recommendations
---
## Technologies Used

- Streamlit: Web framework used to build the app.
- Python: Programming language.
- HuggingFace: Used for integrating LLaMA-2 for personalized coding advice. 
- pandas: For handling data processing and displaying dataframes.
- NumPy: For numerical calculations.
- scikit-fuzzy: Used for expertise classification based on fuzzy logic.
- GitHub: For version control and project management.

---
## Model Integration

### Expertise Classifier
The app uses scikit-fuzzy to classify users into four expertise levels based on their contest ratings and the number of problems solved (easy, medium, hard).

### Recommendations via LLaMA 2
We integrated the LLaMA 2 model via HuggingFace’s Transformers to generate personalized advice based on the user’s LeetCode profile. The input includes:

- Expertise level
- Contest rating
- Number of solved easy, medium, and hard problems
---

## Deployment
The QubitCoders app is deployed on Streamlit Cloud. To view the live version, click here.

---
## Contributor

- Aqiba Abdul Qadir: Creator and Developer
---
## License

This project is licensed under the MIT License - see the LICENSE file for details.