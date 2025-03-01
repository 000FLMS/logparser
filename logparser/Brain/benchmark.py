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
from logparser import Brain
from logparser.utils import evaluator
from logparser.utils import const
import pandas as pd
import os


output_dir = "Brain_result/"  # The output directory of parsing results


general_threshold = 4
benchmark_settings = {
    "HDFS": {
        "log_file": "HDFS/HDFS_2k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
    },
    "Hadoop": {
        "log_file": "Hadoop/Hadoop_2k.log",
        "log_format": "<Date> <Time> <Level> \[<Process>\] <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "delimiter": [],
        "theshold": 6,
    },
    "Spark": {
        "log_file": "Spark/Spark_2k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
    },
    "Zookeeper": {
        "log_file": "Zookeeper/Zookeeper_2k.log",
        "log_format": "<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>",
        "regex": [r"(/|)(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [],
        "theshold": 3,
    },
    "BGL": {
        "log_file": "BGL/BGL_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"core\.\d+"],
        "delimiter": [],
        "theshold": 6,
    },
    "HPC": {
        "log_file": "HPC/HPC_2k.log",
        "log_format": "<LogId> <Node> <Component> <State> <Time> <Flag> <Content>",
        "regex": [],
        "delimiter": [],
        "theshold": 5,
    },
    "Thunderbird": {
        "log_file": "Thunderbird/Thunderbird_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "delimiter": [],
        "theshold": 3,
    },
    "Windows": {
        "log_file": "Windows/Windows_2k.log",
        "log_format": "<Date> <Time>, <Level>                  <Component>    <Content>",
        "regex": [r"0x.*?\s"],
        "delimiter": [],
        "theshold": 3,
    },
    "Linux": {
        "log_file": "Linux/Linux_2k.log",
        "log_format": "<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\d{2}:\d{2}:\d{2}", r"J([a-z]{2})"],
        "delimiter": [r""],
        "theshold": 4,
    },
    "Android": {
        "log_file": "Android/Android_2k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "delimiter": [r""],
        "theshold": 5,
    },
    "HealthApp": {
        "log_file": "HealthApp/HealthApp_2k.log",
        "log_format": "<Time>\|<Component>\|<Pid>\|<Content>",
        "regex": [],
        "delimiter": [r""],
        "theshold": 4,
    },
    "Apache": {
        "log_file": "Apache/Apache_2k.log",
        "log_format": "\[<Time>\] \[<Level>\] <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "delimiter": [],
        "theshold": 4,
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
        "delimiter": [],
        "theshold": 3,
    },
    "OpenSSH": {
        "log_file": "OpenSSH/OpenSSH_2k.log",
        "log_format": "<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 6,
    },
    "OpenStack": {
        "log_file": "OpenStack/OpenStack_2k.log",
        "log_format": "<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>",
        "regex": [r"((\d+\.){3}\d+,?)+", r"/.+?\s ", r"\d+"],
        "delimiter": [],
        "theshold": 5,
    },
    "Mac": {
        "log_file": "Mac/Mac_2k.log",
        "log_format": "<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>",
        "regex": [r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 5,
    },
}

spark_benchmark_settings = {
    "Spark_10k": {
        "log_file": "Spark/Spark_10k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
    },
    "Spark_50k": {
        "log_file": "Spark/Spark_50k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
    },
    "Spark_100k": {
        "log_file": "Spark/Spark_100k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
    },
    "Spark_500k": {
        "log_file": "Spark/Spark_500k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
    }
}

hdfs_benchmark_settings = {
    "HDFS_10k": {
        "log_file": "HDFS/HDFS_10k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
    },
    "HDFS_50k": {
        "log_file": "HDFS/HDFS_50k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
    },
    "HDFS_100k": {
        "log_file": "HDFS/HDFS_100k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
    },
    "HDFS_500k": {
        "log_file": "HDFS/HDFS_500k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
    },
}



def benchmark_accuracy():
    benchmark_result = []

    for dataset, setting in benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.corrected_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        parser = Brain.LogParser(
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting['regex'],
            # rex = general_regex,
            delimeter=setting['delimiter'],
            threshold=setting['theshold'],
            # threshold=general_threshold,
            logname=dataset,
        )
        parser.parse(log_file)

        F1_measure, accuracy = evaluator.evaluate(
            groundtruth=os.path.join(indir, log_file + const.corrected_file_suffix),
            parsedresult=os.path.join(output_dir, log_file + const.input_file_suffix),
        )
        benchmark_result.append([dataset, F1_measure, accuracy])

    print("\n=== Overall evaluation results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "F1_measure", "Accuracy"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Brain_bechmark_result.csv", float_format="%.6f")

def benchmark_time():
    benchmark_result = []
    for dataset, setting in const.android_benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.all_log_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        benchmark_result += evaluator.benchmark_time(
            dataset, Brain.LogParser, log_file, 10, 
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting['regex'],
            # rex = general_regex,
            delimeter=setting['delimiter'],
            threshold=setting['theshold'],
            # threshold=general_threshold,
            logname=dataset)

    print("\n=== Overall time results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "Mean", "Std"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Brain_android_time.csv", float_format="%.6f")

def benchmark_memory():
    benchmark_result = []
    for dataset, setting in const.android_benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.all_log_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        benchmark_result += evaluator.benchmark_memory(
            dataset, Brain.LogParser, log_file, 10, 
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting['regex'],
            # rex = general_regex,
            delimeter=setting['delimiter'],
            threshold=setting['theshold'],
            # threshold=general_threshold,
            logname=dataset)

    print("\n=== Overall time results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "Mean", "Std"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Brain_android_memo.csv", float_format="%.6f")

def benchmark_cpu():
    benchmark_result = []
    for dataset, setting in const.cpu_benchmark_settings.items():
        print("\n=== Evaluation on %s ===" % dataset)
        indir = os.path.join(const.all_log_input_dir, os.path.dirname(setting["log_file"]))
        log_file = os.path.basename(setting["log_file"])
        benchmark_result += evaluator.benchmark_cpu(
            dataset, Brain.LogParser, log_file, 5, 
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting['regex'],
            # rex = general_regex,
            delimeter=setting['delimiter'],
            threshold=setting['theshold'],
            # threshold=general_threshold,
            logname=dataset)

    print("\n=== Overall time results ===")
    df_result = pd.DataFrame(
        benchmark_result, columns=["Dataset", "Mean", "Std"]
    )
    df_result.set_index("Dataset", inplace=True)
    print(df_result)
    df_result.to_csv("Drain_cpu.csv", float_format="%.6f")


if __name__ == "__main__":
    # benchmark_accuracy()
    # benchmark_time()
    # benchmark_memory()
    benchmark_cpu()