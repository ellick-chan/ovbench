import tensorflow as tf
import numpy as np

def save_keras_as_pb(m, pbfile):
    sess = tf.compat.v1.keras.backend.get_session()
    save_tf_as_pb(pbfile, sess, m.output.op.name)

def save_tf_as_pb(pbfile, sess, output_op):
    from tensorflow.python.framework import graph_util
    from tensorflow.python.framework import graph_io    
    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), [output_op])
    graph_io.write_graph(constant_graph, '.', pbfile, as_text=False)

with tf.compat.v1.Session() as sess:
    tf.keras.backend.set_learning_phase(0)
    model = tf.keras.applications.ResNet50(weights=None)
    model.compile(optimizer='sgd', loss='mse')
    res = model.predict(np.zeros([1,224,224,3]))
    print("Classification:", np.argmax(res))
    save_keras_as_pb(model, 'model.pb')
