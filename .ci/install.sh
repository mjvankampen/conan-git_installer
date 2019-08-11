#!/bin/bash

set -e
set -x

pip install conan --upgrade
pip install conan_package_tools bincrafters_package_tools
conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

conan user
