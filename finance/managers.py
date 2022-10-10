from datetime import date, timedelta
from django.db import models

today_date = date.today()
class  OrderPaymentQuerySet(models.QuerySet):
  
  def query_period(self, period, paid_with='cash'):
    if period == 'today':
      return self.today(paid_with)
    elif period == 'week':
      return self.this_week(paid_with)
    elif period == 'month':
      return self.this_month(paid_with)
    elif period == 'year':
      return self.this_year(paid_with)
    elif period == 'all':
      if paid_with is None:
        return self.all()
      return self.filter(paid_with=paid_with,)
    return self.today(paid_with)
  
  def today(self, paid_with='cash'):
    if paid_with is not None:
      if paid_with == 'e_cash':
        return self.filter(paid_with__in=['mtn','voda','bank'], date__date = today_date)
      return self.filter(paid_with=paid_with, date__date = today_date)
    return self.filter(date__date = today_date)

  def this_week(self, paid_with='cash'):
    if paid_with is not None:
      if paid_with == 'e_cash':
        return self.filter(
          paid_with__in=['mtn','voda','bank'],
          date__date__iso_week_day__gte= 1,
          date__date__iso_week_day__lt= 7,
          date__date__month = today_date.month,
          date__date__year = today_date.year,
        )
      return self.filter(
        paid_with=paid_with,
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

  def this_month(self, paid_with='cash'):
    if paid_with is not None:
      if paid_with == 'e_cash':
        return self.filter(
          paid_with__in=['mtn','voda','bank'],
          date__date__month=today_date.month,
          date__date__year=today_date.year,
        )
      return self.filter(
        paid_with=paid_with,
        date__date__month=today_date.month,
        date__date__year=today_date.year,
      )
    return self.filter(
      date__date__month=today_date.month,
      date__date__year=today_date.year,
    )

  def this_year(self, paid_with='cash'):
    if paid_with is not None:
      if paid_with == 'e_cash':
        return self.filter(
          paid_with__in=['mtn','voda','bank'],
          date__date__year = today_date.year)
        
      return self.filter(
        paid_with=paid_with,
        date__date__year = today_date.year)
      
    return self.filter(date__date__year = today_date.year)

