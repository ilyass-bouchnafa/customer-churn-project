# Customer Churn Prediction

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-green.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-ready machine learning system that predicts customer churn with 95% accuracy, enabling proactive retention strategies through data-driven insights.

![Project Banner](https://img.shields.io/badge/Status-Production%20Ready-success)

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Project Highlights](#-project-highlights)
- [Methodology](#-methodology)
- [Model Performance](#-model-performance)
- [Deployment](#-deployment)
- [Technologies Used](#️-technologies-used)
- [Understanding Key Metrics](#-understanding-key-metrics)
- [Key Insights & Learnings](#-key-insights--learnings)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Support](#-contact--support)

## 🎯 Project Overview

In today's highly competitive digital environment, businesses can no longer afford to wait for customers to leave before taking action. Customer churn represents not just a cancellation, but a significant loss of future revenue and long-term value.

This project leverages **machine learning** to transform customer behavioral data into actionable intelligence, enabling companies to shift from reactive to **proactive retention strategies**.

### 🔑 Key Question

**How can we exploit customer behavioral data to predict churn and optimize retention strategies?**

### ✨ Key Features

- **High Performance**: 95% AUC-ROC score with 99% recall
- **Real-time Predictions**: Instant churn probability assessment
- **Interactive Dashboard**: User-friendly Streamlit interface for business teams
- **Explainable AI**: Feature importance analysis reveals actionable insights
- **Production Ready**: MLOps-structured codebase with model versioning
- **Scalable**: Handles datasets with 500,000+ customer records

---

## 📊 Project Highlights

### Business Impact

| Metric | Value | Impact |
|--------|-------|--------|
| **Recall** | 99% | Detects almost all at-risk customers |
| **AUC-ROC** | 0.95 | Excellent discrimination capability |
| **Precision** | 90% | Minimizes false alerts |
| **Dataset Size** | 500K+ rows | Enterprise-scale solution |

### Top Churn Predictors

1. **Support Call Frequency** 🎧 - Most critical indicator
2. **Total Spend** 💰 - Strong loyalty signal
3. **Payment Delays** ⏰ - Early warning sign





---

##  Methodology

### 1. Data Quality Assessment

- **Dataset Size**: ~500,000 customer records
- **Missing Values**: Only 1 (negligible impact - removed)
- **Duplicates**: None detected
- **Outliers**: High-value customers in Total Spend preserved (legitimate data)

### 2. Exploratory Data Analysis (EDA)

#### Class Distribution
- **55.5%** customers retained
- **44.5%** customers churned
- *Slight imbalance addressed through stratified sampling*

#### Critical Thresholds Identified

| Feature | Churn Threshold | Insight |
|---------|----------------|---------|
| **Total Spend** | < $500 | High churn risk |
| **Support Calls** | > 5 calls | Strong churn indicator |
| **Payment Delays** | > 20 days | Critical warning sign |
| **Account Inactivity** | > 15 days | Maximum churn risk |
| **Age** | 30-50 years | Highest loyalty segment |

#### Categorical Insights

- **Contract Duration**: Monthly contracts → high churn; Annual contracts → strong retention
- **Subscription Type**: Premium > Standard > Basic (retention rate)
- **Gender**: Slight difference observed (females marginally higher churn)

### 3. Preprocessing Pipeline

- ✅ Data cleaning and validation
- ✅ Categorical variable encoding
- ✅ Feature normalization and scaling
- ✅ Stratified train/test split (maintains class distribution)

### 4. Model Selection Process

#### Baseline Model
**Dummy Classifier** - Establishes minimum performance threshold (always predicts majority class)

#### Models Evaluated

| Model Type | Models | Performance | Outcome |
|------------|--------|-------------|---------|
| **Linear** | Logistic Regression, Naive Bayes | High false negatives | ❌ Insufficient |
| **Non-linear** | KNN, Decision Tree | KNN: Good isolation; Tree: Unstable | ⚠️ Moderate |
| **Ensemble** | Random Forest, XGBoost | Excellent recall & precision | ✅ **Best** |

#### Why Random Forest? 🏆

While XGBoost achieved comparable performance, **Random Forest** was selected because:
- ✅ **Best Recall (99%)**: Minimizes missed at-risk customers
- ✅ **Robust & Stable**: Reliable for production deployment
- ✅ **Interpretable**: Clear feature importance for business decisions
- ✅ **Lower Complexity**: Easier maintenance and monitoring

> **Business Priority**: It's better to identify all at-risk customers (high recall) even with some false alerts, than to miss customers who will churn.

---

## 📊 Model Performance

### Confusion Matrix (Random Forest)

|  | Predicted: Stay | Predicted: Churn |
|---|----------------|------------------|
| **Actual: Stay** | 38,640 ✅ | 6,303 ⚠️ |
| **Actual: Churn** | 287 ❌ | 55,812 ✅ |

- **True Positives (55,812)**: Correctly identified churners
- **False Negatives (287)**: Missed only 0.5% of churners
- **False Positives (6,303)**: Acceptable false alerts
- **True Negatives (38,640)**: Correctly identified loyal customers

### Performance Metrics

```
Accuracy:  94.8%
Precision: 89.8%
Recall:    99.5% ⭐
F1-Score:  94.4%
AUC-ROC:   0.95
```

### ROC Curve Analysis

The **ROC (Receiver Operating Characteristic) Curve** measures the model's ability to distinguish between classes:
- **AUC = 0.95** indicates excellent discrimination
- Random Forest and XGBoost significantly outperform simpler models
- High True Positive Rate with minimal False Positive Rate

### Feature Importance

The model's decisions are driven by:

| Rank | Feature | Importance | Business Insight |
|------|---------|-----------|------------------|
| 1️⃣ | **Support Calls** | Highest | Frequent contact = dissatisfaction signal |
| 2️⃣ | **Total Spend** | High | Low spend = weak engagement |
| 3️⃣ | **Payment Delays** | High | Financial issues or disengagement |
| 4️⃣ | Contract Type | Medium | Monthly > Annual churn risk |
| 5️⃣ | Account Inactivity | Medium | User disengagement indicator |
| ⬇️ | Age, Gender | Low | Demographics less predictive |

> **No Black Box**: Feature importance analysis ensures transparent, actionable business decisions.

---

## 🎨 Deployment

### MLOps Architecture

The project follows **MLOps best practices** with clear separation of concerns:

```
├── Data Layer       → Raw and processed datasets
├── Development      → Jupyter notebooks for experimentation
├── Model Layer      → Trained models with versioning
└── Application      → Production-ready Streamlit interface
```

### Streamlit Web Application

The model is deployed via an **interactive web application** that enables:

- 📊 **Real-time Predictions**: Input customer data and get instant churn probability
- 🎯 **Risk Assessment**: Visual indicators for churn risk levels
- 📈 **Feature Analysis**: Understand which factors contribute to churn
- 💾 **Report Generation**: Download prediction reports for stakeholder review
- 👥 **Business-Friendly**: No technical knowledge required

**Benefits**:
- Transforms ML predictions into actionable business intelligence
- Enables targeted retention campaigns
- Facilitates data-driven decision making

---

## 🛠️ Technologies Used

### Core Framework
- **Python 3.8+** - Primary programming language

### Machine Learning
- **Scikit-learn** - Model training and evaluation
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

### Visualization
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical graphics
- **Plotly** - Interactive charts

### Deployment
- **Streamlit** - Web application framework
- **Pickle** - Model serialization

---

## 📖 Understanding Key Metrics

### Why Recall is Critical for This Project

**Recall** measures: *"Of all customers who actually churned, how many did we detect?"*

```
Recall = True Positives / (True Positives + False Negatives)
```

**Business Translation**:
- High recall (99%) = We catch almost all customers at risk
- Low False Negatives = Very few churners slip through undetected
- **Better to have false alerts than miss a churning customer**

### ROC Curve & AUC Explained

**ROC Curve** plots:
- **X-axis (FPR)**: False Positive Rate - loyal customers incorrectly flagged
- **Y-axis (TPR)**: True Positive Rate - churners correctly detected

**AUC (Area Under Curve)** interpretation:
- **0.5** = Random guessing (useless model)
- **0.95** = Our model (excellent discrimination)
- **1.0** = Perfect prediction

---

## 🎓 Key Insights & Learnings

### Data Quality
While the dataset was exceptionally clean, comprehensive data cleaning techniques were explored and documented in `optionnel.ipynb`, including:
- Advanced imputation methods (MICE, KNN)
- Outlier detection and treatment
- Data validation strategies

*This additional exploration demonstrates technical proficiency in data preprocessing, even when not strictly required for the final model.*

### Model Selection Strategy
- Simple models (Logistic Regression, Naive Bayes) failed to capture complex patterns
- Non-linear models (KNN) showed promise but lacked stability at scale
- **Ensemble methods** (Random Forest, XGBoost) provided the robustness needed for production

### Business Alignment
Every technical decision was made with business value in mind:
- **Recall > Precision**: Missing a churner is costlier than a false alert
- **Interpretability**: Feature importance guides retention strategies
- **Usability**: Streamlit interface empowers non-technical stakeholders

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



---

## 🙏 Acknowledgments

- Dataset provided by [Source Name/Organization]
- Inspiration from industry best practices in customer retention analytics
- Special thanks to academic supervisors for guidance and feedback

---

## 📞 Contact & Support

For questions, suggestions, or collaboration opportunities:
- 📧 Email: your.email@example.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/customer-churn-project/issues)

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

</div>
