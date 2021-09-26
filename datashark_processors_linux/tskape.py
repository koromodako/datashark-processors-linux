"""Datashark TSKAPE Processor
"""
from typing import Dict
from asyncio.subprocess import PIPE, DEVNULL
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.processor import ProcessorInterface
from datashark_core.model.api import Kind, System, ProcessorArgument

NAME = 'linux_tskape'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class TSKAPEProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Run tskape on given filepath"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = [
        {
            'name': 'extract_to',
            'kind': Kind.PATH,
            'required': False,
            'description': "Extract matched filepath content to this directory",
        },
        {
            'name': 'log',
            'kind': Kind.PATH,
            'required': True,
            'description': "Log results to this file",
        },
        {

            'name': 'filepath',
            'kind': Kind.PATH,
            'required': True,
            'description': "File to process",
        },
        {
            'name': 'pattern_file',
            'kind': Kind.PATH,
            'required': True,
            'description': "File with patterns to find, one python re compatible pattern per line",
        },
    ]
    DESCRIPTION = """
    Run tskape on given filepath
    """

    async def _run(self, arguments: Dict[str, ProcessorArgument]):
        """Process a file using tskape"""
        # invoke subprocess
        proc = await self._start_subprocess(
            'datashark.processors.tskape.bin',
            ['find'],
            [
                # optional
                ('extract_to', '--extract-to'),
                ('log', '--log'),
                # positional
                ('filepath', None),
                ('pattern_file', None),
            ],
            arguments,
            stdout=DEVNULL,
            stderr=PIPE,
        )
        await self._handle_communicating_process(proc)
