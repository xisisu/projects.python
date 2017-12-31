'''
dataset info: https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names
'''

import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import sklearn.datasets
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection


def PredictBostonHouse():
  # source: https://medium.com/@haydar_ai/learning-data-science-day-9-linear-regression-on-boston-housing-dataset-cd62a80775ef

  boston = sklearn.datasets.load_boston()

  # print(boston.keys())
  # print(boston.feature_names)
  # print(boston.DESCR)

  bos = pd.DataFrame(boston.data)
  bos.columns = boston.feature_names
  bos['PRICE'] = boston.target
  X = bos.drop(['PRICE'], axis=1)
  Y = bos['PRICE']
  X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.33, random_state=5)

  # print(X_train.shape)
  # print(X_test.shape)
  # print(Y_train.shape)
  # print(Y_test.shape)

  lm = sklearn.linear_model.LinearRegression()
  lm.fit(X_train, Y_train)
  Y_pred = lm.predict(X_test)

  plt.scatter(Y_test, Y_pred)
  plt.xlabel('Actual Price: $Y_i$')
  plt.ylabel('Predicted Price: $\hat{Y}_i$')
  plt.title('Actual vs. Predicted Prices')
  plt.show()

  mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)
  print(mse)


def PredictBostonHouse1():
  lr = sklearn.linear_model.LinearRegression()
  boston = sklearn.datasets.load_boston()
  y = boston.target

  # cross_val_predict returns an array of the same size as `y` where each entry
  # is a prediction obtained by cross validation:
  predicted = sklearn.model_selection.cross_val_predict(lr, boston.data, y, cv=10)

  fig, ax = plt.subplots()
  ax.scatter(y, predicted, edgecolors=(0, 0, 0))
  ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
  ax.set_xlabel('Measured')
  ax.set_ylabel('Predicted')
  plt.show()

def run():
  # PredictBostonHouse()
  PredictBostonHouse1()

if __name__ == '__main__':
  run()
