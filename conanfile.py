from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class GitinstallerConan(ConanFile):
    name = "git_installer"
    version = "2.29.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    homepage = "https://www.github.com/git/git"
    windows_homepage = "https://www.github.com/git-for-windows/git"
    description = "<Description of Gitinstaller here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os_build", "compiler", "arch", "arch_build"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    _conan_git_arch = {
        "x86": "32-bit",
        "x86_64": "64-bit"
        }
        
    def source(self):
        if self.settings.os_build == "Windows":
            self.filename = "PortableGit-{0}-{1}.7z.exe".format(self.version, self._conan_git_arch[str(self.settings.arch_build)])
            tools.download("{0}/releases/download/v{1}.windows.1/{2}".format(self.windows_homepage, self.version, self.filename), filename=self.filename)
        else:
            tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
            os.rename("git-%s" % self.version, self._source_subfolder)
    def _configureAutotools(self):
        with tools.chdir(self._source_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make(target="configure")
            autotools.configure(args=["LDFLAGS=-pthread"])
        return autotools
        
    def build(self):
        if self.settings.os_build == "Windows":
            self.run(self.filename + " -y -gm2 -InstallPath=\"./\"")
        elif self.settings.os_build == "Linux":
            autotools = self._configureAutotools()
            with tools.chdir(self._source_subfolder):
                autotools.make(target="all")

    def package(self):
        if self.settings.os_build == "Windows":
            self.copy("*", dst="", src="PortableGit")
        elif self.settings.os_build == "Linux":
            autotools = self._configureAutotools()
            with tools.chdir(self._source_subfolder):
                autotools.install()

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        if not self.settings.os_build == "Windows":
            self.cpp_info.cflags = ["-pthread"]
        
    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()

    def requirements(self):
    # Or add a new requirement!
        if self.settings.os_build == "Linux":
            self.requires("libiconv/1.16")
            self.requires("expat/2.2.10")
            self.requires("openssl/1.1.1h")
            self.requires("zlib/1.2.11")
            self.requires("libcurl/7.73.0")