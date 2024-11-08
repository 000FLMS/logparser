# =========================================================================
# Copyright (C) 2016-2023 LOGPAI (https://github.com/logpai).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

import sys

sys.path.append("../../")
from logparser.Spell import LogParser
from logparser.utils import evaluator
from logparser.utils import const
import os
import pandas as pd
from datetime import datetime
import tracemalloc

output_dir = "Spell_result/"  # The output directory of parsing results

benchmark_settings = {
    "HDFS": {
        "log_file": "HDFS/HDFS_2k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "tau": 0.7,
    },
    "Hadoop": {
        "log_file": "Hadoop/Hadoop_2k.log",
        "log_format": "<Date> <Time> <Level> \[<Process>\] <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.7,
    },
    "Spark": {
        "log_file": "Spark/Spark_2k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.55,
    },
    "Zookeeper": {
        "log_file": "Zookeeper/Zookeeper_2k.log",
        "log_format": "<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>",
        "regex": [r"(/|)(\d+\.){3}\d+(:\d+)?"],
        "tau": 0.7,
    },
    "BGL": {
        "log_file": "BGL/BGL_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"core\.\d+"],
        "tau": 0.75,
    },
    "HPC": {
        "log_file": "HPC/HPC_2k.log",
        "log_format": "<LogId> <Node> <Component> <State> <Time> <Flag> <Content>",
        "regex": [r"=\d+"],
        "tau": 0.65,
    },
    "Thunderbird": {
        "log_file": "Thunderbird/Thunderbird_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.5,
    },
    "Windows": {
        "log_file": "Windows/Windows_2k.log",
        "log_format": "<Date> <Time>, <Level>                  <Component>    <Content>",
        "regex": [r"0x.*?\s"],
        "tau": 0.7,
    },
    "Linux": {
        "log_file": "Linux/Linux_2k.log",
        "log_format": "<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\d{2}:\d{2}:\d{2}"],
        "tau": 0.55,
    },
    "Android": {
        "log_file": "Android/Android_2k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "tau": 0.95,
    },
    "HealthApp": {
        "log_file": "HealthApp/HealthApp_2k.log",
        "log_format": "<Time>\|<Component>\|<Pid>\|<Content>",
        "regex": [],
        "tau": 0.5,
    },
    "Apache": {
        "log_file": "Apache/Apache_2k.log",
        "log_format": "\[<Time>\] \[<Level>\] <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.6,
    },
    "Proxifier": {
        "log_file": "Proxifier/Proxifier_2k.log",
        "log_format": "\[<Time>\] <Program> - <Content>",
        "regex": [
            r"<\d+\ssec",
            r"([\w-]+\.)+[\w-]+(:\d+)?",
            r"\d{2}:\d{2}(:\d{2})*",
            r"[KGTM]B",
        ],
        "tau": 0.85,
    },
    "OpenSSH": {
        "log_file": "OpenSSH/OpenSSH_2k.log",
        "log_format": "<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.8,
    },
    "OpenStack": {
        "log_file": "OpenStack/OpenStack_2k.log",
        "log_format": "<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>",
        "regex": [r"((\d+\.){3}\d+,?)+", r"/.+?\s", r"\d+"],
        "tau": 0.9,
    },
    "Mac": {
        "log_file": "Mac/Mac_2k.log",
        "log_format": "<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>",
        "regex": [r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.6,
    },
}

def benchmark_accuracy():
    bechmark_result = []
    for dataset, setting in benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.corrected_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])

        parser = LogParser(
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting["regex"],
            tau=setting["tau"],
        )
        parser.parse(log_file)

        F1_measure, accuracy = evaluator.evaluate(
            groundtruth=os.path.join(indir, log_file + const.corrected_file_suffix),
            parsedresult=os.path.join(output_dir, log_file + const.input_file_suffix),
        )
        bechmark_result.append([dataset, F1_measure, accuracy])

    print("\n=== Overall evaluation results ===")
    df_result = pd.DataFrame(bechmark_result, columns=["Dataset", "F1_measure", "Accuracy"])
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Spell_bechmark_result.csv", float_format="%.6f")

def benchmark_time():
    benchmark_result = []
    parsing_times = 10
    for dataset, setting in const.android_benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.all_log_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        
        total_time = []
        for _ in range(parsing_times):
            parser = LogParser(
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting["regex"],
            tau=setting["tau"],
        )
            start_time = datetime.now()
            parser.parse(log_file)
            end_time = datetime.now()
            total_time.append((end_time - start_time).total_seconds())
        delta_series = pd.Series(total_time)
        mean_time = delta_series.mean()
        std_time = delta_series.std()
        benchmark_result.append([dataset, mean_time, std_time])

    print("\n=== Overall time results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "Mean", "Std"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Spell_android_time.csv", float_format="%.6f")

def benchmark_memory():
    benchmark_result = []
    parsing_times = 10
    for dataset, setting in const.bgl_benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.all_log_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        
        total_memo = []
        for _ in range(parsing_times):
            parser = LogParser(
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting["regex"],
            tau=setting["tau"],
        )
            tracemalloc.start()
            current, _ = tracemalloc.get_traced_memory()
            parser.parse(log_file)
            _, peak = tracemalloc.get_traced_memory()
            total_memo.append((peak - current) / 1024)
            tracemalloc.stop()
        delta_series = pd.Series(total_memo)
        mean_memo = delta_series.mean()
        std_memo = delta_series.std()
        benchmark_result.append([dataset, mean_memo, std_memo])

    print("\n=== Overall time results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "Mean", "Std"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Spell_bgl_memo.csv", float_format="%.6f")

if __name__ == "__main__":
    benchmark_time()
    # benchmark_memory()
