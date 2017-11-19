"""
Unit Converter (temp, currency, volume, mass and more) - Converts various units between one another. The user enters
the type of unit being entered, the type of unit they want to convert to and then the value. The program will then
make the conversion.
"""

from enum import Enum


class TempUnit(Enum):
  CELSIUS = 1
  KELVIN = 2
  FAHRENHEIT = 3

  @classmethod
  def fromstring(cls, str):
    return getattr(cls, str.upper(), None)


class Temp:
  def __init__(self, val, unit):
    self.val = val
    self.unit = unit

  def ConvertToCelsius(self):
    if self.unit == TempUnit.CELSIUS:
      return
    elif self.unit == TempUnit.KELVIN:
      self.val -= 273.15
      self.unit = TempUnit.CELSIUS
    elif self.unit == TempUnit.FAHRENHEIT:
      self.val = (self.val * 1.8 + 32.0)
      self.unit = TempUnit.CELSIUS
    else:
      raise Exception('Unknown temp unit {}'.format(self.unit))

  def __str__(self):
    val_in_kelvin = self.val + 273.15
    val_in_fahrenheit = self.val * 9.0 / 5.0 + 32.0
    return '{} celsius = {} kelvin = {} fahrenheit.\n\n'.format(self.val, val_in_kelvin, val_in_fahrenheit)


def ConvertTemp():
  val_from = float(input('Enter value: '))
  unit_from = TempUnit.fromstring(input('Enter from unit (Celsius, Kelvin, Fahrenheit): '))
  cur = Temp(val_from, unit_from)
  cur.ConvertToCelsius()
  print(cur)


def run():
  while True:
    print('''Select conversion type:
    1. Temperature
    2. Volume
    3. Mass
    4. Currency
    ''')
    n = input('Enter conversion type: ')
    if n == '1':
      ConvertTemp()
    # elif n == '2':
    #   ConvertVolume()
    # elif n == '3':
    #   ConvertMass()
    # elif n == '4':
    #   ConvertCurrency()
    else:
      raise Exception('Invalid choice {}'.format(n))


if __name__ == '__main__':
  run()
