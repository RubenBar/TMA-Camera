import argparse
from sklearn.model_selection import train_test_split
from models.cnn_model import CNN_Model
from data_loader.data_loader_all import Data_Loader
from utils.config import process_config
from utils.plot import plot_results, plot_model_history


def get_config():
    # Getting the input arguments
    print('    Reading configuration file...')
    argparser = argparse.ArgumentParser()
    argparser.add_argument('config', help='Model setup')
    parser = argparser.parse_args()

    # Getting the settings
    config = process_config(parser.config)
    return config


def get_data(config):
    # Getting the data from the Dataset
    print('    Selecting the data to use...')
    if(config.dataset.loader.parameters == 'all'):
        dl = Data_Loader(config)

    print('    Processing the data...')
    samples = dl.get_samples()
    labels, numLabels = dl.get_labels()
    queries, queries_num = dl.get_queries()
    train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.2, shuffle=True)

    train_samples, train_labels = dl.process_data(train_samples, train_labels, config.model.type)
    test_samples, test_labels = dl.process_data(test_samples, test_labels, config.model.type)

    config.model.generator.input_dim = len(train_samples[0])
    config.model.generator.output_dim = numLabels 

    return train_samples, train_labels, test_samples, test_labels, numLabels


def get_model(config):
    print('    Selecting the structure of the model to use...')
    if config.model.type == 'cnn':
        print('    Selected Model: CNN')
        model = CNN_Model(config)
        return model

    else:
        raise ValueError('Unknown structure')


def main():

    print('\n##################################')
    print('##                              ##')
    print('##         MAIN PROGRAM         ##')
    print('##                              ##')
    print('##################################')

    print('\n[1/5] Getting INPUT ARGUMENTS...')
    config = get_config()
    print('Process done correctly')


    print('\n[2/5] Obtaining and preparing the DATOS...')
    t_samples, t_labels, test_samples, test_labels, numLabels = get_data(config)
    print('Process done correctly')


    print('\n[3/5] Preparating the MODEL...')
    model = get_model(config)
    model.summary()
    model.plot_model()
    print('Process done correctly')


    print('\n[4/5] Training the MODEL...')
    model_hist = model.train(t_samples, t_labels)
    model.evaluate(t_samples, t_labels)
    #model.save()
    print('Process done correctly')


    print('\n[5/5] Preparating RESULTS...')
    rounded_predictions = model.predict(test_samples, test_labels)
    plot_results(numLabels, test_labels, rounded_predictions)
    plot_model_history(model_hist)
    print('Process done correctly')


if __name__ == "__main__":
        main()