# Deploying your Nexus AI Backend

Since GitHub Pages only hosts static content (HTML/CSS/JS), your Python backend needs a separate home. Here are the best free-tier options:

## Option 1: Render (Recommended)
1. Sign up at [render.com](https://render.com).
2. Click **New + > Web Service**.
3. Connect your GitHub repository.
4. Set the following:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py` (or `uvicorn app:app --host 0.0.0.0 --port $PORT`)
5. Add **Environment Variables**:
   - `GEMINI_API_KEY`: Your Google AI Key.

## Option 2: Railway
1. Sign up at [railway.app](https://railway.app).
2. Click **New Project > Deploy from GitHub**.
3. It will automatically detect the Python environment.
4. Set the `GEMINI_API_KEY` in the Variables tab.

## Important Note: Update Frontend
Once your backend is deployed, you will get a URL like `https://nexus-backend.onrender.com`.
Update the `fetch` calls in your `script.js` to point to this new URL instead of `localhost:8000`.

```javascript
// Change this in script.js:
const response = await fetch(`https://your-backend-url.com/chat`, { ... });
```
