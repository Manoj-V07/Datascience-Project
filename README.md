# Disaster Relief Resource Allocation Analytics

**"Right Resource. Right Place. Right Time."**

## Project Overview
This project aims to analyze disaster-affected regions, predict relief-resource demand, prioritize affected zones, and eventually optimize the allocation of limited resources. It features a full-stack dashboard powered by machine learning models to assist in real-time disaster management and resource allocation.

## Tech Stack
- **Frontend**: Next.js, React, Tailwind CSS, Recharts (Charts), React-Leaflet (Maps)
- **Backend**: FastAPI (Python), Pandas, Scikit-Learn
- **Machine Learning**: Predictive models for demand forecasting (Food, Water, Medical Kits, Shelter).

## Project Structure
- `frontend/`: Next.js web application for the interactive dashboard.
- `backend/`: FastAPI server providing API endpoints and ML model predictions.
- `data/`: Raw and processed datasets.
- `notebooks/`: Exploratory Data Analysis (EDA) and model prototyping.
- `src/`: Source code for data preprocessing and validation.
- `models/`: Trained machine learning models (e.g., Phase 3 demand models).
- `outputs/`: Generated predictions and resource allocation outputs (Phases 3 and 4).
- `reports/`: Phase analysis reports.

## How to Run Locally

### 1. Backend (FastAPI)
Navigate to the root directory and install dependencies:
```bash
pip install -r requirements.txt
```
Then start the backend server:
```bash
cd backend
python main.py
```
*The API will be available at http://localhost:8000*

### 2. Frontend (Next.js)
Open a new terminal, navigate to the `frontend` directory, and install dependencies:
```bash
cd frontend
npm install
```
Start the development server:
```bash
npm run dev
```
*The dashboard will be available at http://localhost:3000*

## Project Phases
- **Phase 1 (Data Foundation)**: Established and audited. Identified target leakage in Priority_Score and added temporal tracking to inventory.
- **Phase 2 (Zone Assessment)**: Evaluated disaster severity, infrastructure damage, and priority scoring.
- **Phase 3 (Demand Prediction)**: Trained ML models to predict the exact quantities of required resources.
- **Phase 4 (Resource Allocation)**: Optimized the distribution of limited inventory to prioritize the most critical zones based on real-time data.