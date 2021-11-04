
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pickle

import keras
from keras.layers import LSTM, Bidirectional
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import keras.backend as K
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error


'''
Train, Test data from 5-Timeseries_data_prep.py
'''

def lag_window(df,split_rate, lag, col_name, return_original_x = True) :
    lag = lag+1
    result = []
    for idx in range(len(df)-(lag-1)) :
        result.append(df[col_name][idx: idx+lag])
    ########
    lag_arr = np.array(result)
    row = int(round(split_rate*lag_arr.shape[0]))
    train = lag_arr[:row,:]
    
    X_train = train[:,:-1]

    X_min = X_train.min()
    X_max = X_train.max()

    #in case..
    X_min_orig = X_min
    X_max_orig = X_max
    
    def minmax(X) :
      return (X-X_min) / (X_max -X_min)
    
    def inverse_minmax(X) :
      return X * (X_max-X_min) + X_min
    
    def minmax_windows(window_data) :
      normalized = []
      for window in window_data :
        window.index = range(lag)
        normalized_window = [((minmax(p))) for p in window]
        normalized.append(normalized_window)
      return normalized
  
    result = minmax_windows(result)
    result = np.array(result)

    if return_original_x :
      return result, X_min_orig, X_max_orig  
    else :
      return result

def convert_window(window, split_rate) :

    row = round(split_rate *window.shape[0])
    train = window[:row, :]
    
    X_train = train[:,:-1]    
    Y_train = train[:,-1]
    
    X_test = window[row:, :-1]
    print(window.shape[0])
    print(row)
    Y_test = window[row:, -1]
    
    #reshape for fit dimension for LSTM
    X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))
    Y_train = np.reshape(Y_train,(-1,1))
    
    X_test = np.reshape(X_test,(X_test.shape[0], X_test.shape[1],1))
    Y_test = np.reshape(Y_test,(-1,1))
    
    return X_train, Y_train, X_test, Y_test

def data_prep(keyword_train, colname, lag,split_rate) :
    #train_sc_df,sc = scaling(keyword_train)
    lag_result,X_min, X_max = lag_window(keyword_train,split_rate,lag,colname)
    X_train, Y_train, X_test, Y_test = convert_window(lag_result,split_rate)
    return X_train, Y_train,X_test,Y_test, X_min, X_max


def model():
    K.clear_session()
    look_back = 1
    model = Sequential()
    #2 layers
    #input
    model.add(Bidirectional(LSTM(512,activation = 'relu' , return_sequences = True, input_shape= (3,1))))
    #hidden
    model.add(LSTM(512, activation = 'relu'))
    #model.add(keras.layers.BatchNormalization())
    #model.add(Dropout(0.1))
    #model.add(LSTM(512, activation = 'relu'))
    model.add(Dense(1))

    model.compile(loss = "mean_squared_error", optimizer = 'adam')
    #model.summary()  
    return model 

def training_LSTM(x_train_t, y_train,x_test, y_test, epc) :
    
    early_stop = EarlyStopping(monitor = 'loss', patience = 50, verbose = 1)
    history = model.fit(x_train_t, y_train, validation_data=(x_test, y_test), epochs = epc, batch_size = 32, verbose=1)
  
    return history, model

def model_save(model, name) : 
    model.save(path+name)
    return 

def model_load( name) :
    m1 = keras.models.load_model(path+name)
    return m1

def history_save(history, name) :
    with open(path+name, 'wb') as f :
      pickle.dump(history,f)

def train_visualize(model,lag,be_predict, data_df, max, min, test = False) :
  pred = model.predict(be_predict)
  true_pred = inverse_minmax(pred, max, min)

  freq = list(data_df['freq'])[lag:]
  test_idx = freq[int(len(freq)*0.8):]
  train_idx = freq[:int(len(freq)*0.8)]
  plt.figure(figsize=(10,6))
  #plt.xticks(date_list[3:][int(len(freq)*0.8):][int(len(freq)*0.8)][::2],rotation = 90)
  if test :
    plt.plot(date_list[3:][int(len(freq)*0.8):],test_idx, label = 'groud truth')
    plt.xticks(date_list[3:][int(len(freq)*0.8):][::2],rotation = 90)
  else :
    plt.plot(date_list[3:][:int(len(freq)*0.8)],train_idx, label = "ground truth")
    plt.xticks(date_list[3:][:int(len(freq)*0.8)][::6],rotation = 90)

  plt.plot(true_pred, label = 'predict')
  plt.legend()
  plt.savefig(path+"validation_model_fire.jpeg", dpi = 300)
  plt.show()

  return true_pred, train_idx, test_idx

def total_visualize(model,lag,x_train, x_valid, data_df, max, min) :
  #predict values
  pred_train = model.predict(x_train)
  pred_valid = model.predict(x_valid)
  true_train = inverse_minmax(pred_train, max, min)
  true_valid = inverse_minmax(pred_valid, max, min)


  freq = list(data_df['freq'])[lag:]
  #print(len(freq))
  test_idx = freq[int(len(freq)*0.8):]
  train_idx = freq[:int(len(freq)*0.8)]
  print(len(freq))
  
  total_train = np.append(train_idx, test_idx)
  total_valid = np.append(true_train, true_valid)
  plt.figure(figsize=(10,6))
  plt.plot(date_list[3:],total_train, label = 'ground truth')
  plt.plot(date_list[3:],total_valid, label = "predict")
  #plt.xticks(list(range(1,max(x)+1)),[str(i) for i in range(1,max(x)+1)])
  plt.xticks(date_list[3:][::6],rotation = 90)
  plt.axvspan(int(len(freq)*0.8),len(freq), facecolor= 'gray', alpha =0.5)
  plt.legend()
  plt.savefig(path+"total_visualize_model_fire.jpeg", dpi = 300)
  plt.show()

  return true_train, true_valid

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred)) *100)

def mean_absolute_error(y_true, y_pred) :
    return np.mean(np.abs(y_true-y_pred))

def evaluating(model, x, y) :
    
    score = model.evaluate(x,y, batch_size = 32)
    
    return score



if __name__ == '__main__' :

    #example of fire

    f_x_train, f_y_train, f_x_val, f_y_val, X_min, X_max = data_prep(fire_train,'freq', 3,0.8)

    model = model()
    fire_history, model = training_LSTM(f_x_train,f_y_train,f_x_val, f_y_val,400)
    model_save(model, "fire_v_09_1028")

    #plot for test/train data ground truth, prediction
    true_pred, train_re, test_re = train_visualize(model,3, f_x_val,fire_train, X_max, X_min,True)
    
    #plot for train+test data, ground truth, prediction
    true_train, true_valid = total_visualize(model, 3, f_x_train, f_x_val, fire_train, X_max, X_min)

    #Model Evaluations
    # RMSE
    score = evaluating(model,f_x_val,f_y_val)
    np.sqrt(score)

    # MAE
    mean_absolute_error(test_re, true_pred)