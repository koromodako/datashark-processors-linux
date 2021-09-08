"""Datashark TSKAPE Processor
"""
from typing import List
from pathlib import Path
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.processor import ProcessorInterface, ProcessorError
from datashark_core.model.api import Kind, System, ProcessorArgument

NAME = 'linux_tskape'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class TSKAPEProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Run tskape on given filepath"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = []
    DESCRIPTION = """
    Run tskape on given filepath
    """

    async def _run(self, arguments: List[ProcessorArgument]):
        """Process a file using tskape"""
        # TODO: perform artifact processing here
        print(arguments)
        # commit data added by plugin (if needed)
        #self.session.commit()
