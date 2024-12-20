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

import pandas as pd
from scipy.special import comb
import tracemalloc
import psutil;
from datetime import datetime


def evaluate(groundtruth, parsedresult):
    """Evaluation function to benchmark log parsing accuracy

    Arguments
    ---------
        groundtruth : str
            file path of groundtruth structured csv file
        parsedresult : str
            file path of parsed structured csv file

    Returns
    -------
        f_measure : float
        accuracy : float
    """
    df_groundtruth = pd.read_csv(groundtruth)
    df_parsedlog = pd.read_csv(parsedresult)
    # Remove invalid groundtruth event Ids
    non_empty_log_ids = df_groundtruth[~df_groundtruth["EventId"].isnull()].index
    df_groundtruth = df_groundtruth.loc[non_empty_log_ids]
    df_parsedlog = df_parsedlog.loc[non_empty_log_ids]
    (precision, recall, f_measure, accuracy) = get_accuracy(
        df_groundtruth["EventId"], df_parsedlog["EventId"]
    )
    print(
        "Precision: {:.4f}, Recall: {:.4f}, F1_measure: {:.4f}, Parsing_Accuracy: {:.4f}".format(
            precision, recall, f_measure, accuracy
        )
    )
    return f_measure, accuracy


def get_accuracy(series_groundtruth, series_parsedlog, debug=False):
    """Compute accuracy metrics between log parsing results and ground truth

    Arguments
    ---------
        series_groundtruth : pandas.Series
            A sequence of groundtruth event Ids
        series_parsedlog : pandas.Series
            A sequence of parsed event Ids
        debug : bool, default False
            print error log messages when set to True

    Returns
    -------
        precision : float
        recall : float
        f_measure : float
        accuracy : float
    """
    series_groundtruth_valuecounts = series_groundtruth.value_counts()
    real_pairs = 0
    for count in series_groundtruth_valuecounts:
        if count > 1:
            real_pairs += comb(count, 2)

    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    parsed_pairs = 0
    for count in series_parsedlog_valuecounts:
        if count > 1:
            parsed_pairs += comb(count, 2)

    accurate_pairs = 0
    accurate_events = 0  # determine how many lines are correctly parsed
    for parsed_eventId in series_parsedlog_valuecounts.index:
        logIds = series_parsedlog[series_parsedlog == parsed_eventId].index
        series_groundtruth_logId_valuecounts = series_groundtruth[logIds].value_counts()
        error_eventIds = (
            parsed_eventId,
            series_groundtruth_logId_valuecounts.index.tolist(),
        )
        error = True
        if series_groundtruth_logId_valuecounts.size == 1:
            groundtruth_eventId = series_groundtruth_logId_valuecounts.index[0]
            if (
                logIds.size
                == series_groundtruth[series_groundtruth == groundtruth_eventId].size
            ):
                accurate_events += logIds.size
                error = False
        if error and debug:
            print(
                "(parsed_eventId, groundtruth_eventId) =",
                error_eventIds,
                "failed",
                logIds.size,
                "messages",
            )
        for count in series_groundtruth_logId_valuecounts:
            if count > 1:
                accurate_pairs += comb(count, 2)

    precision = float(accurate_pairs) / parsed_pairs
    recall = float(accurate_pairs) / real_pairs
    f_measure = 2 * precision * recall / (precision + recall)
    accuracy = float(accurate_events) / series_groundtruth.size
    return precision, recall, f_measure, accuracy

def benchmark_time(dataset, LogParser, log_file, parsing_times=10, **kwargs):
    benchmark_result = []
    print("\n=== Evaluation on %s ===" % dataset)
    total_time = []
    for _ in range(parsing_times):
        parser = LogParser(**kwargs)
        start_time = datetime.now()
        parser.parse(log_file)
        end_time = datetime.now()
        total_time.append((end_time - start_time).total_seconds())
    delta_series = pd.Series(total_time)
    mean_time = delta_series.mean()
    std_time = delta_series.std()
    benchmark_result.append([dataset, mean_time, std_time])
    return benchmark_result

def benchmark_memory(dataset, LogParser, log_file, parsing_times=10, **kwargs):
    benchmark_result = []
    total_memo = []
    for _ in range(parsing_times):        
        parser = LogParser(**kwargs)
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
    return benchmark_result

def benchmark_cpu(dataset, LogParser, log_file, parsing_times=10, **kwargs):
    benchmark_result = []
    total_cpu = []
    for _ in range(parsing_times):
        parser = LogParser(**kwargs)
        start_cpu = psutil.cpu_percent(interval=1.0)
        print(start_cpu)
        parser.parse(log_file)
        cpu_percentage = psutil.cpu_percent(interval=None)
        total_cpu.append(cpu_percentage)
        delta_series = pd.Series(total_cpu)
        mean_cpu = delta_series.mean()
        std_cpu = delta_series.std()
        benchmark_result.append([dataset, mean_cpu, std_cpu])