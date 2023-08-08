# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2023 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging
from typing import Any, Dict, List, Optional, Union

from mvt.android.artifacts.dumpsys_receivers import DumpsysReceiversArtifact

from .base import AndroidQFModule


class DumpsysReceivers(DumpsysReceiversArtifact, AndroidQFModule):
    """This module analyse dumpsys receivers"""

    def __init__(
        self,
        file_path: Optional[str] = None,
        target_path: Optional[str] = None,
        results_path: Optional[str] = None,
        module_options: Optional[dict] = None,
        log: logging.Logger = logging.getLogger(__name__),
        results: Union[List[Any], Dict[str, Any], None] = None,
    ) -> None:
        super().__init__(
            file_path=file_path,
            target_path=target_path,
            results_path=results_path,
            module_options=module_options,
            log=log,
            results=results,
        )

        self.results = results if results else {}

    def run(self) -> None:
        dumpsys_file = self._get_files_by_pattern("*/dumpsys.txt")
        if not dumpsys_file:
            return
        data = self._get_file_content(dumpsys_file[0])

        dumpsys_section = self.extract_dumpsys_section(
            data.decode("utf-8", errors="replace"), "DUMP OF SERVICE package:"
        )

        self.parse(dumpsys_section)

        self.log.info("Extracted receivers for %d intents", len(self.results))
