#!/usr/bin/python
import glob
import tempfile
from os import path, system, chdir, getcwd
import subprocess
from path_context import set_directory
from shutil import copy, copyfile
from random import randint


PROJECTS_DIR = "projects/*"
ICARUS_COMPILER = "iverilog"
TESTS_FOLDER = "tests"
OUTPUT_EXECUTABLE = "a.out"

VCDROM_HOSTING_DIRECTORY = "/root/vcdrom/node_modules/vcdrom/app/"


class Project:
    def __init__(self, project_path):
        self.path = project_path

    def grade(self):
        compilation_command = ["iverilog"]

        source_files = [
            x for x in glob.glob(path.join(self.path, "*.v"))
        ]

        if len(source_files) == 0:
            print(f"Skipping project {path.basename(self.path)}, as there are no source files.")
            return

        test_files = [
            x for x in glob.glob(path.join(self.path, TESTS_FOLDER, "*.v"))
        ]

        with tempfile.TemporaryDirectory() as working_dir:
            compilation_command.extend(["-o", path.join(working_dir, "a.out")])
            compilation_command.extend(source_files)
            compilation_command.extend(test_files)

            print(" ".join(compilation_command))
            subprocess.call(compilation_command)

            with set_directory(working_dir) as _:
                subprocess.call("./" + OUTPUT_EXECUTABLE)
                for vcd in glob.glob("*.vcd"):
                    copyfile(vcd, path.join(VCDROM_HOSTING_DIRECTORY, vcd))
                    print(f"http://172.17.0.2:8080/?local={vcd}")
                


def generate_project_list(directory: str) -> list[Project]:
    return list([
        Project(project_path) for project_path in sorted(glob.glob(directory))
    ])


def main():
    projects = generate_project_list(PROJECTS_DIR)
    for project in projects:
        project.grade()


if __name__=="__main__":
    main()
