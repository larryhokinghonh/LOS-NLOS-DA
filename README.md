# LOS/NLOS Detection and Analysis

A machine learning project for Line-of-Sight (LOS) and Non-Line-of-Sight (NLOS) detection using Ultra-Wideband (UWB) sensor data.

## Project Overview

This project implements a data pipeline and machine learning models for LOS/NLOS detection using UWB sensor data. The system processes Channel Impulse Response (CIR) data along with first path metrics and noise measurements to classify signal conditions and predict ranging errors.

### Key Features

- Data pipeline with GCP integration
- Advanced feature engineering from UWB sensor data
- Multiple machine learning models for classification and regression
- Comprehensive model evaluation and analysis tools

## Project Structure

```
.
├── data/                  # Data storage and processing
├── models/               # Trained model artifacts
├── notebooks/            # Jupyter notebooks for analysis
├── scripts/              # Processing and utility scripts
├── requirements.txt      # Project dependencies
└── .env                 # Environment configuration
```

## Models

### Classification Models
- Random Forest Classifier
- Support Vector Machine (SVM)

### Regression Models
- Random Forest Regressor
- Gradient Boosting

## Technical Stack

- Python 3.x
- Scientific Computing: NumPy, Pandas
- Machine Learning: scikit-learn
- Visualization: Matplotlib, Seaborn
- Data Processing: SciPy

## Setup and Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure GCP credentials:
   - Place the service account JSON file in the project root
   - Set up environment variables in `.env`

## Current Features

- Data Pipeline:
  - GCP data retrieval
  - Multi-stage data processing
  - Feature engineering
  - Outlier detection
  - Duplicate removal

- Feature Engineering:
  - CIR statistics
  - First path metrics
  - Noise measurements
  - Signal quality indicators

- Analysis Tools:
  - PCA dimensionality reduction
  - Feature importance analysis
  - Model performance evaluation
  - SHAP analysis

## Future Improvements

1. Model Enhancements:
   - Ensemble methods
   - Deep learning (1D CNN, LSTM)
   - Bayesian optimization

2. Feature Engineering:
   - Wavelet transforms
   - Advanced signal processing
   - Domain-specific feature extraction

3. System Optimization:
   - Real-time processing
   - Model monitoring
   - Automated retraining

## Dependencies

Key dependencies include:
- numpy==2.2.3
- pandas==2.2.3
- scikit-learn==1.6.1
- scipy==1.15.2
- matplotlib==3.10.1
- seaborn==0.13.2

For a complete list, see `requirements.txt`.