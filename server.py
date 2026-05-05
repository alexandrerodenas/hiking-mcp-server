import requests
from mcp.server.fastmcp import FastMCP

# Initialiser le serveur MCP
mcp = FastMCP("Hiking-Explorer")

@mcp.tool()
def search_hikes(latitude: float, longitude: float, radius_km: float = 5.0, name_filter: str = None) -> str:
    """Search for hiking trails, with optional name filtering."""
    
    # ... (query remains the same)
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"path|footway|track"](around:{radius_km * 1000},{latitude},{longitude});
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        headers = {'User-Agent': 'Hiking-Explorer-MCP/1.0'}
        response = requests.post("https://overpass-api.de/api/interpreter", data=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        elements = data.get("elements", [])
        hikes = []
        for el in elements:
            if el.get("type") == "way" and "tags" in el:
                tags = el["tags"]
                name = tags.get("name", "Unnamed trail")
                
                # Filter by name if specified
                if name_filter and name_filter.lower() not in name.lower():
                    continue
                
                hikes.append(f"- {name}")
                if len(hikes) >= 15: break
        
        if not hikes:
            return "No trails found (check your filters)."
        return "Trails found:\n" + "\n".join(hikes)
        
    except Exception as e:
        return f"Error during Overpass request: {str(e)}"

if __name__ == "__main__":
    mcp.run()
