#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    command = "conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan"
    builder = ConanMultiPackager(docker_entry_script=command)
    builder.add_common_builds(pure_c=True)
    builder.run()