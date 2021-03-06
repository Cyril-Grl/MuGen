from tensorflow.keras.layers import Lambda, Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.losses import mse, binary_crossentropy
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend as K
import argparse
import math

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

import os

import pretty_midi
import pandas as pd
import numpy as np

from tensorflow.keras.layers import Dense,Activation, Dropout

from src.data import get_drum
class Vae:
    def __init__(self):
        self.epochs = 20
        self.batch_size = 128
        self.intermediate_dim = 512
        self.latent_dim = 2

        print("LOADING VAE MODEL...")

        # x_train, y_train = self.load_data_for_evaluation("ressources/example_midi_file.mid")

        self.vae, self.encoder, self.decoder = self.compile_model((4800,))
        self.vae.load_weights("src/vae_centre_sur_random.h5")
        self.models = (self.encoder, self.decoder)

        filepath = "ressources/dataset_csv/dataset.csv"
        if not os.path.exists(filepath):
            filepath = "../ressources/dataset_csv/dataset.csv"
        self.metadata = pd.read_csv(filepath)



    # reparameterization trick
    # instead of sampling from Q(z|X), sample epsilon = N(0,I)
    # z = z_mean + sqrt(var) * epsilon
    def sampling(self,args):
        """Reparameterization trick by sampling from an isotropic unit Gaussian.
        # Arguments
            args (tensor): mean and log of variance of Q(z|X)
        # Returns
            z (tensor): sampled latent vector
        """

        z_mean, z_log_var = args
        batch = K.shape(z_mean)[0]
        dim = K.int_shape(z_mean)[1]
        # by default, random_normal has mean = 0 and std = 1.0
        epsilon = K.random_normal(shape=(batch, dim))
        return z_mean + K.exp(0.5 * z_log_var) * epsilon


    def get_coord(self,models,data,batch_size=128,model_name="vae_mnist"):
        encoder, decoder = models
        x_test, y_test = data
        os.makedirs(model_name, exist_ok=True)

        filename = os.path.join(model_name, "vae_mean.png")
        # display a 2D plot of the digit classes in the latent space
        z_mean,_,_= encoder.predict(x_test,
                                       batch_size=batch_size)

        #print(z_mean)
        #plt.scatter(z_mean[:, 0], z_mean[:, 1], c=y_test)
        #plt.show()
        return z_mean




    def compile_model(self, input_shape):
        intermediate_dim = 512
        latent_dim = 2
        # VAE model = encoder + decoder
        # build encoder model
        inputs = Input(shape=input_shape, name='encoder_input')
        x = Dense(intermediate_dim, activation='relu')(inputs)
        z_mean = Dense(latent_dim, name='z_mean')(x)
        z_log_var = Dense(latent_dim, name='z_log_var')(x)

        # use reparameterization trick to push the sampling out as input
        # note that "output_shape" isn't necessary with the TensorFlow backend
        z = Lambda(self.sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

        # instantiate encoder model
        encoder = Model(inputs, [z_mean, z_log_var, z], name='encoder')
        # encoder.summary()
        # plot_model(encoder, to_file='vae_mlp_encoder.png', show_shapes=True)

        # build decoder model
        latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
        x = Dense(intermediate_dim, activation='relu')(latent_inputs)
        outputs = Dense(input_shape[0], activation='sigmoid')(x)

        # instantiate decoder model
        decoder = Model(latent_inputs, outputs, name='decoder')
        # decoder.summary()
        # plot_model(decoder, to_file='vae_mlp_decoder.png', show_shapes=True)

        # instantiate VAE model
        outputs = decoder(encoder(inputs)[2])
        vae = Model(inputs, outputs)  # , name='vae_mlp')

        vae.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        # vae.summary()
        # plot_model(vae, to_file='vae_mlp.png', show_shapes=True)

        return vae, encoder, decoder

    def load_data_for_evaluation(self,path_to_plot):
        # features = []
        # '''
        # # Iterate through each midi file and extract the features
        # for index, row in self.metadata.iterrows():
        #     path_midi_file = self.path + str(row["File"])
        #     if row["Score"] == 100:
        #         class_label = float(row["Score"]) / 100
        #         midi_data = pretty_midi.PrettyMIDI(path_midi_file)
        #         for instrument in midi_data.instruments:
        #             instrument.is_drum = False
        #         if len(midi_data.instruments) > 0:
        #             data = midi_data.get_piano_roll(fs=8)
        #             data.resize(3968)
        #             result = np.where(data == 80)
        #
        #             features.append([data, class_label])
        # '''
        # '''
        # # GRAB A 50 AND CALCULATE ITS DISTANCE
        # for index, row in metadata.iterrows():
        #     path_midi_file = path+ str(row["File"])
        #     if row["File"] == "27_random.mid":
        #         class_label = float(row["Score"]) / 100
        #         midi_data = pretty_midi.PrettyMIDI(path_midi_file)
        #         for instrument in midi_data.instruments:
        #             instrument.is_drum=False
        #         if len(midi_data.instruments)>0:
        #             data  = midi_data.get_piano_roll(fs=8)
        #             data.resize(3968)
        #             result = np.where(data == 80)
        #
        #             features.append([data, class_label])
        # '''
        # class_label = 0
        # midi_data = pretty_midi.PrettyMIDI(path_to_plot)
        #
        # for instrument in midi_data.instruments:
        #     instrument.is_drum = False
        # if len(midi_data.instruments) > 0:
        #     data = midi_data.get_piano_roll(fs=8)
        #     data.resize(3968)
        #     result = np.where(data == 80)
        #
        #     features.append([data, class_label])
        #
        # # Convert into a Panda dataframe
        # featuresdf = pd.DataFrame(features, columns=['feature', 'class_label'])
        #
        # #print('Finished feature extraction from ', len(featuresdf), ' files')
        #
        # # Convert features & labels into numpy arrays
        # X = np.array(featuresdf.feature.tolist())
        # y = np.array(featuresdf.class_label.tolist())
        #
        # #print(X.shape, y.shape)
        # # split the dataset
        midi_data = pretty_midi.PrettyMIDI(path_to_plot)
        a = None
        for instrument in midi_data.instruments:
            if instrument.is_drum:
                instrument.is_drum = False
                a = instrument.get_piano_roll()[36:48]
                a[a > 0] = 1
                a = np.pad(a, [(0, 0), (0, 400 - a.shape[1])], 'constant')
                a = a.astype(dtype=bool)
                a.resize(4800)
        X = a
        y = np.array(0)
        x_train = X
        y_train = y

        #midi_file_size = x_train.shape[1]

        # network parameters
        #input_shape = (midi_file_size,)


        # x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))


        #return vae, encoder, decoder, x_train, y_train
        return  x_train, y_train


    def load_data_for_training(self, path_to_plot):
        features = []

        # Iterate through each midi file and extract the features
        for index, row in metadata.iterrows():
            path_midi_file = path+ str(row["File"])
            #if row["Score"] == 0 or row["Score"] == 100:
            if row["Score"] !=89:
                class_label = float(row["Score"]) / 100
                midi_data = pretty_midi.PrettyMIDI(path_midi_file)
                for instrument in midi_data.instruments:
                    instrument.is_drum=False
                if len(midi_data.instruments)>0:
                    data  = midi_data.get_piano_roll(fs=8)
                    #data.resize(3968)
                    data.resize(3968)
                    #np.pad(data, [(0,0), (0, 10000-data.shape[1])], 'constant')
                    #print(data.size)
                    result = np.where(data == 80)
                    features.append([data, class_label])
        '''
        #Itarating through the lakh midi dataset:
        for subdir, dirs, files in os.walk(lakh_path):
            for file in files:
                if file !=".DS_Store":
                    #print(os.path.join(subdir, file))
                    class_label=0
                    try:
                        midi_data = pretty_midi.PrettyMIDI(subdir+"/"+file)
                        for instrument in midi_data.instruments:
                            instrument.is_drum=False
                        if len(midi_data.instruments)>0:
                            data  = midi_data.get_piano_roll(fs=8)
                            data.resize(10000)
                            features.append([data, class_label])
                            #print("ADDED")
                    except:
                        print("An exception occurred")
    
        '''


        # Convert into a Panda dataframe
        featuresdf = pd.DataFrame(features, columns=['feature','class_label'])

        print('Finished feature extraction from ', len(featuresdf), ' files')

        # Convert features & labels into numpy arrays
        X = np.array(featuresdf.feature.tolist())
        y = np.array(featuresdf.class_label.tolist())

        print(X.shape,y.shape)
        # split the dataset


        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


        midi_file_size = x_train.shape[1]

        return vae, encoder, decoder, x_train, y_train, x_test, y_test

    def train(self):
        batch_size = 128
        epochs = 100
        batch_size = 128
        vae, encoder, decoder, x_train, y_train, x_test, y_test = load_data(True)
        data = (x_train, y_train)
        # train the autoencoder
        vae.fit(x_train, x_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, x_test))
        # validation_data=(x_test, None))
        vae.save_weights('vae_midi.h5')
        models = (encoder, decoder)
        coord = get_coord(models, data, batch_size=batch_size)

        x = coord[:, 0]
        y = coord[:, 1]
        # print(x, y)

        # distance = math.sqrt(((0 - x) ** 2) + ((0 - y) ** 2))
    # def train(self):
    #     vae, encoder, decoder, x_train, y_train, x_test, y_test = load_data_for_training(path_to_plot)
    #     data = (x_train, y_train)
    #     models = (encoder, decoder)
    #
    #     # train the autoencoder
    #     vae.fit(x_train,
    #             x_train,
    #             epochs=epochs,
    #             batch_size=batch_size,
    #             validation_data=(x_test, x_test))
    #     # validation_data=(x_test, None))
    #     vae.save_weights('vae_midi.h5')


    def get_distance(self,midi_file_path):


        x_train, y_train = self.load_data_for_evaluation(midi_file_path)
        #vae, encoder, decoder = self.compile_model(x_train)

        data = (x_train, y_train)

        coord = self.get_coord(self.models,data,batch_size=self.batch_size,model_name="vae_mlp")

        x = coord[:, 0]
        y = coord[:, 1]
        #print(x,y)

        distance = math.sqrt(   ( (0-x) **2)  +  ( (0-y) **2) )
        #print(distance)

        return distance
