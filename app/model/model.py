import tensorflow.keras as keras
from keras import models
from keras import layers


def create_model():

    METRICS = [
          keras.metrics.TruePositives(name='tp'),
          keras.metrics.FalsePositives(name='fp'),
          keras.metrics.TrueNegatives(name='tn'),
          keras.metrics.FalseNegatives(name='fn'),
          keras.metrics.BinaryAccuracy(name='accuracy'),
          keras.metrics.Precision(name='precision'),
          keras.metrics.Recall(name='recall'),
          keras.metrics.AUC(name='auc'),
    ]


    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', # (3,3) - фильтр
                            input_shape=(32,141,1)),
        layers.MaxPooling2D((2,2)), # фильтр (2,2) для пулинга
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, 'relu'),
        layers.Dense(32, 'relu'),
        layers.Dense(16, 'relu'),
        layers.Dense(1, 'sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=METRICS)
    return model

def callbacks():

    class CustomCallback(keras.callbacks.Callback):
        def on_train_begin(self, logs=None):
            keys = list(logs.keys())
            # print("Starting training; got log keys: {}".format(keys))

        def on_train_end(self, logs=None):
            keys = list(logs.keys())
            # print("Stop training; got log keys: {}".format(keys))

        def on_train_batch_begin(self, batch, logs=None):
            keys = list(logs.keys())
            print("...Training: start of batch {}; got log keys: {}".format(batch, keys))

        def on_train_batch_end(self, batch, logs={}):
            # keys = list(logs.keys())
            print({'loss': logs.get('loss'), 'tp': logs.get('tp'), 'fp': logs.get('fp'), 'tn': logs.get('tn'),
                   'fn': logs.get('fn'), 'accuracy': logs.get('accuracy'), 'precision': logs.get('precision'),
                   'recall': logs.get('recall'),
                   'auc': logs.get('auc')})

    return CustomCallback()
