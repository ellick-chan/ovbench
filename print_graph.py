import tensorflow as tf

def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="prefix")
    return graph

graph = load_graph('model.pb')
for op in graph.get_operations(): 
    print(op.name, op.inputs[0] if len(op.inputs) > 0 else '', ' --> ',  op.outputs[0] if len(op.outputs) > 0 else '')