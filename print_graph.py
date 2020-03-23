if __name__ == '__main__':
    import sys, tfutil
    model = sys.argv[1] if len(sys.argv) >=2 else 'model.pb'
    tfutil.print_graph(model)
