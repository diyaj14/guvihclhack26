# How to Run the Vigilante AI Project

This project consists of a **Next.js frontend** and a **FastAPI backend**.

## Prerequisites
- Node.js (v18+)
- Python (3.9+)
- A Groq API Key (Get it from [console.groq.com](https://console.groq.com/))

---

## 🚀 1. Setup Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create or update your `.env` file in this directory:
   ```bash
   # d:/GITHUB/guvihclhack26/DJ/guvihack-main/backend/.env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server **from within the /backend folder**:
   ```bash
   uvicorn main:app --reload
   ```
   *The backend will be available at `http://127.0.0.1:8000`*

---

## 🌐 2. Setup Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The website will be available at `http://localhost:3000`*

---

## 🛠️ Tech Stack
- **Frontend**: Next.js 15, React 19, Tailwind CSS 4, Lucide React.
- **Backend**: FastAPI, Groq LLM (Llama 3.3 70B), Pydantic.

---

## 🔍 Troubleshooting: "Stuck on AI Analyzing"

If the dashboard is stuck at "AI analyzing...", follow these steps:

1. **Check Browser Console**:
   - Right-click the dashboard -> **Inspect** -> **Console**.
   - Look for red errors like `ERR_CONNECTION_REFUSED` or `CORS Error`.
   - If you see a CORS error, ensure `main.py` has the allow_origins=["*"] setting.

2. **Check Backend Terminal**:
   - Look for lines starting with `DEBUG: [INCOMING]`. 
   - If you **DO NOT** see these lines after sending a message, the request is not leaving your browser.
   - If you **DO** see them but it hangs, check your `GROQ_API_KEY` in `.env`.

3. **Verify API URL**:
   - Open `http://127.0.0.1:8000/` in your browser. You should see `{"status": "Vigilante AI Module 1 Operational"}`.
