import tensorflow as tf
import numpy as np

data        = np.zeros((1, 224, 224, 3))
input_node  = 'input_1:0'
output_node = 'fc1000/Softmax:0'

with tf.Session() as sess:
    options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()
    with open('model.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    
    input_tensor  = sess.graph.get_tensor_by_name(input_node)
    output_tensor = sess.graph.get_tensor_by_name(output_node)
    out = sess.run(output_tensor, feed_dict={input_tensor: data}, options=options, run_metadata=run_metadata)
    print('Output:', out.shape)

    from tensorflow.python.client import timeline
    fetched_timeline = timeline.Timeline(run_metadata.step_stats)
    chrome_trace     = fetched_timeline.generate_chrome_trace_format()
    with open('timeline.ctf.json', 'w') as f:
        f.write(chrome_trace)
        print('Wrote Tensorflow timeline')