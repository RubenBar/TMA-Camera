from keras.models import Sequential
from keras.layers import Conv1D, Dense, Dropout, Flatten, MaxPooling1D
from keras.optimizers import Adam
from keras.models import load_model
import numpy as np
from keras.utils.vis_utils import plot_model


class CNN_Model():
    def __init__(self, config):
        self.config = config
        self.build_model()

    def generate_model(self):
        model = Sequential()

        model.add(Conv1D(filters=self.config.model.generator.l1_filt, kernel_size=self.config.model.generator.l1_kernel, activation='tanh',
                         input_shape=(self.config.model.generator.input_dim,1)))
        model.add(MaxPooling1D(pool_size=self.config.model.generator.l1_psize))
        model.add(Dropout(self.config.model.generator.dropout))

        model.add(Conv1D(filters=self.config.model.generator.l2_filt, kernel_size=self.config.model.generator.l2_kernel, activation='relu'))
        model.add(MaxPooling1D(pool_size=self.config.model.generator.l2_psize))
        model.add(Dropout(self.config.model.generator.dropout))

        model.add(Flatten())
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=self.config.model.generator.output_dim, activation='softmax'))

        return model


    def build_model(self):
        print("    Defining model...")
        self.model = self.generate_model()

        print("    Compiling model...")
        opt = Adam(learning_rate=self.config.model.generator.learning_rate)
        self.model.compile(optimizer=opt, loss=self.config.model.generator.loss_function, metrics=['accuracy'])


    def summary(self):
        print("    Summary of the model architecture...")
        self.model.summary()


    def train(self, train_samples, train_labels):
        print("    Training model...")
        model_hist = self.model.fit(
            train_samples, train_labels,
            validation_split = self.config.model.trainer.val_split,
            batch_size = self.config.model.trainer.batch_size,
            epochs = self.config.model.trainer.epochs, 
            verbose = self.config.model.trainer.verbose,
        )
        return model_hist


    def evaluate(self, train_samples, train_labels):
        print("    Evaluating model...")
        _, accuracy = self.model.evaluate(train_samples, train_labels)
        print('Accuracy: %.2f' % (accuracy*100))
        return accuracy 


    def predict(self, predict_samples, predict_labels):
        print("    Making predictions...")
        predictions = self.model.predict(x=predict_samples, batch_size=150, verbose=1)
        # The following code lines are commented as they are used for DEBUG purposes
        # rounded_labels = np.argmax(predict_labels, axis=-1)
        rounded_predictions = np.argmax(predictions, axis=-1)
        #for i in range(len(rounded_predictions)):
        #    print('%d (expected %d)' % (rounded_predictions[i], rounded_labels[i]))
        return rounded_predictions


    def plot_model(self):
        print("    Generate graph with the architecture of the model...")
        plot_model(self.model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
        print("    Generated graph")


    def save(self):
        print("    Saving model...")
        self.model.save('models/save/cnn_model.h5')
        print("    Model saved successfully...")


    def load(self):
        print("    Loading model...")
        self.model = load_model('models/save/cnn_model.h5')
        print("    Model loaded successfully...")