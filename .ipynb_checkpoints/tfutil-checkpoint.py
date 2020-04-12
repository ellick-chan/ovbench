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

def run_tensorflow_pb(model, input_node, output_node, shape, timeline='timeline.ctf.json'):
    import tensorflow as tf
    import numpy as np

    print('Running Tensorflow timeline:', model, input_node, output_node, shape, timeline)
    data = np.zeros(shape)
    with tf.Session() as sess:
        options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        with open(model, 'rb') as f:
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

def read_timeline(fn, maxents=0):
    import json
    import pandas as pd
    with open(fn, 'r') as f:
        j = json.loads(f.read())
    allkeys = [list(js.keys()) for js in j['traceEvents']]
    allkeys = [item for sublist in allkeys for item in sublist]
    allkeys=sorted(set(allkeys))
    argkeys = [js['args'].keys() for js in j['traceEvents'] if 'args' in js]
    argkeys = sorted(set([item for sublist in argkeys for item in sublist]))
    argkeys = ['arg_' + k for k in argkeys]
    entries = []
    for i, e in enumerate(j['traceEvents']):
        if maxents !=0 and i > maxents: break
        ent = {}
        for k, v in e.items():
            if k == 'args':
                for a in v.keys():
                    ent['arg_' + a] = str(v[a])
            else:
                ent[k] = str(v)
        entries.append(ent)
    df = pd.DataFrame(entries)
    return df