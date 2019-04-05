from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class LibsndfileConan(ConanFile):
    name = "libsndfile"
    version = "1.0.28"
    license = "LGPL-2.1"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libsndfile here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    url_base = "http://www.mega-nerd.com/libsndfile/files/"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    def source(self):
        if self.settings.os == "Windows":
            pass
        else:
            url = self.url_base + "libsndfile-%s.tar.gz" % self.version
            sha256 = "1ff33929f042fa333aed1e8923aa628c3ee9e1eb85512686c55092d1e5a9dfa9"
            tools.get(url, sha256=sha256)
            os.rename("libsndfile-" + self.version, "src")

    def build(self):
        if self.settings.os == "Windows":
            if self.settings.arch == "x86":
                bin_url = self.url_base + "libsndfile-%s-w32.zip" % self.version
                bin_sha256 = "a73e1a8f87207e121a78e7cfbfe758d3ad15a28a37e4ca0e96d43348d53a2a1f"
            elif self.settings.arch == "x86_64":
                bin_url = self.url_base + "libsndfile-%s-w64.zip" % self.version
                bin_sha256 = "b885e97c797c39127d7d252be0da704a8bbdb97948b562d95cd5b8821d2b42ba"
            else:
                raise Exception("Binary does not exist for these settings")
            tools.get(bin_url, sha256=bin_sha256)
        else:
            with tools.chdir("src"):
                env_build = AutoToolsBuildEnvironment(self)
                args = [
                    "--disable-static"
                ]
                env_build.configure(args=args)
                env_build.make()
                env_build.install()


    def package(self):
        if self.settings.os == "Windows":
            self.copy("*")
        else:
            pass

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libsndfile-1"]
        else:
            self.cpp_info.libs = ["sndfile"]
    
    def package_id(self):
        if (self.settings.os == "Windows"):
            del self.info.settings.compiler
            del self.info.settings.build_type
