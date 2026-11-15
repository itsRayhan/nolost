# Nolost maps — Django Pathfinding Visualizer

A Django web application that integrates the **Google Maps JavaScript API** with classic graph pathfinding algorithms (**A\***, **Dijkstra**, **BFS**, and **DFS**) to compute, visualize, and compare routes between locations on an interactive map.

---

## Features

- **Interactive Map Visualization**: Displays a 12-node manual graph (`Node A` through `Node L`) across Dhaka with gray graph edges (`Graph Connections`) and a highlighted blue optimal path (`Calculated Route`).
- **4 Pathfinding Algorithms**:
  - **A\* Search**: Uses Haversine straight-line distance as an admissible heuristic for fast shortest-path routing.
  - **Dijkstra's Algorithm**: Guarantees the shortest weighted path distance in kilometers.
  - **Breadth-First Search (BFS)**: Finds the path with the fewest hops/intersections.
  - **Depth-First Search (DFS)**: Explores deep paths first for behavioral comparison.
- **Performance Comparison Table**: Compares route sequence, hop count, total distance (km), nodes explored, and execution time (ms) across all four algorithms side by side.
- **Production Ready for Render + Custom Domain**: Pre-configured with `gunicorn`, `whitenoise`, `build.sh`, and `render.yaml`.

---

## Project Structure

```text
nolost-maps/
├── manage.py
├── requirements.txt
├── build.sh
├── render.yaml
├── .env.example
├── .gitignore
├── README.md
├── nolost_maps/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── pathfinder/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── graph_data.py       # 12 manual nodes + weighted edges (Haversine distance)
    ├── algorithms.py       # A*, Dijkstra, BFS, DFS + performance metrics
    ├── views.py            # Main page view & JSON pathfinding API
    ├── urls.py
    ├── tests.py
    ├── static/
    │   └── pathfinder/
    │       ├── css/style.css
    │       └── js/map.js
    └── templates/
        └── pathfinder/
            └── index.html
```

---

## 1. Local Setup in VS Code

1. **Extract the ZIP file** and open the folder in **VS Code**.
2. Open the VS Code integrated terminal (`Ctrl + ~`) and create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows (PowerShell / CMD):**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create your `.env` file from `.env.example`:
   - **Windows:** `copy .env.example .env`
   - **macOS / Linux:** `cp .env.example .env`
6. Open `.env` and paste your **Google Maps JavaScript API Key**:
   ```env
   GOOGLE_MAPS_API_KEY=AIzaSyYourActualGoogleMapsApiKeyHere
   ```
   *(Note: Even before adding your API key, the app runs in fallback preview mode so you can test everything immediately.)*
7. Run migrations and start the development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
8. Open **http://127.0.0.1:8000/** in your browser.

---

## 2. How to Get a Google Maps JavaScript API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `Nolost Maps`).
3. Navigate to **APIs & Services → Library**, search for **Maps JavaScript API**, and click **Enable**.
4. Go to **APIs & Services → Credentials → Create Credentials → API key**.
5. Copy the generated key into your `.env` file (and later into Render's Environment Variables).

---

## 3. Push to GitHub

1. Initialize a Git repository in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Nolost maps Django pathfinding app"
   ```
2. Create a new repository on [GitHub](https://github.com/new) (e.g., `nolost-maps`).
3. Link and push your code:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/nolost-maps.git
   git push -u origin main
   ```

---

## 4. Deploy Publicly on Render & Connect Your Personal Domain

1. Log in to [Render](https://render.com/) and click **New + → Web Service**.
2. Connect your GitHub repository (`nolost-maps`).
3. Render will automatically detect `render.yaml` (or set these values manually):
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn nolost_maps.wsgi:application`
4. Under **Environment Variables**, add:
   - `GOOGLE_MAPS_API_KEY` = `your_google_maps_api_key`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*`
5. Click **Create Web Service** and wait ~2 minutes for the build to finish.
6. **Connect Your Personal Domain:**
   - In your Render service dashboard, go to **Settings → Custom Domains → Add Custom Domain**.
   - Enter your personal domain (e.g., `maps.yourdomain.com` or `yourdomain.com`).
   - Add the `CNAME` or `A` record shown by Render into your domain registrar's DNS settings (Namecheap, Cloudflare, GoDaddy, etc.).
   - Render automatically provisions a free SSL/HTTPS certificate once DNS propagates.
