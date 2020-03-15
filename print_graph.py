import tensorflow as tf

def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="prefix")
    return graph

graph = load_graph('model.pb')
ops = []
for op in graph.get_operations(): 
    print(op.name, op.inputs, ' --> ',  op.outputs)
    ops.append((op.name, op.inputs, op.outputs))

print('-'*50)
print('First:', ops[0])
print('Last:', ops[-1])