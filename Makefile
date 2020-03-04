# Name of the model file
TF_MODEL=model.pb
INPUT_SHAPE=[1,224,224,3]

# OpenVINO tag version
OV_BASE=openvino/ubuntu18_dev
OV_VERSION=latest
#OV_VERSION=2019_R3.1

# OpenVINO commands
DOCKER_CMD=docker run -it --rm -v $(PWD):/data -u root $(OV_BASE):$(OV_VERSION)
SOURCE_CMD=source /opt/intel/openvino/bin/setupvars.sh
APT_PREP=apt update && apt install -y libpython3.6

MO_CONVERT=python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model $(TF_MODEL) --input_shape $(INPUT_SHAPE)

MO_CONV32=$(MO_CONVERT) --data_type=FP32 --model_name=model32
MO_CONV16=$(MO_CONVERT) --data_type=FP16 --model_name=model16

BENCHMARK=python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py 
BENCHMARK32=$(BENCHMARK) -m model32.xml -pc
BENCHMARK16=$(BENCHMARK) -m model16.xml -pc

all: benchmark

convert:
	echo "Converting model to FP32"
	$(DOCKER_CMD) /bin/bash -c "$(SOURCE_CMD) && cd /data && ls && $(MO_CONV32)"
	echo "Converting model to FP16"
	$(DOCKER_CMD) /bin/bash -c "$(SOURCE_CMD) && cd /data && ls && $(MO_CONV16)"

benchmark: convert
	echo "Benchmarking model in FP32"
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARK32)"

	echo "Benchmarking model in FP16"
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARK16)"

clean:
	rm -f model32.* model16.*