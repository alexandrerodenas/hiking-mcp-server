import requests
from mcp.server.fastmcp import FastMCP

# Initialiser le serveur MCP
mcp = FastMCP("Hiking-Explorer")

@mcp.tool()
def search_hikes(latitude: float, longitude: float, radius_km: float = 5.0, name_filter: str = None) -> str:
    """Search for hiking trails, with optional name filtering."""
    # Reduced query scope: restrict highway to path or track, 
    # and use a slightly smaller radius to avoid timeouts in dense areas.
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"path|track"](around:{radius_km * 500},{latitude},{longitude});
    );
    out tags;
    >;
    out skel qt;
    """
    
    # Return simplified GeoJSON-like path data
    # (Extracting coordinates for each path)
    
    try:
        headers = {'User-Agent': 'Hiking-Explorer-MCP/1.0'}
        response = requests.post("https://overpass-api.de/api/interpreter", data=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # We need to map nodes to coordinates
        nodes = {el['id']: (el['lat'], el['lon']) for el in data.get('elements', []) if el['type'] == 'node'}
        
        hikes = []
        for el in data.get("elements", []):
            if el.get("type") == "way" and "tags" in el:
                tags = el["tags"]
                name = tags.get("name", "Unnamed trail")
                if name_filter and name_filter.lower() not in name.lower(): continue
                
                # Get coordinates
                coords = [nodes.get(node_id) for node_id in el.get('nodes', []) if node_id in nodes]
                
                difficulty = tags.get("sac_scale", "unknown")
                hikes.append(f"- {name} (Diff: {difficulty}) | Nodes: {len(coords)} | Coords: {coords[:2]}...")
                if len(hikes) >= 10: break
        
        return "Trails found (copy coordinates for map plotting):\n" + "\n".join(hikes)

        
    except Exception as e:
        return f"Error during Overpass request: {str(e)}"

if __name__ == "__main__":
    mcp.run()
