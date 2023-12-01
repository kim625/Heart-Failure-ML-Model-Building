# -*- coding: utf-8 -*-
"""Heart Failure Prediction ML Model Building (Fetal Health Classification)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SEUodLSvQ2ypvETVeQL0ukKI3O1j83Iq

# Heart Failure Prediction ML Model Building (Fetal Health Classification)

---

# Heart Failure Prediction Dataset

Cardiovascular diseases (CVDs) are the number 1 cause of death globally, taking an estimated 17.9 million lives each year, which accounts for 31% of all deaths worldwide.
Heart failure is a common event caused by CVDs and this dataset contains 12 features that can be used to predict mortality by heart failure.

Most cardiovascular diseases can be prevented by addressing behavioural risk factors such as tobacco use, unhealthy diet and obesity, physical inactivity and harmful use of alcohol using population-wide strategies.

People with cardiovascular disease or who are at high cardiovascular risk (due to the presence of one or more risk factors such as hypertension, diabetes, hyperlipidaemia or already established disease) need early detection and management wherein a machine learning model can be of great help.

--------
In this project I worked on EDA (Exploratory Data Analysis). At the end of the notebook, I experimented and built a regression ML model to classify the health of a fetus as Normal, Suspect, or Pathological using CTG data.

## Import Packages and Helper Functions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score

np.random.seed(0)

"""## Load Data into Pandas DataFrame"""

url_file = 'https://raw.githubusercontent.com/gauravjain2/heart-failure-prediction/main/heart_failure_clinical_records_dataset.csv'
data = pd.read_csv(url_file)

data

data.info()

# Generating descriptive statistics
data.describe().T

"""This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features.

Input Features:

- **age** - age of patient
- **anaemia** - Decrease of red blood cells or hemoglobin (boolean)
- **creatinine_phosphokinase** - Level of the CPK enzyme in the blood (mcg/L)
- **diabetes** - If the patient has diabetes (boolean)
- **ejection_fraction** - Percentage of blood leaving the heart at each contraction (percentage)
- **high_blood_pressure** - If the patient has hypertension (boolean)
- **platelets** - Platelets in the blood (kiloplatelets/mL)
- **serum_creatinine** - Level of serum creatinine in the blood (mg/dL)
- **serum_sodium** - Level of serum sodium in the blood (mEq/L)
- **sex** - Woman or man (binary)
- **smoking** - If the patient smokes or not (boolean)
- **time** - Follow-up period (days)


Target Label:

- **DEATH_EVENT** - If the patient deceased during the follow-up period (boolean)
"""

# Evaluating distributions of the features
hist_plot = data.hist(figsize = (20,20), color = "#483D8B")

"""### Creating Heatmap to find the correlation with *DEATH_EVENT*"""

# generate heatmap to display correlations in data using seaborn
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
corr = data.corr()
fig, ax = plt.subplots(figsize=(15, 8))
sns.heatmap(corr, annot=True, cmap="RdPu");

"""---

## Data Preparation

### Data Scaling
"""

data.columns

columns = ['age', 'anaemia', 'creatinine_phosphokinase', 'diabetes',
       'ejection_fraction', 'high_blood_pressure', 'platelets',
       'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time']
scale_X = StandardScaler()
X =  pd.DataFrame(scale_X.fit_transform(data[columns],), columns = columns)

X.head()

y = data["DEATH_EVENT"]
y.head()

"""### Train/Test Split and Cross-Validation"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42, stratify = y)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""---

## Building a Machine Learning Model

### Logistic Regression (LR)
"""

logistic_regression = LogisticRegression()
logistic_regression_model = logistic_regression.fit( X_train , y_train )

# Calculating the mean accuracy from using the model on the given test data X and labels y
print(f"Baseline Logistic Regression: {round(logistic_regression_model.score(X_test, y_test), 3)}")

pred_logistic_regression = logistic_regression_model.predict( X_test )

pred_logistic_regression

print("Classification Report")
print(classification_report( y_test, pred_logistic_regression ))

cv_method = StratifiedKFold(n_splits= 3 , shuffle=True, random_state= 40 )

scores_Logistic = cross_val_score(
    logistic_regression,
    X = X_train ,
    y = y_train ,
    cv = cv_method ,
    n_jobs = 2 ,
    scoring = "accuracy"
    )

print(f"Scores(Cross validate) for Logistic Regression model:\n{scores_Logistic}")
print(f"Cross Validation Means: {round(scores_Logistic.mean(), 3)}")
print(f"Cross Validation Standard Deviation: {round(scores_Logistic.std(), 3)}")

logistic_regression.get_params()

params_LR = {"tol": [0.0001,0.0002,0.0003],
            "C": [0.01, 0.1, 1, 10, 100],
            "intercept_scaling": [1, 2, 3, 4]
            }

GridSearchCV_LR = GridSearchCV(estimator=LogisticRegression(),
                                param_grid= params_LR ,
                                cv= cv_method,
                                verbose=1,
                                n_jobs= 2 ,
                                scoring="accuracy",
                                return_train_score=True
                                )

GridSearchCV_LR.fit( X_train , y_train );

best_estimator_LR = GridSearchCV_LR.best_estimator_
print(f"Best estimator for LR model:\n{best_estimator_LR}")
best_params_LR = GridSearchCV_LR.best_params_
print(f"Best parameter values for LR model:\n{best_params_LR}")

print(f"Best score for LR model: {round(GridSearchCV_LR.best_score_, 3)}")

logistic_regression = LogisticRegression(
    C= 1 ,
    intercept_scaling= 1,
    tol= 0.0001 ,
    random_state=42
    )

logistic_regression_model = logistic_regression.fit( X_train, y_train )
pred_logistic_regression = logistic_regression_model.predict( X_test )

print("Classification Report")
print(classification_report(y_test ,pred_logistic_regression))

"""---"""