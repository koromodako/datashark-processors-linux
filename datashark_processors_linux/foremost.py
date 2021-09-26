"""Datashark Foremost Processor
"""
from typing import Dict
from asyncio.subprocess import PIPE, DEVNULL
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.processor import ProcessorInterface
from datashark_core.model.api import Kind, System, ProcessorArgument

NAME = 'linux_foremost'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class ForemostProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Run foremost on given filepath"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = [
        {
            'name': 'quick',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': "Enables quick mode. Search are performed on 512 byte boundaries",
        },
        {
            'name': 'audit_only',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': "Only write the audit file, do not write any detected files to the disk",
        },
        {
            'name': 'config',
            'kind': Kind.PATH,
            'required': False,
            'description': "Configuration file",
        },
        {
            'name': 'output_dir',
            'kind': Kind.PATH,
            'required': False,
            'description': "Output directory",
        },
        {
            'name': 'filepath',
            'kind': Kind.PATH,
            'required': True,
            'description': "File to process",
        },
    ]
    DESCRIPTION = """
    Run foremost on given filepath
    """

    async def _run(self, arguments: Dict[str, ProcessorArgument]):
        """Process a file using foremost"""
        # invoke subprocess
        proc = await self._start_subprocess(
            'datashark.processors.foremost.bin',
            ['-Q'],
            [
                # optional
                ('config', '-c'),
                ('audit_only', '-w'),
                ('output_dir', '-o'),
                ('filepath', '-i'),
                # positional
            ],
            arguments,
            stdout=DEVNULL,
            stderr=PIPE,
        )
        await self._handle_communicating_process(proc)
