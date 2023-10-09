# Copyright 2023 Google Inc.
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

import os
import sys
import constants
from importer import SimpleStatsImporter

# For importing util
_CODEDIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(_CODEDIR, "../"))

from util.filehandler import create_file_handler, FileHandler


class Runner:
    """Runs and coordinates all imports.
    """

    def __init__(
            self,
            input_path: str,
            output_dir: str,
            entity_type: str = None,
            ignore_columns: list[str] = list(),
    ) -> None:
        self.input_fh = create_file_handler(input_path)
        self.output_dir_fh = create_file_handler(output_dir)
        self.process_dir_fh = self.output_dir_fh.make_file(
            f"{constants.PROCESS_DIR_NAME}/")
        self.entity_type = entity_type
        self.ignore_columns = ignore_columns

        self.output_dir_fh.make_dirs()
        self.process_dir_fh.make_dirs()

    def run(self):
        # TODO: Add support for input file directory.
        self._run_single_import(input_file_fh=self.input_fh)

    def _run_single_import(self, input_file_fh: FileHandler):
        basename = input_file_fh.basename()
        observations_fh = self.output_dir_fh.make_file(
            f"{constants.OBSERVATIONS_FILE_NAME_PREFIX}_{basename}")
        debug_resolve_fh = self.process_dir_fh.make_file(
            f"{constants.DEBUG_RESOLVE_FILE_NAME_PREFIX}_{basename}")
        importer = SimpleStatsImporter(input_fh=input_file_fh,
                                       observations_fh=observations_fh,
                                       debug_resolve_fh=debug_resolve_fh,
                                       entity_type=self.entity_type,
                                       ignore_columns=self.ignore_columns)
        importer.do_import()
