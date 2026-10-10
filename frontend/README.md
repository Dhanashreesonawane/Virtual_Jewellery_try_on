# Aurelia — frontend
React + Vite UI for the FastAPI virtual jewellery try-on backend. All detection and rendering happen in the backend.

## Setup
    cp .env.example .env     # set VITE_API_BASE_URL (default http://localhost:8000)
    npm install
    npm run dev              # http://localhost:5173

Start the backend first (see ../backend/README.md) with `CORS_ORIGINS=http://localhost:5173`.
Camera access needs `localhost` or HTTPS. Live camera streams frames over WebSocket (/ws/tryon) and shows the processed frames; image upload uses POST /api/tryon/image.
