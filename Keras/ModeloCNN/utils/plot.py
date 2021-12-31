# -*- coding: utf-8 -*-
"""
MATRIZ DE CONFUSION
"""
##MATRIZ DE CONFUSION --> CONOCER LOS RESULTADOS DE NUESTRO MODELO##
import numpy as np
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt

def plot_results(queries, test_labels, rounded_predictions):
    print("    Generando graficos...") 
    test_labels = np.argmax(test_labels, axis=-1)
    cm = confusion_matrix(y_true=test_labels, y_pred=rounded_predictions)    
    cm_plot_labels = ['Movimiento','No_movimiento']
    plot_confusion_matrix(cm=cm, classes=cm_plot_labels)
                   
    
def plot_confusion_matrix(cm, classes, normalize=False, cmap=plt.cm.Blues):
    title='Confusion matrix'
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    

def plot_model_history(model_history):
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['accuracy'])+1),model_history.history['accuracy'])
    axs[0].plot(range(1,len(model_history.history['val_accuracy'])+1),model_history.history['val_accuracy'])
    axs[0].set_title('Porcentaje de Aciertos')
    axs[0].set_ylabel('Precisión')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['accuracy'])+1),len(model_history.history['accuracy'])/10)
    axs[0].legend(['cj. entrenamiento', 'cj. validación'], loc='best')
    
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Función de Pérdida')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['cj. entrenamiento', 'cj. validación'], loc='best')
    plt.show()

