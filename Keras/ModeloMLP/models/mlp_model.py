from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam, Adadelta, Adamax, Adagrad
from keras.models import load_model
import numpy as np
from keras.utils.vis_utils import plot_model

class MLP_Model():
    def __init__(self, config):
        self.config = config
        self.build_model()

    def generate_model(self):
        model = Sequential()

        model.add(Dense(units=self.config.model.generator.l1_units, input_shape=(self.config.model.generator.input_dim,), activation='tanh'))
        model.add(Dropout(self.config.model.generator.dropout1))

        model.add(Dense(units=self.config.model.generator.l2_units, activation='relu'))
        model.add(Dropout(self.config.model.generator.dropout2))

        model.add(Dense(units=self.config.model.generator.output_dim, activation='softmax'))

        return model


    def build_model(self):
        print("    Defining the model...")
        self.model = self.generate_model()

        print("    Compiling the model...")
        opt = Adadelta(learning_rate=self.config.model.generator.learning_rate)
        self.model.compile(optimizer=opt, loss=self.config.model.generator.loss_function, metrics=['accuracy'])


    def summary(self):
        print("    Model architecture summary...") 
        self.model.summary()


    def plot_model(self):
        print("    Generate graph with the architecture of the model...")
        plot_model(self.model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
        print("    Generated Graph")


    def train(self, train_samples, train_labels):
        print("    Training the model...")
        model_hist = self.model.fit(
            train_samples, train_labels,
            validation_split = self.config.model.trainer.val_split,
            batch_size = self.config.model.trainer.batch_size,
            epochs = self.config.model.trainer.epochs, 
            verbose = self.config.model.trainer.verbose,
        )
        return model_hist


    def evaluate(self, train_samples, train_labels):
        print("    Evaluating the model...")
        _, accuracy = self.model.evaluate(train_samples, train_labels)
        print('Accuracy: %.2f' % (accuracy*100))
        return accuracy 


    def predict(self, predict_samples, predict_labels):
        print("    Making predictions...") 
        predictions = self.model.predict(x=predict_samples, batch_size=100, verbose=1)
        rounded_predictions = np.argmax(predictions, axis=-1)

        # Uncomment to observe the predictions made
        '''
        rounded_labels = np.argmax(predict_labels, axis=-1)
        for i in range(len(self.rounded_predictions)):
            print('%d (expected %d)' % (self.rounded_predictions[i], rounded_labels[i]))
        '''
        return rounded_predictions


    def save(self):
        print("    Saving model...")
        self.model.save('models/save/mlp_model.h5')
        print("    Model saved successfully...")


    def load(self):
        print("    Loading model...")
        self.model = load_model('models/save/mlp_modelDef.h5')
        print("    Model loaded successfully...")