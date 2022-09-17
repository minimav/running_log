from collections import defaultdict
import datetime as dt
import os
import typing as tp

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db import NoRunError, RunningDatabase
from models import Run


tags_metadata = [{"name": "runs", "description": "Operations on runs"}]

app = FastAPI(openapi_tags=tags_metadata)

origins = ["http://localhost:5000", "localhost:5000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/recent_runs", tags=["runs"])
async def get_recent_runs(num_days: tp.Optional[int] = 7) -> dict:
    """Get runs in the last n days."""
    today = dt.date.today()
    start_date = today - dt.timedelta(days=num_days - 1)
    runs_in_last_week = db.get_runs_in_date_range(start_date=start_date, end_date=today)

    last_week = [
        (start_date + dt.timedelta(days=days)).strftime("%Y-%m-%d")
        for days in range(num_days)
    ]
    recent_runs = []
    for day in last_week:
        try:
            recent_runs.append(runs_in_last_week[day].dict())
        except KeyError:
            recent_runs.append({"date": day})
    return recent_runs


@app.post("/run", tags=["runs"])
async def add_run(run: Run) -> dict:
    """Add a run to the database."""
    success = db.store_run(run)
    if success:
        return {"data": f"Run {run} added :)"}
    else:
        raise HTTPException(
            status_code=409, detail=f"Could not store run {run} due to duplicate date."
        )


@app.get("/run", tags=["runs"])
async def get_run(date: str) -> dict:
    """Delete a run for a specific date."""
    try:
        run = db.get_run_on_date(date)
        return {"data": run.dict()}
    except NoRunError as e:
        return HTTPException(status_code=404, detail=e.message)


@app.get("/runs", tags=["runs"])
async def get_runs(
    time_unit: str,
    start_date: tp.Optional[str] = None,
    end_date: tp.Optional[str] = None,
) -> list:
    """Get runs between two dates."""
    valid_time_units = {"monthly", "weekly"}
    if time_unit not in valid_time_units:
        return HTTPException(
            status_code=404,
            detail=f"time_unit={time_unit} was not in {valid_time_units}",
        )

    runs = db.get_runs_in_date_range(start_date=start_date, end_date=end_date).values()

    distances_per_label = defaultdict(float)
    for run in runs:
        label = run.week_label() if time_unit == "weekly" else run.month_label()
        distances_per_label[label] += run.distance_miles

    return [{"x": x, "y": y} for x, y in distances_per_label.items()]


@app.get("/delete_run", tags=["runs"])
async def delete_run(date: str) -> dict:
    """Delete a run for a specific date."""
    db.delete_run_on_date(date)
    return {"data": f"Run on {date} deleted :)"}


def populate_with_existing_runs(db: RunningDatabase):
    """Insert existing runs from a file into the database."""
    if not os.path.exists("existing_runs.txt"):
        return

    with open("existing_runs.txt", "r") as f:
        for line in f.readlines():
            date, distance_miles, duration_mins, *additional = line.split(",")
            try:
                comments = additional[0]
            except IndexError:
                comments = ""
            distance_miles = float(distance_miles)
            duration_mins = float(duration_mins)
            run = Run(
                date=date,
                distance_miles=distance_miles,
                duration_mins=duration_mins,
                comments=comments,
            )
            db.store_run(run)

if __name__ == "__main__":
    db = RunningDatabase()
    if db.exists():
        db.clean()

    db.create()
    
    populate_with_existing_runs(db)

    uvicorn.run(app, host="0.0.0.0", port=8080)
