from uuid import uuid4
import plotly.graph_objects as go
import os 
import httpx
import asyncio
async def create_plot(city, interval):
    try:
        # Async get data from API
        async with httpx.AsyncClient() as client:
            response = await client.get('http://api:5000/get_weather', 
                params={
                    'city': city,
                    'interval': interval
                }, timeout=15)
            
            if response.status_code != 200:
                raise Exception('Проблемы с AccuWeather: ' + str(response.json())) 
            else:
                data = response.json()
                forecasts = data['weather']

        # Extract data
        dates = [forecast['date'] for forecast in forecasts]
        max_temps = [forecast['max_temp'] for forecast in forecasts]
        min_temps = [forecast['min_temp'] for forecast in forecasts]
        humidities = [forecast['humidity'] for forecast in forecasts]
        wind_speeds = [forecast['wind_speed'] for forecast in forecasts]
        rain_probabilities = [forecast['rain_probability'] for forecast in forecasts]
        
        # Create a plotly figure
        fig = go.Figure()

        # Add temperature
        fig.add_trace(go.Scatter(x=dates, y=max_temps, mode='lines+markers', name='Max Temp (°C)', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=dates, y=min_temps, mode='lines+markers', name='Min Temp (°C)', line=dict(color='blue')))

        # Add humidity, wind speed, rain probability as bar traces
        fig.add_trace(go.Bar(x=dates, y=humidities, name='Humidity (%)', marker_color='rgba(0, 128, 255, 0.6)'))
        fig.add_trace(go.Bar(x=dates, y=wind_speeds, name='Wind Speed (km/h)', marker_color='rgba(128, 0, 255, 0.6)'))
        fig.add_trace(go.Bar(x=dates, y=rain_probabilities, name='Rain Probability (%)', marker_color='rgba(0, 255, 128, 0.6)'))

        # Update layout
        fig.update_layout(
            title=f"{len(forecasts)}-Day Weather Forecast for {city}",
            xaxis_title="Date",
            yaxis_title="Value",
            barmode='group',
            template="plotly_white",
            legend=dict(x=0.02, y=1.0, bgcolor="rgba(255,255,255,0.8)"),
        )

        file_path = f"/tmp/weather_forecast_{str(uuid4())}.png"
        fig.write_image(file_path)
        return file_path
    except Exception as e:
        raise Exception('Проблемы с подключением к API: ' + str(e))