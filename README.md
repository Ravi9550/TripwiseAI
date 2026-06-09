# TripwiseAI

TripwiseAI is a Streamlit-based multi-agent travel planner. Users can register, log in, generate trip plans, and manage their own trip history. LangGraph coordinates specialized agents for flights, hotels, itinerary creation, and the final response.

## Features

- Login and registration with password hashing
- Per-user trip history stored in PostgreSQL
- Rename and delete saved trips
- LangGraph multi-agent workflow
- Groq LLaMA model integration
- Tavily hotel/web search
- AviationStack flight lookup
- PostgreSQL checkpoint memory for LangGraph

## App Flow

```mermaid
flowchart TD
    A[User opens Streamlit app] --> B{Logged in?}
    B -- No --> C[Login / Register page]
    C --> D[Create or verify user in PostgreSQL]
    D --> E[Travel planner home]
    B -- Yes --> E

    E --> F[User enters trip request]
    F --> G[LangGraph workflow starts]
    G --> H[Flight Agent]
    H --> I[Hotel Agent]
    I --> J[Itinerary Agent]
    J --> K[Final Agent]
    K --> L[Final travel plan shown]
    L --> M[Trip saved to PostgreSQL]
    M --> N[User history sidebar]

    N --> O{History action}
    O --> P[Rename trip]
    O --> Q[Delete trip]
```

## Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain
- Groq
- PostgreSQL
- Psycopg
- Tavily
- AviationStack

## Environment Variables

Create these in your deployment platform. For local development, put them in `.env`.

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

`DATABASE_URL` is used for both LangGraph checkpoint memory and app data such as users and trip history.

## Local Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run frontend.py
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run frontend.py
```

## Project Structure

```text
TripWiseAi/
  auth.py
  db_utils.py
  frontend.py
  main.py
  requirements.txt
  tools/
    flight_tool.py
    tavily_tool.py
    recommendations.py
```

## Deployment Entry Point

Use this as the app entry file:

```text
frontend.py
```

## Notes

- Do not commit `.env`.
- Do not commit `venv/`.
- Do not commit local `.db` files.
- Make sure your deployed PostgreSQL database allows external connections from your hosting provider.
