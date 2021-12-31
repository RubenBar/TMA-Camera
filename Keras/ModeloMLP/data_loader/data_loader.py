import pandas as pd 
import numpy as np
from keras.utils import np_utils 

class Data_Loader_Tcp():   
    def __init__(self, config):
        self.config = config
        self.data = []
        self.load_data() 
    
    
    def load_data(self):   
        #Obtener lista de ficheros
        self.data = pd.read_csv(self.config.dataset.loader.path, sep=',', skiprows=0)

                     
    def get_samples(self):
        #Obtener features
        samples = self.data.iloc[:, 2:650].values.tolist()
        new_samples = []
        for sample in samples:
            data_2 = sample[:650]   
            new_samples.append(data_2)
        return new_samples
        
    
    def process_data(self, t_samples, t_labels, model):             
        train_labels = np.array(t_labels)
        train_samples = np.array(t_samples)  
        
        train_labels = np_utils.to_categorical(train_labels, self.config.model.generator.output_dim)

        return train_samples, train_labels     
         
    
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