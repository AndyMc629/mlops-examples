import warnings

import matplotlib.pyplot as plt
import mpld3  # Converts matplotlib plots to interactive HTML
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

# Generate synthetic telecom customer data
np.random.seed(42)
n_samples = 1000

tenure = np.random.gamma(shape=2.0, scale=15, size=n_samples)
monthly_charges = np.random.normal(loc=70, scale=25, size=n_samples)
total_spend = tenure * monthly_charges * (1 + np.random.normal(0, 0.1, n_samples))
service_calls = np.random.poisson(lam=2, size=n_samples)
has_premium = np.random.binomial(n=1, p=0.4, size=n_samples)

churn_probability = (
    0.5
    - 0.03 * np.log(tenure + 1)
    + 0.004 * monthly_charges
    + 0.05 * service_calls
    - 0.15 * has_premium
)
churn_probability = np.clip(churn_probability, 0.05, 0.95)
churn = np.random.binomial(n=1, p=churn_probability)

data = pd.DataFrame(
    {
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_spend": total_spend,
        "service_calls": service_calls,
        "has_premium": has_premium,
        "churn": churn,
    }
)

# Prepare the HTML plots
figs = []


def add_section(title, description, fig_html):
    """Format each section with a title and description before embedding the plot."""
    return (
        f"<div class='section'>"
        f"<h2>{title}</h2>"
        f"<p>{description}</p>"
        f"<div class='plot-container'>{fig_html}</div>"
        f"</div>"
    )


# Add explanatory sections
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="churn", y="tenure", data=data, ax=ax)
ax.set_title("Tenure by Churn Status")
figs.append(
    add_section(
        "Customer Tenure vs Churn",
        "Customers with a longer tenure tend to have a lower churn rate. This suggests that retaining customers for longer periods increases loyalty and reduces churn.",
        mpld3.fig_to_html(fig),
    )
)

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="churn", y="monthly_charges", data=data, ax=ax)
ax.set_title("Monthly Charges by Churn Status")
figs.append(
    add_section(
        "Monthly Charges vs Churn",
        "Customers with higher monthly charges tend to churn more frequently. This suggests that pricing might be a factor in customer retention.",
        mpld3.fig_to_html(fig),
    )
)

fig, ax = plt.subplots(figsize=(10, 8))
correlation = data.corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Feature Correlation Matrix")
figs.append(
    add_section(
        "Feature Correlation Analysis",
        "This heatmap shows the relationships between different customer attributes. Strong correlations can help in feature selection for churn prediction models.",
        mpld3.fig_to_html(fig),
    )
)

# ROC Curve Comparison
rf = RandomForestClassifier(n_estimators=100, random_state=42)
X = data.drop("churn", axis=1)
y = data["churn"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
rf.fit(X_train, y_train)
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)
log_reg_prob = log_reg.predict_proba(X_test)[:, 1]
rf_prob = rf.predict_proba(X_test)[:, 1]

fig, ax = plt.subplots(figsize=(8, 6))
fpr_lr, tpr_lr, _ = roc_curve(y_test, log_reg_prob)
roc_auc_lr = auc(fpr_lr, tpr_lr)
ax.plot(fpr_lr, tpr_lr, label=f"Logistic Regression (AUC = {roc_auc_lr:.3f})")

fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_prob)
roc_auc_rf = auc(fpr_rf, tpr_rf)
ax.plot(fpr_rf, tpr_rf, label=f"Random Forest (AUC = {roc_auc_rf:.3f})")
ax.plot([0, 1], [0, 1], "k--")
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curve Comparison")
ax.legend(loc="lower right")
figs.append(
    add_section(
        "Model Performance Comparison",
        "The ROC curve compares the performance of Logistic Regression and Random Forest models in predicting customer churn. A higher AUC indicates a better predictive model.",
        mpld3.fig_to_html(fig),
    )
)

# Generate the HTML file
html_content = (
    "<html>"
    "<head>"
    "<title>Customer Churn Analysis Report</title>"
    "<style>"
    "body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding: 40px; }"
    ".container { width: 80%; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); }"
    "h1 { text-align: center; color: #2c3e50; font-size: 28px; margin-bottom: 20px; }"
    ".section { border: 1px solid #ddd; padding: 20px; margin: 20px auto; border-radius: 5px; background: #ffffff; text-align: left; width: 90%; box-shadow: 0px 3px 10px rgba(0,0,0,0.1); }"
    "h2 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 8px; font-size: 22px; margin-bottom: 10px; text-align: center; }"
    "p { font-size: 16px; color: #34495e; line-height: 1.6; text-align: justify; }"
    ".plot-container { text-align: center; margin-top: 10px; }"
    "</style>"
    "</head>"
    "<body>"
    "<div class='container'>"
    "<h1>Customer Churn Analysis Report</h1>"
    f"{''.join(figs)}"
    "</div>"
    "</body>"
    "</html>"
)

with open("customer_churn_analysis.html", "w") as f:
    f.write(html_content)

print("HTML report saved: customer_churn_analysis.html")
