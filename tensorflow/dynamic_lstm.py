import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib import rnn
import numpy as np


def lstm(x, batch_size):
    output_size = 10
    lstm_size = 28

    x = tf.transpose(x, (0, 2, 1))

    lstm = rnn.BasicLSTMCell(lstm_size, forget_bias=1, state_is_tuple=True)
    outputs, states = tf.nn.dynamic_rnn(lstm, x, dtype=tf.float32, sequence_length=batch_size)
    outputs = tf.convert_to_tensor(outputs[-1])
    return tf.layers.dense(outputs, output_size, activation=tf.nn.relu, use_bias=True)


def train():

    mnist = input_data.read_data_sets("/home/mxxmhh/MNIST_data", one_hot=True)

    train_batch_size = 128
    test_batch_size = 1024
    learning_rate = 0.001
    episodes = 10

    x = tf.placeholder(tf.float32, [None, 28, 28])
    y = tf.placeholder(tf.float32, [None, 10])
    batch_size = tf.placeholder(tf.int32)

    predicted_y = lstm(x, batch_size)
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predicted_y, labels=y))
    optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate, decay=0.9).minimize(loss)

    correct_prediction = tf.equal(tf.argmax(predicted_y, 1), tf.argmax(y, 1))
    # tf.cast改变Tensor的类型
    predict_accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

    sess_conf = tf.ConfigProto()
    sess_conf.gpu_options.allow_growth = True

    with tf.Session(config=sess_conf) as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(episodes):
            train_accuracy = 0
            epoches = mnist.train.num_examples // train_batch_size
            for j in range(epoches):
                batch_xs, batch_ys = mnist.train.next_batch(train_batch_size)
                batch_xs = np.reshape(np.array(batch_xs), [train_batch_size, 28, 28])
                batch_ys = np.reshape(np.array(batch_ys), [train_batch_size, 10])
                _, accuracy = sess.run([optimizer, predict_accuracy],
                                       feed_dict={x: batch_xs, y:batch_ys, batch_size: train_batch_size})
                train_accuracy += accuracy
            train_accuracy = train_accuracy / epoches
            # print(total_accuracy)

            valid_accuracy = 0
            epoches = mnist.validation.num_examples// test_batch_size
            for j in range(epoches):
                batch_xs, batch_ys = mnist.validation.next_batch(test_batch_size)
                batch_xs = np.reshape(np.array(batch_xs), [test_batch_size, 28, 28])
                batch_ys = np.reshape(np.array(batch_ys), [test_batch_size, 10])
                accuracy = sess.run(predict_accuracy,
                                    feed_dict={x: batch_xs, y: batch_ys, batch_size: test_batch_size})
                valid_accuracy += accuracy
            valid_accuracy = valid_accuracy / epoches
            print("Episodes ", i, ": train accuracy: ", train_accuracy, ", valid_accuracy: ", valid_accuracy)


if __name__ == "__main__":
    train()
