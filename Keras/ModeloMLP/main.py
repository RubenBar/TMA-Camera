import argparse
from sklearn.model_selection import train_test_split
from models.mlp_model import MLP_Model
from data_loader.data_loader import Data_Loader_Tcp
from utils.config import process_config
from utils.plot import plot_results, plot_model_history


def get_config():
    #Obtencion de los argumentos de entrada
    print('    Leyendo fichero de configuracion...')
    argparser = argparse.ArgumentParser()    
    argparser.add_argument('config', help='Configuracion del modelo')    
    parser = argparser.parse_args()
    
    #Obtencion de la configuracion
    config = process_config(parser.config)
    return config

          
def get_data(config):
    #Obtencion de los datos del dataset
    print('    Seleccionando los datos a utilizar...')   
    if(config.dataset.loader.parameters == 'tcptrace'):
        dl = Data_Loader_Tcp(config)
        
    print('    Procesando los datos...')        
    samples = dl.get_samples()
    labels, numLabels = dl.get_labels()
    queries, queries_num = dl.get_queries()
    train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.3, shuffle=True)
    
    train_samples, train_labels = dl.process_data(train_samples, train_labels, config.model.type)
    test_samples, test_labels = dl.process_data(test_samples, test_labels, config.model.type)
    
    config.model.generator.input_dim = len(train_samples[0])
    config.model.generator.output_dim = numLabels 
    
    return train_samples, train_labels, test_samples, test_labels, numLabels


def get_model(config):
    #Obtencion de la red neuronal - Perceptron Multicapa (MLP)
    print('    Seleccionando la estructura del modelo a utilizar...')
    if config.model.type == 'mlp':
        print('    Modelo seleccionado: MLP')
        model = MLP_Model(config)
        return model
    else:
        raise ValueError('Estructura no conocida')


def main(): 
   
    print('\n##################################') 
    print('##                              ##')   
    print('##       PROGRAMA PRINCIPAL     ##') 
    print('##                              ##') 
    print('##################################') 
    
    print('\n[1/5] Obteniendo ARGUMENTOS de ENTRADA...')
    config = get_config()
    print('Proceso realizado correctamente')
    
    
    print('\n[2/5] Obteniendo y preparando los DATOS...')
    t_samples, t_labels, test_samples, test_labels, numLabels = get_data(config)
    print('Proceso realizado correctamente')  


    print('\n[3/5] Creando el MODELO...')     
    model = get_model(config)
    model.summary()
    model.plot_model()
    print('Proceso realizado correctamente ')
    
    
    print('\n[4/5] Entrenando el MODELO...')  
    model_hist = model.train(t_samples, t_labels)
    model.evaluate(t_samples, t_labels)
    #model.save()
    print('Proceso realizado correctamente ')
    
        
    print('\n[5/5] Preparando RESULTADOS...') 
    rounded_predictions = model.predict(test_samples, test_labels)
    plot_results(numLabels, test_labels, rounded_predictions)
    plot_model_history(model_hist)
    print('Proceso realizado correctamente ')
     
if __name__ == "__main__":
        main()