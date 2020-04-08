# docker run -it -p 8888:8888 -v $PWD:/data -w /data --rm intel/oneapi-aikit /data/pykernel.sh

# Jupyter lab
pip install jupyterlab

# Tensorflow
/opt/intel/inteloneapi/tensorflow/latest/bin/pip install --user ipykernel
/opt/intel/inteloneapi/tensorflow/latest/bin/python -m ipykernel install --user --name tensorflow --display-name "Tensorflow"

# PyTorch
/opt/intel/inteloneapi/pytorch/latest/bin/pip install --user ipykernel
/opt/intel/inteloneapi/pytorch/latest/bin/python -m ipykernel install --user --name pytorch --display-name "PyTorch"

# OpenVINO
echo deb https://apt.repos.intel.com/openvino/2020 all main > /etc/apt/sources.list.d/openvino.list
apt update
apt install -y intel-openvino-dev-ubuntu18

# Delete extra kernels
jupyter kernelspec remove python3

# Launch Jupyter lab
jupyter lab --ip=0.0.0.0 --allow-root
