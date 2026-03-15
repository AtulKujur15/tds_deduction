# Automated TDS Deduction Prediction System

This project is a machine learning based web application that predicts Tax Deducted at Source (TDS) according to Indian Income Tax rules.

The system analyzes transaction details such as payment type, vendor type, PAN availability, and transaction amount to predict the applicable TDS rate and deduction amount.

## Technologies Used

- Python
- Django
- Scikit-learn
- Pandas
- Bootstrap
- SQLite

## Features

- Predict TDS deduction automatically
- PAN-based higher deduction rule
- Lower deduction certificate handling
- Vendor type based deduction logic
- Transaction history stored in database
- Dashboard for prediction statistics

## System Architecture

User Input → Django Web Application → Machine Learning Model → Prediction → Database Storage

## Installation

Clone the repository

git clone https://github.com/yourusername/tds-automation-system

Install dependencies

pip install -r requirements.txt

Run the server

python manage.py runserver