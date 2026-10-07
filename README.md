# Google Photos - Ask Photos MVP (Graduation Project)

This project is a functional MVP (Minimum Viable Product) demonstrating a next-generation "Memory Search" (Ask Photos) feature for Google Photos. The application allows users to search for photos using natural, conversational language rather than exact keywords.

## 🚀 Features

- **Conversational Memory Search**: Users can type complex, natural queries like *"I remember a birthday dinner with my family at home. There was a cake."*
- **LLM-Powered Extraction**: Uses an LLM (via Groq API) to extract semantic memory cues (people, events, objects, places, time, visual details) from the user's natural language input.
- **Intelligent Ranking Algorithm**: Matches extracted semantic cues against a structured metadata JSON library of 50 photos, intelligently ranking results as **Strong**, **Possible**, or **Weak** matches.
- **Beautiful UI**: A frontend built in React + Vite that accurately replicates the clean, modern aesthetic of Google Photos, complete with dynamic explanation panels for *why* an image matched a query.
- **Photorealistic Demo Library**: A fully populated mock library of 50 real, photorealistic images specifically curated and labeled to support various complex testing scenarios.

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Vanilla CSS with modern Google Photos aesthetics
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python)
- **AI Integration**: Groq API (LLaMA 3) for zero-shot JSON metadata extraction
- **Data**: Static JSON-based mock database (`demo_library.json`)
- **Deployment**: Railway

## 📸 How It Works

1. **User Input**: The user enters a natural language query in the search bar.
2. **Metadata Extraction**: The FastAPI backend sends the prompt to the Groq LLM, which parses the query and returns a structured JSON object detailing the memory cues (`people`, `event`, `objects`, `place`, `visual_details`).
3. **Retrieval & Ranking**: The backend iterates over the 50-photo library. Using strict boundaries and regex matching, it checks the extracted cues against each photo's metadata. 
4. **Scoring**: Photos are scored based on the number of cues matched. If 100% of the cues are found, it is labeled a **Strong match**. If some cues are found but others are missing, it is labeled a **Possible match**.
5. **Presentation**: The frontend renders the photos alongside visual "pills" explaining exactly which memory cues were successfully matched.

## 🏃‍♂️ Running Locally

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file in the `backend/` directory and add your API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Run the FastAPI server:
```bash
python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
```
Create a `.env` file in the `frontend/` directory and point it to the local backend:
```env
VITE_API_BASE_URL=http://localhost:8000
```
Run the Vite development server:
```bash
npm run dev
```
Navigate to `http://localhost:5173` to test the application!

## 🧪 Example Test Queries

The demo library is highly tuned to test edge cases. Try searching for:
- *"I remember a birthday dinner with my family at home. There was a cake."*
- *"I remember a yellow car near the sea, but I don't remember exactly where it was."*
- *"I remember a beach trip with friends around summer, probably near sunset."*
- *"I remember a road trip with friends and a mountain view."*

---
*Built for NextLeap Graduation Project.*