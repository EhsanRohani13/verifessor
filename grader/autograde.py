#!/usr/bin/python
import glob
import tempfile
import subprocess
from os import path, makedirs
from shutil import copy, move
from csv import DictReader
from path_context import set_directory
import socket
from io import TextIOWrapper
from datetime import datetime


CONTAINER_IP=socket.gethostbyname(socket.gethostname())
WEBSERVER_PORT=8080

PROJECTS_DIR = "projects/*"
ICARUS_COMPILER = "iverilog"
TESTS_FOLDER = "tests"
OUTPUT_EXECUTABLE = "a.out"
VCDROM_HOSTING_DIRECTORY = "/root/vcdrom/node_modules/vcdrom/app/"
REPORT_FILE = "report.md"
CSV_KEYS = [
    "problem",
    "score",
    "possible",
    "reason",
]

# Code for report header
def generate_report_header(f: TextIOWrapper):
    f.write("# Homework Results\n\n")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"### Generated on {current_time}\n\n")

class TestResult:
    def __init__(self, number, score, max_score, error_message, description):
        self.number = number
        self.score = score
        self.max_score = max_score
        self.error_message = error_message
        self.description = description


class Project:
    # WIP
    """
    Title
    Description

    test results (of type list[TestResult])

    For each problem, a summary of what the problem is testing for. (a list of problem descriptions)

    vcd url
    """
    def __init__(self, title: str, description: str, test_results: list[TestResult], problem_descriptions, vcd_urls: list[str]):
        self.title = title
        self.description = description
        self.test_results = test_results
        self.problem_descriptions = problem_descriptions
        self.vcd_urls = vcd_urls


def generate_problem_summary_table(f: TextIOWrapper, test_results):
    def generate_problem_summary_row(f, test_result):
        percent_score = (test_result.score / test_result.max_score) * 100
        success_symbol = "🟢" if test_result.score == test_result.max_score else "🔴"
        f.write(f"| {success_symbol} {test_result.number} | {test_result.score}/{test_result.max_score} | {percent_score:.2f}% |")
        f.write("|\n")
    f.write("| Problem | Score | Percent Score | \n")
    f.write("| --- | --- | --- |\n")
    for test_result in test_results:
        generate_problem_summary_row(f, test_result)


def generate_reports(f: TextIOWrapper, test_results: list[TestResult], project_directory, vcds):
    if test_results is None:
        return
    project_name = path.basename(path.normpath(project_directory))
    f.write(f"## Project: {project_name}\n\n")
    generate_problem_summary_table(f, test_results)
    for vcd in vcds:
        f.write(f"{vcd}\n\n")


def build_binary(make_directory, output_directory: str):
    with set_directory(make_directory) as _:
        results = subprocess.run('make', capture_output=True)
        if results.returncode != 0:
            print(results.stderr.decode())
            return False
        move(OUTPUT_EXECUTABLE, output_directory)
        return True

# Run tests and return results
def run_tests() -> subprocess.CompletedProcess[bytes]:
    results = subprocess.run("./" + OUTPUT_EXECUTABLE, capture_output=True)            
    return results

def parse_results(results: subprocess.CompletedProcess[bytes]) -> list[TestResult]:
    csv_vals = []
    for line in results.stdout.decode().splitlines():
        if not line.startswith("VCD info"):
            csv_vals.append(line)
    raw_results = list(DictReader(csv_vals, CSV_KEYS))

    parsed_results = []
    for raw_result in raw_results:
        parsed_result = TestResult(
            number=int(raw_result["problem"]),
            score=float(raw_result["score"]),
            max_score=float(raw_result["possible"]),
            error_message=None,
            description="",
        )
        parsed_results.append(parsed_result)
    return parsed_results

# Copies all generated 
# Returns a list of vcdrom files in the vcdrom
def copy_vcds(vcd_directory) -> list[str]:
    vcd_list = []
    for vcd in glob.glob("*.vcd"):
        copy(vcd, vcd_directory)
        vcd_list.append(f"http://{CONTAINER_IP}:{WEBSERVER_PORT}/?local={path.basename(vcd_directory)}/{vcd}")
    return vcd_list

def grade(project_path) -> list[TestResult]:
    # Create the folder to store vcd files in
    vcd_directory = path.join(VCDROM_HOSTING_DIRECTORY, path.basename(project_path))
    makedirs(vcd_directory, exist_ok=True)

    with tempfile.TemporaryDirectory() as working_dir:
        if build_binary(project_path, working_dir):
            with set_directory(working_dir) as _:
                results = run_tests()
                vcds = copy_vcds(vcd_directory)
                return parse_results(results), vcds            
            

def generate_project_list(directory: str) -> list[str]:
    return sorted(glob.glob(directory))

def main():
    project_paths = generate_project_list(PROJECTS_DIR)
    
    with open(REPORT_FILE, "w") as f:
        generate_report_header(f)
        for project_path in project_paths:
            results = grade(project_path)
            # print(project_path, results)
            if results is not None:
                test_results, vcds = results
                generate_reports(f, test_results, project_path, vcds)

if __name__=="__main__":
    main()
