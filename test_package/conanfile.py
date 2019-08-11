import os

from conans import ConanFile, tools


class GitinstallerTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("git --version", run_environment=True)
