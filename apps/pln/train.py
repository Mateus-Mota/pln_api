# import logging, os
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# import logging
# logging.getLogger('tensorflow').disabled = True

import numpy as np
import pandas as pd
import spacy as sp
import tensorflow as tf
import tensorflow_datasets as tfds
from clean_tt.clean_tweets import clean_tweets, clean_tweets2
from dm.dcnn import DCNN
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


class Main:
    cols = ["sentiment", "id", "date", "query", "user", "text"]

    def train(self):
        print("--- train ---")
        train_data = pd.read_csv(
            "apps/pln/data/trainingandtestdata/train.csv",
            header=None,
            names=self.cols,
            engine="python",
            encoding="latin1",
        )
        return train_data

    def test_data(self):
        print("--- test data ---")
        test_data = pd.read_csv(
            "apps/pln/data/trainingandtestdata/test.csv",
            header=None,
            names=self.cols,
            engine="python",
            encoding="latin1",
        )
        return test_data

    def data_drop(self, data):
        print("--- data drop cols ---")
        data.drop(["id", "date", "query", "user"], axis=1, inplace=True)
        return data

    def data_labels(self, y):
        print("--- data labels ---")
        data_labels = y
        data_labels[data_labels == 4] = 1
        return data_labels

    def save_tt(self, data_clean):
        print("--- salve tt ---")
        with open("apps/pln/services/save_tt.txt", "w") as file:
            file.write(str(data_clean))

    def data_clean_tt(self, X):
        print("--- data clean tt ---")
        nlp = sp.load("en_core_web_sm")

        data_clean = [clean_tweets2(clean_tweets(tweet), nlp) for tweet in X]
        return data_clean

    def token(self, data_clean):
        print("--- token ---")
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            data_clean, target_vocab_size=2**16)
        vocab_fname = "apps/pln/services/ttVocab"
        tokenizer.save_to_file(vocab_fname)
        return tokenizer

    def max_len_data_inputs(self, data_inputs):
        print("--- max len data inputs ---")
        max_len = max([len(sentence) for sentence in data_inputs])
        return max_len

    def data_inputs_pad_sequences(self, data_inputs, max_len):
        print("--- data_inputs pad sequences ---")
        data_inputs = tf.keras.preprocessing.sequence.pad_sequences(
            data_inputs, value=0, padding="post", maxlen=max_len)
        return data_inputs

    def data_input(self, tokenizer, data_clean):
        print("-- data input --")
        data_inputs = [tokenizer.encode(sentence) for sentence in data_clean]
        return data_inputs, tokenizer

    def train_test(self, data):
        print("--- train test ---")
        X = data.iloc[:, 1].values
        y = data.iloc[:, 0].values
        # trabalhando so com 15% da base de 1.6m, (drop 85 da base)
        test_size = 0.85
        # stratify, amostram estratificada, mandento a proporção,
        #  (pagina 43 livro)
        X, _, y, _ = train_test_split(X, y, test_size=test_size, stratify=y)
        return X, y

    def list_txt_data_clean(self):
        print("-- list txt data clean ---")
        with open("apps/pln/services/save_tt.txt", "r") as data:
            data_list = eval(data.read())
        return data_list

    def main(self):
        print("-- main --")
        data = self.train()
        data = self.data_drop(data)
        X, y = self.train_test(data)

        data_labels = self.data_labels(y)

        data_clean = self.data_clean_tt(X)
        self.save_tt(data_clean)
        data_clean = self.list_txt_data_clean()

        tokenizer = self.token(data_clean)
        vocab_fname = "apps/pln/services/ttVocab"
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.load_from_file(
            vocab_fname)

        data_inputs, tokenizer = self.data_input(tokenizer, data_clean)
        max_len = self.max_len_data_inputs(data_inputs)
        data_inputs = self.data_inputs_pad_sequences(data_inputs, max_len)

        train_inputs, test_inputs, train_labels, test_labels = train_test_split(
            data_inputs, data_labels, test_size=0.2, stratify=data_labels)

        vocab_size = tokenizer.vocab_size
        emb_dim = 200
        nb_filters = 100
        ffn_units = 256
        batch_size = 64
        nb_classes = len(set(train_labels))
        dropout_rate = 0.2
        nb_epochs = 5

        Dcnn = DCNN(
            vocab_size=vocab_size,
            emb_dim=emb_dim,
            nb_filters=nb_filters,
            ffn_units=ffn_units,
            nb_classes=nb_classes,
            dropout_rate=dropout_rate,
        )

        if nb_classes == 2:
            Dcnn.compile(loss="binary_crossentropy",
                         optimizer="adam",
                         metrics=["accuracy"])
        else:
            print("--- mais de 2 classes")
            Dcnn.compile(
                loss="sparse_categorical_crossentropy",
                optimizer="adam",
                metrics=["accuracy"],
            )

        checkpoint_path = "apps/pln/checkpoint"
        ckpt = tf.train.Checkpoint(Dcnn=Dcnn)
        ckpt_manager = tf.train.CheckpointManager(ckpt,
                                                  checkpoint_path,
                                                  max_to_keep=5)

        if ckpt_manager.latest_checkpoint:
            ckpt.restore(ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored")

        Dcnn.fit(
            train_inputs,
            train_labels,
            batch_size=batch_size,
            epochs=nb_epochs,
            verbose=1,
            validation_split=0.10,
        )
        ckpt_manager.save()

        print("-- evaluate --")
        results = Dcnn.evaluate(test_inputs,
                                test_labels,
                                batch_size=batch_size)
        print(results)

        print("-- y_pred_test ---")
        y_pred_test = Dcnn.predict(test_inputs)
        print(y_pred_test)

        y_pred_test = y_pred_test > 0.5
        print(y_pred_test)

        print("--- matrix de confusão")
        cm = confusion_matrix(test_labels, y_pred_test)
        print(cm)

        print("--- salve ---")
        path = "apps/pln/weights_folder/my_weights"
        Dcnn.save_weights(path, save_format="tf")
        print("Model Saved!")

        print()
        print("---------- testes -------------------")
        text = "i hate you"

        vocab_fname = "apps/pln/services/ttVocab"
        encoder = tfds.deprecated.text.SubwordTextEncoder.load_from_file(
            vocab_fname)
        text = encoder.encode(text)
        print("-" * 50)
        value = Dcnn(np.array([text]), training=False).numpy()
        print(value)


if __name__ == "__main__":
    main = Main()
    main.main()
