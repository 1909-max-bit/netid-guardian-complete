# netid-guardian-complete

# =============================
# NetID Guardian - Run Commands
# =============================

# -----------------------------
# 1. Prerequisites (Linux/Ubuntu)
# -----------------------------
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nmap

# Optional: install Docker if you want the Docker method
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# (Logout/login required after adding yourself to docker group)

# -----------------------------
# 2. Option A: Run locally (venv)
# -----------------------------

# --- Backend ---
cd ~/netid-guardian/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Backend runs on http://0.0.0.0:8000

# --- Agent --- (open new terminal)
cd ~/netid-guardian/agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python agent.py

# Example: run with environment variables
export BACKEND_URL="http://localhost:8000/api/events"
export SCAN_NET="192.168.1.0/24"
python agent.py

# --- Frontend ---
cd ~/netid-guardian/frontend
# Option 1: open index.html in browser directly
# Option 2: serve with python http server
python3 -m http.server 8080
# Then open http://localhost:8080/index.html

# --- Test backend manually ---
curl -X POST http://localhost:8000/api/events   -H "Content-Type: application/json"   -d '{"type":"test","timestamp":'$(date +%s)',"info":"manual test"}'

# -----------------------------
# 3. Option B: Run with Docker Compose
# -----------------------------
cd ~/netid-guardian
docker-compose up --build        # run in foreground
docker-compose up --build -d     # run in background

# Logs
docker-compose logs -f backend
docker-compose logs -f agent

# Stop and clean up
docker-compose down

# -----------------------------
# 4. Useful Notes
# -----------------------------
# - BACKEND_URL = http://localhost:8000/api/events
# - SCAN_NET    = 192.168.1.0/24   (adjust to your LAN)
# - DB_PATH     = sqlite:///db.sqlite3 (default backend DB)
# - Check health: curl http://localhost:8000/api/health
