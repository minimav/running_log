from datetime import datetime, timedelta
import typing as tp

from pydantic import BaseModel

DATE_FORMAT = "%Y-%m-%d"

class Run(BaseModel):
    date: str
    distance_miles: float
    duration_mins: float
    comments: tp.Optional[str] = ""

    def week_label(self):
        date = datetime.strptime(self.date, DATE_FORMAT)
        date -= timedelta(days=date.weekday())
        return date.strftime(DATE_FORMAT)
        
    def month_label(self):
        date = datetime.strptime(self.date, "%Y-%m-%d")
        date -= timedelta(days=date.day)
        return date.strftime(DATE_FORMAT)
