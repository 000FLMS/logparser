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


import re
import os
import pandas as pd
import hashlib
from datetime import datetime

class LogParser:
    def __init__(
        self,
        log_format,
        indir="./",
        outdir="./result/",
        rex=[],
        keep_parameters=True,
    ):
        """
        Log Parser using simple regex to remove letters and digits.

        Attributes
        ----------
        log_format : str
            The format of the log lines.
        indir : str
            Input directory where log file is located.
        outdir : str
            Output directory where parsing results will be stored.
        rex : list
            List of regular expressions for preprocessing log lines.
        keep_parameters : bool
            Whether to keep the parameters extracted from log lines.
        """
        self.path = indir
        self.log_format = log_format
        self.rex = rex
        self.keep_parameters = keep_parameters
        self.df_log = None
        self.log_name = None
        self.save_path = outdir

    def parse(self, log_name):
        print("Parsing file: " + os.path.join(self.path, log_name))
        start_time = datetime.now()
        self.log_name = log_name
        self.load_data()

        # Process each log message
        templates = {}
        event_ids = []
        event_templates = []
        parameter_lists = []

        for idx, row in self.df_log.iterrows():
            log_content = row['Content']
            # Apply preprocessing
            # preprocessed_content = self.preprocess(log_content)
            # Generate a template by removing letters and digits
            template = self.generate_template(log_content)
            # Extract parameters if required
            parameters = self.extract_parameters(log_content, template) if self.keep_parameters else []

            # Generate a unique EventId for the template
            template_str = template
            event_id = hashlib.md5(template_str.encode('utf-8')).hexdigest()[0:8]

            # Store the template and associated log IDs
            if event_id not in templates:
                templates[event_id] = {
                    'EventTemplate': template_str,
                    'Occurrences': 1,
                }
            else:
                templates[event_id]['Occurrences'] += 1

            # Append results
            event_ids.append(event_id)
            event_templates.append(template_str)
            if self.keep_parameters:
                parameter_lists.append(parameters)

            if (idx + 1) % 1000 == 0 or (idx + 1) == len(self.df_log):
                print(f"Processed {idx + 1} lines out of {len(self.df_log)}.")

        # Add results to the DataFrame
        self.df_log['EventId'] = event_ids
        self.df_log['EventTemplate'] = event_templates
        if self.keep_parameters:
            self.df_log['ParameterList'] = parameter_lists

        # Output the results
        self.output_results(templates)
        time_taken = datetime.now() - start_time
        print(f"Parsing done. [Time taken: {time_taken}]")

    def preprocess(self, line):
        # Apply custom regex patterns
        for regex in self.rex:
            line = re.sub(regex, '', line)
        return line

    def generate_template(self, line):
        # Remove all letters and digits
        template = re.sub(r'[a-zA-Z0-9]+', '', line)
        return template

    def extract_parameters(self, original_line, template_tokens):
        # Join the template tokens to form the template string
        template_str = template_tokens
        # Escape special regex characters in template
        template_regex = re.escape(template_str)
        # Replace spaces with regex whitespace matcher
        template_regex = template_regex.replace('\\ ', '\\s+')
        # Replace placeholders with regex groups
        template_regex = re.sub(r'\\\*', '(.*?)', template_regex)
        # Compile the regex
        pattern = re.compile('^' + template_regex + '$')
        # Match the original line
        match = pattern.match(original_line)
        if match:
            return list(match.groups())
        else:
            return []

    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(
            os.path.join(self.path, self.log_name), regex, headers, self.log_format
        )

    def generate_logformat_regex(self, logformat):
        """Function to generate regular expression to split log messages"""
        headers = []
        splitters = re.split(r"(<[^<>]+>)", logformat)
        regex = ""
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(" +", "\\\s+", splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip("<").strip(">")
                regex += "(?P<%s>.*?)" % header
                headers.append(header)
        regex = re.compile("^" + regex + "$")
        return headers, regex

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """Function to transform log file to dataframe"""
        log_messages = []
        linecount = 0
        with open(log_file, "r") as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    print("[Warning] Skip line: " + line)
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, "LineId", None)
        logdf["LineId"] = [i + 1 for i in range(linecount)]
        print("Total lines: ", len(logdf))
        return logdf

    def output_results(self, templates):
        """
        Output the parsing results to CSV files.
        """
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # Output structured log file
        self.df_log.to_csv(
            os.path.join(self.save_path, self.log_name + '_structured.csv'), index=False
        )

        # Output templates
        df_templates = pd.DataFrame(columns=['EventId', 'EventTemplate', 'Occurrences'])
        for event_id, info in templates.items():
            df_templates = df_templates._append({
                'EventId': event_id,
                'EventTemplate': info['EventTemplate'],
                'Occurrences': info['Occurrences'],
            }, ignore_index=True)

        df_templates.to_csv(
            os.path.join(self.save_path, self.log_name + '_templates.csv'),
            index=False
        )
