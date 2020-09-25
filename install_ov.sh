echo deb https://apt.repos.intel.com/openvino/2020 all main > /etc/apt/sources.list.d/openvino.list
apt update
apt install -y intel-openvino-dev-ubuntu18
