# Hiking MCP Server

Un serveur MCP (Model Context Protocol) autonome pour rechercher des sentiers de randonnée via l'API Overpass (OpenStreetMap).

## Fonctionnalités
- Recherche de sentiers par coordonnées (lat, lon).
- Filtrage par nom optionnel.
- Utilisation de l'API Overpass pour des données en temps réel.

## Installation

1. Cloner le repo : `git clone https://github.com/alexandrerodenas/hiking-mcp-server`
2. Créer l'environnement : `python3 -m venv venv && source venv/bin/activate`
3. Installer les dépendances : `pip install mcp requests`

## Utilisation
Lance le serveur via le SDK MCP.

```bash
python server.py
```
