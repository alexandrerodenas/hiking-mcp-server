from mcp.server.fastmcp import FastMCP
import httpx
import asyncio

mcp = FastMCP("HikingAssistant")

@mcp.tool()
async def search_hikes(lat: float, lon: float, radius: int = 5000) -> list:
    """Cherche les sentiers de randonnée autour de coordonnées données."""
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (way["route"="hiking"](around:{radius},{lat},{lon}););
    out geom;
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(overpass_url, data=query, headers={"User-Agent": "HikingAssistant/1.0"})
        data = response.json()
        return [{"id": w.get("id"), "tags": w.get("tags")} for w in data.get("elements", [])]

@mcp.tool()
async def get_weather_forecast(lat: float, lon: float, target_date: str) -> dict:
    """Retourne les prévisions météo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,weather_code&timezone=auto&start_date={target_date}&end_date={target_date}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@mcp.tool()
async def get_nearby_pois(lat: float, lon: float, radius_m: int = 1000) -> list:
    """Cherche des points d'intérêt (viewpoint, shelter, fast_food)."""
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
        nwr["tourism"="viewpoint"](around:{radius_m},{lat},{lon});
        nwr["amenity"="shelter"](around:{radius_m},{lat},{lon});
        nwr["amenity"="fast_food"](around:{radius_m},{lat},{lon});
    );
    out;
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(overpass_url, data=query, headers={"User-Agent": "HikingAssistant/1.0"})
        data = response.json()
        return [{"type": e.get("tags", {}).get("amenity") or e.get("tags", {}).get("tourism"), "name": e.get("tags", {}).get("name")} for e in data.get("elements", [])]

if __name__ == "__main__":
    mcp.run()
