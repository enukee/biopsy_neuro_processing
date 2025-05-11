from keras import Model
from tensorflow.keras.layers import Lambda, Conv2D, MaxPool2D, Conv2DTranspose, Concatenate, BatchNormalization
from tensorflow.keras import Input
import tensorflow as tf

SIZE = None                     # Размерность входного слоя
N_LEVELS = 7                    # Количество уровней модели
DIVIDER = pow(2, N_LEVELS - 1)  # Делитель, модель принимает только данные размерность которых кратна DIVIDER


# Кастомная UNET
def unet(n_levels, initial_features=32, n_blocks=2, kernel_size=3, pooling_size=2, in_channels=1, out_channels=3):
  inputs = Input(shape=(SIZE, SIZE, in_channels))
  x = Lambda(lambda x: x / 255) (inputs)
  convpars = dict(kernel_size=kernel_size, activation='elu', kernel_initializer='he_normal', padding='same')

  #downstream

  skips = {}

  for level in range(n_levels):
    for _ in range(n_blocks):
      x = Conv2D(initial_features * 2 ** level, **convpars)(x)
      x = BatchNormalization()(x)
    if level < n_levels - 1:
      skips[level] = x
      x = MaxPool2D(pooling_size)(x)



  # upstream
  for level in reversed(range(n_levels - 1)):
    x = Conv2DTranspose(initial_features * 2 ** level, strides=pooling_size, **convpars)(x)
    x = Concatenate()([x, skips[level]])
    for _ in range(n_blocks):
      x = Conv2D(initial_features * 2 ** level, **convpars)(x)
      x = BatchNormalization()(x)



  # output
  activation = 'sigmoid' if out_channels == 1 else 'softmax'
  x = Conv2D(out_channels, kernel_size=1, activation=activation, padding='same')(x)
  return Model(inputs=[inputs], outputs=[x], name=f'UNET-L{n_levels}-F{initial_features}')


def build(model_path):
  print("Используемая версия tensorflow ", tf.__version__)
  model = unet(N_LEVELS, in_channels=3, out_channels=1)

  model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  model.load_weights(model_path)
  model.summary()
  return model
