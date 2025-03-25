from keras import Model
from tensorflow.keras.layers import Input, Lambda, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate, Dropout
import tensorflow as tf


def build(model_path):
  print("Используемая версия tensorflow ", tf.__version__)
  inputs = Input((256, 256, 3))
  s = Lambda(lambda x: x / 255) (inputs)

  c0 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (s)
  c0 = Dropout(0.5) (c0)
  c0 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c0)
  p0 = MaxPooling2D((2, 2)) (c0)

  c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p0)
  c1 = Dropout(0.5) (c1)
  c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c1)
  p1 = MaxPooling2D((2, 2)) (c1)

  c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p1)
  c2 = Dropout(0.5) (c2)
  c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c2)
  p2 = MaxPooling2D((2, 2)) (c2)

  c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p2)
  c3 = Dropout(0.5) (c3)
  c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c3)
  p3 = MaxPooling2D((2, 2)) (c3)

  c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (p3)
  c4 = Dropout(0.5) (c4)
  c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c4)
  p4 = MaxPooling2D(pool_size=(2, 2)) (c4)

  c5 = Conv2D(256, (5, 5), activation='elu', kernel_initializer='he_normal', padding='same') (p4)
  c5 = Dropout(0.5) (c5)
  c5 = Conv2D(256, (5, 5), activation='elu', kernel_initializer='he_normal', padding='same') (c5)

  u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same') (c5)
  u6 = concatenate([u6, c4])
  c6 = Conv2D(128, (7, 7), activation='elu', kernel_initializer='he_normal', padding='same') (u6)
  c6 = Dropout(0.5) (c6)
  c6 = Conv2D(128, (7, 7), activation='elu', kernel_initializer='he_normal', padding='same') (c6)

  u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (c6)
  u7 = concatenate([u7, c3])
  c7 = Conv2D(64, (7, 7), activation='elu', kernel_initializer='he_normal', padding='same') (u7)
  c7 = Dropout(0.5) (c7)
  c7 = Conv2D(64, (7, 7), activation='elu', kernel_initializer='he_normal', padding='same') (c7)

  u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c7)
  u8 = concatenate([u8, c2])
  c8 = Conv2D(32, (5, 5), activation='elu', kernel_initializer='he_normal', padding='same') (u8)
  c8 = Dropout(0.5) (c8)
  c8 = Conv2D(32, (5, 5), activation='elu', kernel_initializer='he_normal', padding='same') (c8)

  u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c8)
  u9 = concatenate([u9, c1], axis=3)
  c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u9)
  c9 = Dropout(0.5) (c9)
  c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c9)

  u10 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c9)
  u10 = concatenate([u10, c0], axis=3)
  c10 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (u10)
  c10 = Dropout(0.5) (c10)
  c10 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same') (c10)

  outputs = Conv2D(1, (1, 1), activation='sigmoid') (c10)

  model = Model(inputs=[inputs], outputs=[outputs])
  model.compile(optimizer='Adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
  model.load_weights(model_path)
  return model
