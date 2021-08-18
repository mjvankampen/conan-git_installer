from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class GitinstallerConan(ConanFile):
    name = "git_installer"
    version = "2.33.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    homepage = "https://www.github.com/git/git"
    windows_homepage = "https://www.github.com/git-for-windows/git"
    description = "<Description of Gitinstaller here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _autotools = None

    _conan_git_arch = {
        "x86": "32-bit",
        "x86_64": "64-bit"
        }
        
    def requirements(self):
    # Or add a new requirement!
        if self.settings.os == "Linux":
            self.requires("libiconv/1.16")
            self.requires("expat/2.4.1")
            self.requires("openssl/1.1.1k")
            self.requires("zlib/1.2.11")
            self.requires("libcurl/7.78.0")
            
    def source(self):
        if self.settings.os == "Windows":
            self.filename = "PortableGit-{0}-{1}.7z.exe".format(self.version, self._conan_git_arch[str(self.settings.arch)])
            tools.download("{0}/releases/download/v{1}.windows.1/{2}".format(self.windows_homepage, self.version, self.filename), filename=self.filename)
        else:
            tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
            os.rename("git-%s" % self.version, self._source_subfolder)
          

    def configure(self): 
        if self.settings.os == "Windows":
            del self.settings.compiler
            del self.settings.build_type
            del self.options.fPIC
            del self.options.shared
        
    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.libs.append("pthread")
            self._autotools.flags.append("-pthread")
            self.run("autoconf")
            config_args = []
            config_args.append("--with-iconv={}".format(tools.unix_path(self.deps_cpp_info["libiconv"].rootpath)))
            config_args.append("--with-curl={}".format(tools.unix_path(self.deps_cpp_info["libcurl"].rootpath)))
            self._autotools.configure(args=config_args)
        return self._autotools 
        
    def build(self):
        if self.settings.os == "Windows":
            self.run(self.filename + " -y -gm2 -InstallPath=\"./\"")
        elif self.settings.os == "Linux":
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.make()

    def package(self):
        if self.settings.os == "Windows":
            self.copy("*", dst="", src="PortableGit")
        elif self.settings.os == "Linux":
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.install()

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        if self.settings.os == "Linux":
            self.cpp_info.libs = tools.collect_libs(self)
            self.cpp_info.system_libs.extend(["pthread"])
            self.cpp_info.cflags.extend(["-pthread"])
            self.cpp_info.cxxflags.extend(["-pthread"])
