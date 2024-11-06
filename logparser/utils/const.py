input_dir = "../../data/loghub_2k/"  # The input directory of log file
input_file_suffix = "_structured.csv"
corrected_input_dir = "../../data/loghub_2k_corrected/"
corrected_file_suffix = "_structured_corrected.csv"
all_log_input_dir = "../../data/loghub_all/"

general_regex = [
    r"(\d+\.){3}\d+(:\d+)?",
    r"((\d+\.){3}\d+,?)+",
    r"(/[\w-]+)+",
    r"([\w-]+\.){2,}[\w-]+",
    r"\d{2}:\d{2}(:\d{2})*",
    r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
]



spark_benchmark_settings = {
    "Spark_10k": {
        "log_file": "Spark/Spark_10k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    "Spark_50k": {
        "log_file": "Spark/Spark_50k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    "Spark_100k": {
        "log_file": "Spark/Spark_100k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "delimiter": [],
        "theshold": 4,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    # "Spark_500k": {
    #     "log_file": "Spark/Spark_500k.log",
    #     "log_format": "<Date> <Time> <Level> <Component>: <Content>",
    #     "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
    #     "delimiter": [],
    #     "theshold": 4,
    #     "minEventCount": 2,
    #     "merge_percent": 0.5,
    #     "st": 0.5,
    #     "depth": 4,
    # }
}

hdfs_benchmark_settings = {
    "HDFS_10k": {
        "log_file": "HDFS/HDFS_10k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    "HDFS_50k": {
        "log_file": "HDFS/HDFS_50k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    "HDFS_100k": {
        "log_file": "HDFS/HDFS_100k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
        "delimiter": [""],
        "theshold": 2,
        "minEventCount": 2,
        "merge_percent": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    # "HDFS_500k": {
    #     "log_file": "HDFS/HDFS_500k.log",
    #     "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
    #     "regex": [r"blk_-?\d+", r"(\d+\.){3}\d+(:\d+)?"],
    #     "delimiter": [""],
    #     "theshold": 2,
    #     "minEventCount": 2,
    #     "merge_percent": 0.5,
    #     "st": 0.5,
    #     "depth": 4,
    # },
}

android_benchmark_settings = {
    "Android_10k": {
        "log_file": "Android/Android_10k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "minEventCount": 2,
        "merge_percent": 0.6,
        "st": 0.2,
        "depth": 6,
        "delimiter": [r""],
        "theshold": 5,
        "minEventCount": 2,
        "merge_percent": 0.6,
    },
    "Android_50k": {
        "log_file": "Android/Android_50k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "minEventCount": 2,
        "merge_percent": 0.6,
        "st": 0.2,
        "depth": 6,
        "delimiter": [r""],
        "theshold": 5,
        "minEventCount": 2,
        "merge_percent": 0.6,
    },
    "Android_100k": {
        "log_file": "Android/Android_100k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "minEventCount": 2,
        "merge_percent": 0.6,
        "st": 0.2,
        "depth": 6,
        "delimiter": [r""],
        "theshold": 5,
        "minEventCount": 2,
        "merge_percent": 0.6,
    },
}

bgl_benchmark_settings = {
    "BGL_10k": {
        "log_file": "BGL/BGL_10k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"core\.\d+"],
        "st": 0.5,
        "depth": 4,
        "delimiter": [],
        "theshold": 6,
        "minEventCount": 2,
        "merge_percent": 0.5,
    },
    "BGL_50k": {
        "log_file": "BGL/BGL_50k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"core\.\d+"],
        "st": 0.5,
        "depth": 4,
        "delimiter": [],
        "theshold": 6,
        "minEventCount": 2,
        "merge_percent": 0.5,
    },
    "BGL_100k": {
        "log_file": "BGL/BGL_100k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"core\.\d+"],
        "st": 0.5,
        "depth": 4,
        "delimiter": [],
        "theshold": 6,
        "minEventCount": 2,
        "merge_percent": 0.5,
    },

    # "BGL_500k": {
    #     "log_file": "BGL/BGL_500k.log",
    #     "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
    #     "regex": [r"core\.\d+"],
    #     "st": 0.5,
    #     "depth": 4,
    # },
}