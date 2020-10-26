from keras.utils import plot_model
from keras.models import load_model

model = load_model('DBNweights.h5')
model.summary()
plot_model(model, to_file='model.png', show_shapes = True)