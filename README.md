# car-price-prediction

# 🚗 Car Price Prediction System

A complete end-to-end **Machine Learning** project that predicts the resale price of used cars based on key vehicle attributes. The project includes a **Jupyter Notebook** for model training, a **Tkinter Desktop App**, and a **Flask Web Application** for real-time predictions.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## 📖 Overview

This project uses a **Random Forest Regressor** trained on a real-world used cars dataset to predict vehicle resale prices. It covers the **complete ML lifecycle** — from raw data cleaning and EDA to model training, evaluation, and deployment through two interfaces: a desktop GUI and a web app.

---

## ✨ Features

- 🔍 **Exploratory Data Analysis (EDA)** with visualizations using Matplotlib, Seaborn & Plotly
- 🧹 **Data Preprocessing** — null handling, outlier removal, feature engineering
- 🤖 **Random Forest Regressor** for accurate price prediction
- 📦 **Model serialization** with Pickle for reusable deployment
- 🖥️ **Tkinter Desktop App** — clean GUI with input validation, activity log & progress bar
- 🌐 **Flask Web App** — REST API with session-based prediction history
- 💰 Price output formatted in **Lakhs / Crores** for Indian market

---

## 🛠️ Tech Stack

| Category | Tools / Libraries |
|---|---|
| Language | Python 3.x |
| ML & Data | Scikit-learn, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Desktop App | Tkinter (ttk) |
| Web App | Flask |
| Database | SQLAlchemy, PyMySQL |
| Model Storage | Pickle |
| Environment | Jupyter Notebook |

---

## 📁 Project Structure

```
car-price-prediction/
│
├── main.ipynb                  # EDA, preprocessing, model training & evaluation
├── car_price_app.py            # Tkinter Desktop Application
├── web_app.py                  # Flask Web Application
├── requirements.txt            # All dependencies
│
├── saved_models/
│   └── RandomForestRegressor.pkl   # Trained ML model
│
├── saved_scaling/
│   └── scaler.pkl                  # Fitted StandardScaler
│
├── templates/
│   └── index.html                  # HTML template for Flask app
│
└── dataset/
    ├── cars_dataset.csv            # Raw dataset
    └── cleaned_cars_dataset.csv    # Preprocessed dataset
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/car-price-prediction.git
cd car-price-prediction
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the Desktop App (Tkinter)
```bash
python car_price_app.py
```

### Run the Web App (Flask)
```bash
python web_app.py
```
Then open your browser and go to: `http://127.0.0.1:5000`

### Run the Notebook
```bash
jupyter notebook main.ipynb
```

---

## 🤖 Model Details

| Parameter | Detail |
|---|---|
| Algorithm | Random Forest Regressor |
| Input Features | 16 (after encoding) |
| Encoding | One-Hot Encoding (Seller, Fuel, Transmission) |
| Scaling | StandardScaler |
| Output | Predicted resale price (₹) |

**Input Features:**

| Feature | Type |
|---|---|
| Vehicle Age | Numerical |
| KM Driven | Numerical |
| Mileage (kmpl) | Numerical |
| Engine (cc) | Numerical |
| Max Power (bhp) | Numerical |
| Seats | Numerical |
| Seller Type | Categorical (Dealer / Individual / Trustmark Dealer) |
| Fuel Type | Categorical (CNG / Diesel / Electric / LPG / Petrol) |
| Transmission | Categorical (Automatic / Manual) |

---

## 🔮 Future Improvements

- [ ] Add more ML models (XGBoost, LightGBM) with comparison
- [ ] Deploy Flask app on **Render / Railway / AWS**
- [ ] Add **car brand & model** as input features
- [ ] Build a **React or Streamlit** frontend for better UI
- [ ] Add **CI/CD pipeline** with GitHub Actions

---

## 🙋‍♂️ Author

**Your Name**
- GitHub:(https://github.com/Adityagupta9975)
- LinkedIn:(www.linkedin.com/in/aditya-gupta-7b186a269)

---

> ⭐ If you found this project helpful, consider giving it a star!
