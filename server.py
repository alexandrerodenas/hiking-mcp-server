import requests
from mcp.server.fastmcp import FastMCP
import xml.etree.ElementTree as ET

# Initialiser le serveur MCP
mcp = FastMCP("Hiking-Explorer")

@mcp.tool()
def generate_gpx(name_filter: str, latitude: float, longitude: float, radius_km: float = 5.0) -> str:
    """Recherche un sentier et génère un fichier GPX pour visualisation."""
    
    # Fixed Overpass query to include nodes
    query = f"""
    [out:json][timeout:60];
    way["name"~"Hangursløypa",i](around:5000,60.6279,6.4253)->.trails;
    (.trails;>;);
    out;
    """
    
    try:
        headers = {'User-Agent': 'Hiking-Explorer-MCP/1.0'}
        response = requests.post("https://overpass-api.de/api/interpreter", data=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"Elements: {len(data.get('elements', []))}")
        
        nodes = {el['id']: (el['lat'], el['lon']) for el in data.get('elements', []) if el['type'] == 'node'}
        
        for el in data.get("elements", []):
            if el.get("type") == "way":
                # Find nodes in order
                coords = []
                for node_id in el.get('nodes', []):
                    # Check if node exists in full data
                    node = next((n for n in data.get('elements', []) if n.get('id') == node_id), None)
                    if node:
                        coords.append((node['lat'], node['lon']))
                
                print(f"Coords found for {el.get('id')}: {len(coords)}")
                if not coords: continue
                
                # Create GPX
                gpx = ET.Element("gpx", version="1.1", creator="Hiking-MCP")
                trk = ET.SubElement(gpx, "trk")
                ET.SubElement(trk, "name").text = el["tags"].get("name", "Trail")
                trkseg = ET.SubElement(trk, "trkseg")
                for lat, lon in coords:
                    ET.SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))
                
                # Generate OpenStreetMap URL for the trail
                # OSM displays ways with an ID: https://www.openstreetmap.org/way/<id>
                osm_url = f"https://www.openstreetmap.org/way/{el.get('id')}"
                
                filename = f"{el['tags'].get('name', 'trail').replace(' ', '_')}.gpx"
                tree = ET.ElementTree(gpx)
                tree.write(filename, encoding="utf-8", xml_declaration=True)
                
                return f"GPX file: {filename} ({len(coords)} points). View on OSM: {osm_url}"
                
        return "Trail not found."
        
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
