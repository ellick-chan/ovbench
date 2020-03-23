def load_graph(frozen_graph_filename):
    import tensorflow as tf
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="prefix")
    return graph

def print_graph(model):
    print('Loading model:', model)
    graph = load_graph(model)
    ops = []
    for op in graph.get_operations(): 
        print(op.name, op.inputs, ' --> ',  op.outputs)
        ops.append((op.name, op.inputs, op.outputs))

    print('-'*50)
    print('First:', ops[0][0], ops[0][2][0].shape)
    print('Last:', ops[-1][0], ops[-1][2][0].shape)

if __name__ == '__main__':
    import sys
    model = sys.argv[1] if len(sys.argv) >=2 else 'model.pb'
    print_graph(model)
