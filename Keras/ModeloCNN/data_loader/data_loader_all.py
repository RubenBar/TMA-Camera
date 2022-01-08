# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from keras.utils import np_utils 
from sklearn.preprocessing import MinMaxScaler

class Data_Loader():
    def __init__(self, config):
        self.config = config
        self.data = []
        self.load_data()


    def load_data(self):
        # Get list of files
        self.data = pd.read_csv(self.config.dataset.loader.path, sep=',', skiprows=0)


    def get_samples(self):
        samples = self.data.iloc[:, 2:700].values.tolist()
        samples = np.array(samples)
        return samples


    def process_data(self, t_samples, t_labels, model):
        train_samples = np.array(t_samples)
        train_labels = np.array(t_labels)

        train_samples =  self.normalize_data(train_samples)

        if model == "cnn":
            train_samples = train_samples.reshape(train_samples.shape[0], train_samples.shape[1], 1)
            train_labels = np_utils.to_categorical(train_labels, self.config.model.generator.output_dim)
        return train_samples, train_labels


    def normalize_data(self, t_samples):
        data_1 = t_samples
        x,y = data_1.shape
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_1 = scaler.fit_transform(data_1.reshape(-1,1))
        data_1 = data_1.reshape(x,y)
        return data_1


    def count_Labels(self, labels):
        diffLabels = []
        for l in labels:
            if l not in diffLabels:
                diffLabels.append(l)
        return len(diffLabels)


    def get_labels(self):
        labels = self.data['label'].tolist()
        numLabels = self.count_Labels(labels)
        return labels, numLabels


    def get_queries(self):
        queries = self.data['query'].tolist() 
        dic = []
        dic_num = []
        index = 0
        for query in queries:
            if query not in dic:
                dic.append(query)
                dic_num.append(index)
                index = index + 1
        return dic, dic_num
