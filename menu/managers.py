from datetime import date, timedelta
from django.db import models

today_date = date.today()
class  MenuQuerySet(models.QuerySet):
  
  def today(self):
    return self.filter(
      date__date=today_date
    )
  
  def today_served(self):
    return self.filter(
      served = True,
      date__date=today_date
    )

  def this_week(self):
    return self.filter(
      date__date__iso_week_day__gte= 1,
      date__date__iso_week_day__lt= 7,
      date__date__month = today_date.month,
      date__date__year = today_date.year,
    )

  def this_week_served(self):
    return self.filter(
      served = True,
      date__date__iso_week_day__gte= 1,
      date__date__iso_week_day__lt= 7,
      date__date__month = today_date.month,
      date__date__year = today_date.year,
    )

  def this_month(self):
    return self.filter(
      date__date__month = today_date.month,
      date__date__year = today_date.year,
    )

  def this_month_served(self):
    return self.filter(
      served = True,
      date__date__month = today_date.month,
      date__date__year = today_date.year,
    )

  def this_year(self):
    return self.filter(
      date__date__year = today_date.year,
    )

  def served(self):
    return self.filter(served = True)
      
      
