"""
Mortgage Calculator - Calculate the monthly payments of a fixed term mortgage over given Nth terms at a given interest
rate. Also figure out how long it will take the user to pay back the loan. For added complexity, add an option for
users to select the compounding interval (Monthly, Weekly, Daily, Continually).
"""


def run():
  rate = float(input('Enter yearly interest rate in percent: '))
  year = int(input('Enter number of terms in year: '))
  principle = float(input('Enter principle: '))

  if rate <= 0.0 or year <= 0 or principle <= 0.0:
    print('Invalid input. quit')
    return

  # see https://www.wikihow.com/Calculate-Mortgage-Payments
  month_rate = (rate / 100) / 12
  factor = (1 + month_rate) ** (year * 12)
  monthly_payment = principle * month_rate * factor / (factor - 1.0)
  print('monthly payment: {}'.format(monthly_payment))


if __name__ == '__main__':
  run()
