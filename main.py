from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from ekadashi import is_ekadashi, get_ekadashi_dates, next_ekadashi

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Ekadashi API running"}


@app.get("/today")
def today():

    today = datetime.now()

    return {
        "date": today.strftime("%Y-%m-%d"),
        "is_ekadashi": is_ekadashi(today)
    }


@app.get("/tomorrow")
def tomorrow():

    tomorrow_date = datetime.now() + timedelta(days=1)

    return {
        "date": tomorrow_date.strftime("%Y-%m-%d"),
        "is_ekadashi": is_ekadashi(tomorrow_date)
    }


@app.get("/year/{year}")
def ekadashi_year(year: int):

    dates = get_ekadashi_dates(year)

    return {
        "year": year,
        "total": len(dates),
        "dates": dates
    }


@app.get("/next")
def next_ek():
    return next_ekadashi()


@app.get("/check/{date}")
def check_date(date: str):

    try:

        dt = datetime.strptime(date, "%Y-%m-%d")

        return {
            "date": date,
            "is_ekadashi": is_ekadashi(dt)
        }

    except ValueError:

        return {
            "error": "Invalid date format. Use YYYY-MM-DD"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)