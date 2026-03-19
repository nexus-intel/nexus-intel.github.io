# Deploying your Nexus AI Backend

If you don't want to use a credit card, **Hugging Face Spaces** is your best bet.

## Option 1: Hugging Face Spaces (No Credit Card Required)
1. Sign up at [huggingface.co](https://huggingface.co).
2. Click **New Space**.
3. Name it and select **Docker** as the SDK.
4. Choose the **Blank** template.
5. In the **Settings** tab, add your `GEMINI_API_KEY` to the **Variables and Secrets** section.
6. Upload your files (or connect your GitHub repo) into the Space.
7. Your app will run automatically!

## Option 2: Render (Requires Card for Verification)
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
