

#pip install neurokit2

# LSTM 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import neurokit2 as nk
import numpy

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)



def clean(dataset):
            np.random.seed(7)
            dataset=dataset.iloc[len(dataset)-2001:len(dataset)-1,2:3]
            ecg=list(dataset.iloc[0:,0])
            signals = pd.DataFrame({"ECG_Raw" : ecg,
                        "ECG_NeuroKit" : nk.ecg_clean(ecg, sampling_rate=1000, method="neurokit"),
                             })
            dataset=signals.iloc[0:,1]
            print(dataset.head(4))
            d=dataset.array
            dataset=d.reshape(-1, 1)
        # normalize the dataset
            scaler = MinMaxScaler(feature_range=(0, 1))
            dataset = scaler.fit_transform(dataset)
            # split into train and test sets
            train_size = int(len(dataset) * 0.67)
            test_size = len(dataset) - train_size
            train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

            # reshape into X=t and Y=t+1
            import numpy
            look_back = 1
            trainX, trainY = create_dataset(train, look_back)
            testX, testY = create_dataset(test, look_back)
            # reshape input to be [samples, time steps, features]
            trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

            # create and fit the LSTM network
            model = Sequential()
            model.add(LSTM(4, input_shape=(1, look_back)))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer='adam')
            model.fit(trainX, trainY, epochs=15, batch_size=1, verbose=2)
            # make prediction
            trainPredict = model.predict(trainX)
            testPredict = model.predict(testX)

            # invert predictions
            trainPredict = scaler.inverse_transform(trainPredict)
            trainY = scaler.inverse_transform([trainY])
            testPredict = scaler.inverse_transform(testPredict)
            testY = scaler.inverse_transform([testY])

            # calculate root mean squared error
            trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
            print('Train Score: %.2f RMSE' % (trainScore))
            testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
            print('Test Score: %.2f RMSE' % (testScore))
            #Train Score: 7.33 RMSE
            #Test Score: 6.45 RMSE

            #normal 2
            # shift train predictions for plotting
            trainPredictPlot = numpy.empty_like(dataset)
            trainPredictPlot[:, :] = numpy.nan
            trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
            # shift test predictions for plotting
            testPredictPlot = numpy.empty_like(dataset)
            testPredictPlot[:, :] = numpy.nan
            testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
                # plot baseline and predictions
            plt.figure(figsize=(10, 4))
            plt.plot(scaler.inverse_transform(dataset[0:1700]), label="Original", color='red')
            plt.plot(trainPredictPlot, label="Predicted train data",color="green") 
            plt.plot(testPredictPlot[:1700], label="Predicted test data",color="blue")
            r=testPredictPlot[1700:]
            x = np.arange(1700,2000 , 1)
            plt.plot(x,r, label="forecasted",color="orange")
            #plt.title("ECG signal forecasting for subject 100")
            plt.legend(loc="upper left")
            plt.ylabel('Signal')
            plt.xlabel("Time")
            return plt



    
        
#dataset = read_csv(r"C:\Users\SURABHI. S\OneDrive\Desktop\fsp - ecg\mitbih_database\100.csv") #, usecols=[1], engine='python')
#clean(dataset)
    
    
    

    

    



    
    

    

    

    
    
