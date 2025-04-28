from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'dev'

# Sample financial data structure
financial_data = {
    'income': [],
    'expenses': [],
    'savings': [],
    'investments': [],
    'debts': []
}

@app.route('/')
def dashboard():
    # Calculate financial health metrics
    total_income = sum(item['amount'] for item in financial_data['income'])
    total_expenses = sum(item['amount'] for item in financial_data['expenses'])
    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
    
    # Create visualizations
    expense_categories = {}
    for expense in financial_data['expenses']:
        category = expense['category']
        expense_categories[category] = expense_categories.get(category, 0) + expense['amount']
    
    # Create Plotly pie chart
    if expense_categories:
        fig = px.pie(
            values=list(expense_categories.values()),
            names=list(expense_categories.keys()),
            title='Expense Breakdown'
        )
        expense_chart = fig.to_html(full_html=False)
    else:
        expense_chart = None
    
    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expenses=total_expenses,
        savings_rate=savings_rate,
        expense_chart=expense_chart
    )

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_type = request.form.get('type')
    amount = float(request.form.get('amount'))
    category = request.form.get('category')
    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    
    transaction = {
        'amount': amount,
        'category': category,
        'date': date
    }
    
    financial_data[transaction_type].append(transaction)
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True) 