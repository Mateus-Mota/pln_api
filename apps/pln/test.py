import logging
import os

import numpy as np
import tensorflow_datasets as tfds
from dm.dcnn import DCNN

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

logging.getLogger("tensorflow").disabled = True

Dcnn = DCNN()
Dcnn.built = True

path = "apps/pln/weights_folder/my_weights"
Dcnn.load_weights(path).expect_partial()

vocab_fname = "apps/pln/services/ttVocab"

encoder = tfds.deprecated.text.SubwordTextEncoder.load_from_file(vocab_fname)
text = "I like you"
text = encoder.encode(text)

# 0 =  negativo
# 1 = possitivo

value = Dcnn.predict(np.array([text]))
print(value)
