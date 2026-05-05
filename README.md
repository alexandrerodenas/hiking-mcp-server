# Hiking MCP Server

An autonomous Model Context Protocol (MCP) server to search for hiking trails and plan trips with weather forecasts.

## Features
- **Trail Search**: Search for hiking trails via OpenStreetMap (Overpass API).
- **GPX Generation**: Generate GPX files for any trail to visualize in your favorite map app.
- **Weather Forecasts**: Get weather predictions (Temp, Wind, Conditions) using Open-Meteo for any location and date.
- **Direct Links**: Direct OpenStreetMap links for every trail.

## Installation

1. Clone the repo: `git clone https://github.com/alexandrerodenas/hiking-mcp-server`
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install mcp requests`

## Usage
Launch the server using the MCP SDK:

```bash
python server.py
```

### Available Tools
- `generate_gpx(name_filter, latitude, longitude, radius_km)`: Find a trail and generate a GPX file.
- `get_weather_forecast(latitude, longitude, target_date)`: Get weather details for a planned hike.
