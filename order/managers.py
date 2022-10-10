from datetime import date, timedelta
from django.db import models

today_date = date.today()
class  OrderQuerySet(models.QuerySet):
  
  def query_period(self, period, served=False):
    if period == 'today':
      return self.today(served)
    elif period == 'week':
      return self.this_week(served)
    elif period == 'month':
      return self.this_month(served)
    elif period == 'year':
      return self.this_year(served)
    elif period == 'all':
      if served is None:
        return self.all()
      return self.filter(served=served,)
    
    return self.today(served)
  
  def today(self, served=False):
    if served is not None:
      return self.filter(served=served, date__date = today_date)
    return self.filter(date__date = today_date)

  def this_week(self, served=False):
    if served is not None:
      return self.filter(
        served=served,
        date__date__iso_week_day__gte= 1,
        date__date__iso_week_day__lt= 7,
        date__date__month = today_date.month,
        date__date__year = today_date.year,
      )
    return self.filter(
      date__date__iso_week_day__gte= 1,
      date__date__iso_week_day__lt= 7,
      date__date__month = today_date.month,
      date__date__year = today_date.year,
    )

  def this_month(self, served=False):
    if served is not None:
      return self.filter(
        served=served,
        date__date__month=today_date.month,
        date__date__year=today_date.year,
      )
    return self.filter(
      date__date__month=today_date.month,
      date__date__year=today_date.year,
    )

  def this_year(self, served=False):
    if served is not None:
      return self.filter(served=served, date__date__year = today_date.year)
    return self.filter(date__date__year = today_date.year)

