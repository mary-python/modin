from setuptools import setup, find_packages
import versioneer

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

dask_deps = ["dask>=2.22.0", "distributed>=2.22.0"]
ray_deps = ["ray[default]>=1.13.0", "pyarrow"]
unidist_deps = ["unidist[mpi]>=0.2.1"]
remote_deps = ["rpyc==4.1.5", "cloudpickle", "boto3"]
spreadsheet_deps = ["modin-spreadsheet>=0.1.0"]
sql_deps = ["dfsql>=0.4.2", "pyparsing<=2.4.7"]
all_deps = dask_deps + ray_deps + unidist_deps + remote_deps + spreadsheet_deps

# Distribute 'modin-autoimport-pandas.pth' along with binary and source distributions.
# This file provides the "import pandas before Ray init" feature if specific
# environment variable is set (see https://github.com/modin-project/modin/issues/4564).
cmdclass = versioneer.get_cmdclass()
extra_files = ["modin-autoimport-pandas.pth"]


class AddPthFileBuild(cmdclass["build_py"]):
    def _get_data_files(self):
        return (super()._get_data_files() or []) + [
            (".", ".", self.build_lib, extra_files)
        ]


class AddPthFileSDist(cmdclass["sdist"]):
    def make_distribution(self):
        self.filelist.extend(extra_files)
        return super().make_distribution()


cmdclass["build_py"] = AddPthFileBuild
cmdclass["sdist"] = AddPthFileSDist

setup(
    name="modin",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    description="Modin: Make your pandas code run faster by changing one line of code.",
    packages=find_packages(exclude=["scripts", "scripts.*"]),
    include_package_data=True,
    license="Apache 2",
    url="https://github.com/modin-project/modin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas==2.0.2",
        "packaging",
        "numpy>=1.18.5",
        "fsspec",
        "psutil",
    ],
    extras_require={
        # can be installed by pip install modin[dask]
        "dask": dask_deps,
        "ray": ray_deps,
        "unidist": unidist_deps,
        "remote": remote_deps,
        "spreadsheet": spreadsheet_deps,
        "sql": sql_deps,
        "all": all_deps,
    },
    python_requires=">=3.8",
)
