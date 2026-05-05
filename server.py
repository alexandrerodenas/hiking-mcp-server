import requests
from mcp.server.fastmcp import FastMCP
import xml.etree.ElementTree as ET

# Initialiser le serveur MCP
mcp = FastMCP("Hiking-Explorer")

@mcp.tool()
def get_weather_forecast(latitude: float, longitude: float, target_date: str) -> str:
    """Get weather forecast for a specific location and date."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,windspeed_10m_max&timezone=auto&start_date={target_date}&end_date={target_date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('daily', {})
        
        # Open-Meteo returns lists for daily data
        t_max = data.get('temperature_2m_max', [None])[0]
        t_min = data.get('temperature_2m_min', [None])[0]
        w_max = data.get('windspeed_10m_max', [None])[0]
        w_code = data.get('weathercode', [None])[0]
        
        return (f"Weather forecast for {target_date}:\n"
                f"- Max Temp: {t_max}°C\n"
                f"- Min Temp: {t_min}°C\n"
                f"- Max Wind Speed: {w_max} km/h\n"
                f"- Weather Code: {w_code}")
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
