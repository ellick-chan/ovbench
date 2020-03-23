if __name__ == '__main__':
    import tfutil
    shp = (1, 224, 224, 3)
    tfutil.run_tensorflow_pb('model.pb', 'input_1:0', 'fc1000/Softmax:0', shp)