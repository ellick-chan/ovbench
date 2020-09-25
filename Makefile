# Name of the model file
TF_MODEL=model.pb
INPUT_SHAPE=[1,224,224,3]

# OpenVINO tag version
OV_BASE=openvino/ubuntu18_dev
OV_VERSION=latest
#OV_VERSION=2019_R3.1

# OpenVINO commands
DOCKER_CMD=docker run -it --rm -p 8888:8888 -v $(PWD):/data -w /data -u root $(OV_BASE):$(OV_VERSION)
DOCKER_GPU_CMD=docker run -it --device /dev/dri --rm -v $(PWD):/data -w /data -u root $(OV_BASE):$(OV_VERSION)
SOURCE_CMD=source /opt/intel/openvino/bin/setupvars.sh && ln -sf /opt/intel/openvino/deployment_tools/model_optimizer/mo.py && ln -sf /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py
APT_PREP=apt update 

MO_CONVERT=python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model $(TF_MODEL) --input_shape $(INPUT_SHAPE)

MO_CONV32=$(MO_CONVERT) --data_type=FP32 --model_name=model32
MO_CONV16=$(MO_CONVERT) --data_type=FP16 --model_name=model16

BENCHMARK=python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py 
BENCHMARK32=$(BENCHMARK) -m model32.xml -pc
BENCHMARK16=$(BENCHMARK) -m model16.xml -pc
BENCHMARKGPU=$(BENCHMARK) -d GPU -m model16.xml -pc
BENCHMARK8 =$(BENCHMARK) -m model32_i8.xml -pc

all: benchmark

resnet50:
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && python3 resnet50.py"

convert:
	echo "Converting model to FP32"
	$(DOCKER_CMD) /bin/bash -c "$(SOURCE_CMD) && cd /data && ls && $(MO_CONV32)"
	echo "Converting model to FP16"
	$(DOCKER_CMD) /bin/bash -c "$(SOURCE_CMD) && cd /data && ls && $(MO_CONV16)"

calibrate: convert
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && python3 /opt/intel/openvino/deployment_tools/tools/calibration_tool/calibrate.py -sm -m model32.xml"

benchmark8: calibrate
	echo "Benchmarking model in INT8"
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARK8)" | tee benchmark8.log

benchmark16: convert
	echo "Benchmarking model in FP16"
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARK16)" | tee benchmark16.log

benchmark: convert
	echo "Benchmarking model in FP32"
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARK32)" | tee benchmark.log

benchmarkgpu: convert
	echo "Benchmarking model in FP16 on GPU"
	$(DOCKER_GPU_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && cd /data && ls && $(BENCHMARKGPU)" | tee benchmark16.log

mmdnn:
	docker run -it --rm -w /data -v $(PWD):/data mmdnn/mmdnn:cpu.small

workbench:
	docker run -it --rm -p 0.0.0.0:5665:5665 -P -e PORT=5665 -v $PWD:/data -e PROXY_HOST_ADDRESS=0.0.0.0 -e http_proxy= -e https_proxy= -e no_proxy= openvino/workbench

print_graph:
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && python3 print_graph.py"

shell:
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && bash"

jupyter:
	$(DOCKER_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && DEBIAN_FRONTEND=noninteractive apt install -y jupyter-notebook libpython3.6 && jupyter notebook --port 8888 --ip 0.0.0.0 --allow-root"

gpushell:
	$(DOCKER_GPU_CMD) /bin/bash -c "$(APT_PREP) && $(SOURCE_CMD) && bash"

clean:
	rm -f model32*.* model16.* 

help:
	@echo "convert   - converts a model to FP32/FP16. Depends on OpenVINO version"
	@echo "benchmark - benchmarks a model and shows performance counters"
	@echo "calibrate - convert a model to INT8"
	@echo "benchmark8- benchmarks an INT8 model and shows performance counters"
	@echo "workbench - launches OpenVINO workbench web app"
	@echo "print_graph - prints Tensorflow graph layout"
	@echo "shell     - drops into an OpenVINO shell"
	@echo "clean     - clears working files"
