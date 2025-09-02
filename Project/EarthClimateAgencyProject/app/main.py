import os
import pickle
from flask import Blueprint, render_template, request, redirect, send_file, session, url_for, flash
import matplotlib.pyplot as plt
import io
import pandas as pd
import requests

main = Blueprint('main', __name__)

# Load your climate data (make sure to adjust the path)
data = pd.read_csv('static/data/climate_data.csv')

# Load the model (make sure the path is correct)
pickle_file_path = os.path.join('static', 'model', 'model.pkl')
with open(pickle_file_path, 'rb') as file:
    model = pickle.load(file)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page
    if request.method == 'GET':
        return render_template('visualization.html')
    else:
        return render_template('visualization_results.html')

# Route for visualizing single variable
@main.route('/visualization_results', methods=['POST'])
def visualization_results():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page

    variable = request.form['variable']

    # Plot the selected variable
    fig, ax = plt.subplots()
    ax.plot(data['date'], data[variable], label=variable)
    ax.set_xlabel('Date')
    ax.set_ylabel(variable.capitalize())
    ax.legend()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

# Route for correlation matrix
@main.route('/correlation_matrix', methods=['POST'])
def correlation_matrix():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page

    # Compute correlation matrix
    corr = data[['temperature', 'humidity', 'co2_levels']].corr()

    # Plot correlation matrix
    fig, ax = plt.subplots()
    cax = ax.matshow(corr, cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

# Route for multi-variable comparison
@main.route('/multi_variable_comparison', methods=['POST'])
def multi_variable_comparison():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page

    selected_vars = request.form.getlist('variables')

    # Plot the selected variables
    fig, ax = plt.subplots()
    for var in selected_vars:
        ax.plot(data['date'], data[var], label=var)

    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page

    countries = {
       'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'UK': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Glasgow'],
            'India': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
            'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
            'China': ['Beijing', 'Shanghai', 'Shenzhen', 'Guangzhou', 'Chengdu'],
            'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Fukuoka'],
            'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza'],
            'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'],
            'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth'],
            'Mexico': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana'],
            'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo'],
            'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'],
            'Argentina': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata'],
            'Pakistan': ['Karachi', 'Lahore', 'Islamabad', 'Quetta', 'Multan'],
            'Saudi Arabia': ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam'],
            'Turkey': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'],
            'Nigeria': ['Lagos', 'Abuja', 'Kano', 'Ibadan', 'Port Harcourt'],
            'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon'],
            'Indonesia': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bekasi'],
            'Egypt': ['Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said'],
            'Philippines': ['Manila', 'Quezon City', 'Davao City', 'Caloocan', 'Cebu City']
    }

    selected_country = None
    selected_city = None
    prediction = None
    alert_color = "success"

    # API details
    api_key = 'acc49f75c81fdf103fdf717e168be8b1'  # Ensure this is valid
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    if request.method == 'POST':
        selected_country = request.form.get('country')
        selected_city = request.form.get('city')

        if not selected_country or not selected_city:
            flash('Please select both a country and a city.', 'warning')
            return render_template('predict.html', countries=countries)

        # Construct the complete URL with country code
        complete_url = f"{base_url}?q={selected_city},{selected_country}&appid={api_key}&units=metric"
        print(f"Fetching URL: {complete_url}")  # Debug print for the URL
        response = requests.get(complete_url)

        # Check for successful API response
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)  # Print the full API response for debugging
            current_temp = weather_data['main']['temp']  # Get temperature from API response

            # Determine alert color based on the temperature
            if current_temp > 30:
                alert_color = "danger"  # Red for high temperature
            elif current_temp < 20:
                alert_color = "warning"  # Yellow for low temperature
            else:
                alert_color = "success"  # Green for normal temperature

            # Display prediction message
            prediction = f"Current temperature for {selected_city}, {selected_country}: {current_temp:.2f}°C."
            trend = "further increase" if current_temp > 28 else "remain stable"
            prediction += f" The temperature is expected to {trend}."
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")  # Log status code and message
            flash('Failed to fetch temperature data. Please try again.', 'danger')

    return render_template('predict.html', countries=countries, selected_country=selected_country, selected_city=selected_city, prediction=prediction, alert_color=alert_color)
