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

from stats.data import ImportType
from stats.data import Provenance
from stats.data import Source
from stats.data import StatVar

_INPUT_FILES_FIELD = "inputFiles"
_IMPORT_TYPE_FIELD = "importType"
_ENTITY_TYPE_FIELD = "entityType"
_IGNORE_COLUMNS_FIELD = "ignoreColumns"
_VARIABLES_FIELD = "variables"
_NAME_FIELD = "name"
_DESCRIPTION_FIELD = "description"
_NL_SENTENCES_FIELD = "nlSentences"
_GROUP_FIELD = "group"
_SOURCES_FIELD = "sources"
_PROVENANCES_FIELD = "provenances"
_URL_FIELD = "url"
_PROVENANCE_FIELD = "provenance"
_DATABASE_FIELD = "database"


class Config:
  """A wrapper around the import config specified via config.json.

    It provides convenience methods for accessing parameters from the config.
    """

  def __init__(self, data: dict) -> None:
    self.data = data
    # dict from provenance name to Provenance
    self.provenances: dict[str, Provenance] = {}
    # dict from provenance name to Source
    self.provenance_sources: dict[str, Source] = {}
    self._parse_provenances_and_sources()

  def import_type(self, input_file_name: str) -> ImportType:
    import_type_str = self._input_file(input_file_name).get(_IMPORT_TYPE_FIELD)
    if not import_type_str:
      return ImportType.OBSERVATIONS
    if import_type_str not in iter(ImportType):
      raise ValueError(
          f"Unsupported import type: {import_type_str} ({input_file_name})")
    return ImportType(import_type_str)

  def variable(self, variable_name: str) -> StatVar:
    var_cfg = self.data.get(_VARIABLES_FIELD, {}).get(variable_name, {})
    return StatVar(
        "",
        var_cfg.get(_NAME_FIELD, variable_name),
        description=var_cfg.get(_DESCRIPTION_FIELD, ""),
        nl_sentences=var_cfg.get(_NL_SENTENCES_FIELD, []),
        group_path=var_cfg.get(_GROUP_FIELD, ""),
    )

  def entity_type(self, input_file_name: str) -> str:
    return self._input_file(input_file_name).get(_ENTITY_TYPE_FIELD, "")

  def ignore_columns(self, input_file_name: str) -> list[str]:
    return self._input_file(input_file_name).get(_IGNORE_COLUMNS_FIELD, [])

  def provenance_name(self, input_file_name: str) -> str:
    return self._input_file(input_file_name).get(_PROVENANCE_FIELD,
                                                 input_file_name)

  def database(self) -> dict:
    return self.data.get(_DATABASE_FIELD)

  def _input_file(self, input_file_name: str) -> dict:
    return self.data.get(_INPUT_FILES_FIELD, {}).get(input_file_name, {})

  def _parse_provenances_and_sources(self):
    sources_cfg = self.data.get(_SOURCES_FIELD, {})
    for source_name, source_cfg in sources_cfg.items():
      source = Source(id="",
                      name=source_name,
                      url=source_cfg.get(_URL_FIELD, ""))
      provenances = source_cfg.get(_PROVENANCES_FIELD, {})
      for prov_name, prov_url in provenances.items():
        provenance = Provenance(id="",
                                source_id="",
                                name=prov_name,
                                url=prov_url)
        self.provenances[prov_name] = provenance
        self.provenance_sources[prov_name] = source
