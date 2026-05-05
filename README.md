# Hiking MCP Server

An autonomous Model Context Protocol (MCP) server to search for hiking trails via the Overpass API (OpenStreetMap).

## Features
- Search for trails by coordinates (lat, lon).
- Optional name filtering.
- Uses Overpass API for real-time data.

## Installation

1. Clone the repo: `git clone https://github.com/alexandrerodenas/hiking-mcp-server`
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install mcp requests`

## Usage
Launch the server using the MCP SDK.

```bash
python server.py
```
