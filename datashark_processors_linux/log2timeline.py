"""Datashark log2timeline.py Processor
"""
from typing import Dict
from asyncio.subprocess import PIPE, DEVNULL
from datashark_core.meta import ProcessorMeta
from datashark_core.logging import LOGGING_MANAGER
from datashark_core.datetime import now
from datashark_core.processor import ProcessorInterface
from datashark_core.model.api import Kind, System, ProcessorArgument
from datashark_core.filesystem import prepend_workdir, ensure_parent_dir

NAME = 'linux_log2timeline'
LOGGER = LOGGING_MANAGER.get_logger(NAME)


class Log2TimelineProcessor(ProcessorInterface, metaclass=ProcessorMeta):
    """Run log2timeline on given filepath"""

    NAME = NAME
    SYSTEM = System.LINUX
    ARGUMENTS = [
        {
            'name': 'artifact_definitions',
            'kind': Kind.PATH,
            'required': False,
            'description': """
                Path to a directory containing artifact definitions, which are .yaml files.
                Artifact definitions can be used to describe and quickly collect data of interest,
                such as specific files or Windows Registry keys
            """,
        },
        {
            'name': 'artifact_filters_file',
            'kind': Kind.PATH,
            'required': False,
            'description': """
                Names of forensic artifact definitions, provided in a file with one artifact name per line. Forensic
                artifacts are stored in .yaml files that are directly pulled from the artifact definitions project.
                You can also specify an artifacts yaml file (see artifact_definitions). Artifact definitions can be
                used to describe and quickly collect data of interest, such as specific files or Windows Registry keys
            """,
        },
        {
            'name': 'filter_file',
            'kind': Kind.PATH,
            'required': False,
            'description': """
                List of files to include for targeted collection of files to parse, one line per file path, setup is
                /path|file - where each element can contain either a variable set in the preprocessing stage or a
                regular expression
            """,
        },
        {
            'name': 'hasher_file_size_limit',
            'kind': Kind.INT,
            'required': False,
            'description': """
                Define the maximum file size in bytes that hashers should process. Any larger file will be skipped.
                A size of 0 represents no limit
            """,
        },
        {
            'name': 'hashers',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define a list of hashers to use by the tool. This is a comma separated list where each entry is the name
                of a hasher, such as "md5,sha256". "all" indicates that all hashers should be enabled. "none" disables
                all hashers.
            """,
        },
        {
            'name': 'parsers',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define which presets, parsers and/or plugins to use, or show possible values. The expression is a comma
                separated string where each element is a preset, parser or plugin name. Each element can be prepended
                with an exclamation mark to exclude the item. Matching is case insensitive. Examples: "linux,!bash_history"
                enables the linux preset, without the bash_history parser. "sqlite,!sqlite/chrome_history" enables all
                sqlite plugins except for chrome_history". "win7,syslog" enables the win7 preset, as well as the syslog
                parser.
            """,
        },
        {
            'name': 'partitions',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define partitions to be processed. A range of partitions can be defined as: "3..5". Multiple partitions
                can be defined as: "1,3,5" (a list of comma separated values). Ranges and lists can also be combined
                as: "1,3..5". The first partition is 1.
                All partitions can be specified with: "all"
            """,
        },
        {
            'name': 'volumes',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define volumes to be processed. A range of volumes can be defined as: "3..5". Multiple volumes can be
                defined as: "1,3,5" (a list of comma separated values). Ranges and lists can also be combined as:
                "1,3..5". The first volume is 1.
                All volumes can be specified with: "all"
            """,
        },
        {
            'name': 'no_vss',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': """
                Do not scan for Volume Shadow Snapshots (VSS). This means that Volume Shadow Snapshots (VSS) are not
                processed.
            """,
        },
        {
            'name': 'vss_only',
            'kind': Kind.BOOL,
            'value': 'false',
            'required': False,
            'description': """
                Do not process the current volume if Volume Shadow Snapshots (VSS) have been selected.
            """,
        },
        {
            'name': 'vss_stores',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define Volume Shadow Snapshots (VSS) (or stores that need to be processed. A range of stores can be
                defined as: "3..5". Multiple stores can be defined as: "1,3,5" (a list of comma separated values).
                Ranges and lists can also be combined as: "1,3..5". The first store is 1.
                All stores can be defined as: "all".
            """,
        },
        {
            'name': 'credential',
            'kind': Kind.STR,
            'required': False,
            'description': """
                Define a credentials that can be used to unlock encrypted volumes e.g. BitLocker. The credential is
                defined as type:data e.g. "password:BDE-test". Supported credential types are: key_data, password,
                recovery_password, startup_key. Binary key data is expected to be passed in BASE-16 encoding (hexadecimal).
                WARNING credentials passed via command line arguments can end up in logs, so use this option with care.
            """,
        },
        {
            'name': 'storage_file',
            'kind': Kind.PATH,
            'required': True,
            'description': "Path to a storage file",
        },
        {
            'name': 'source',
            'kind': Kind.PATH,
            'required': True,
            'description': """
                Path to a source device, file or directory. If the source is a supported
                storage media device or image file, archive file or a directory, the
                files within are processed recursively
            """,
        },
    ]
    DESCRIPTION = """
    Run log2timeline with given arguments
    """

    async def _run(self, arguments: Dict[str, ProcessorArgument]):
        """Process a file using log2timeline.py"""
        # invoke subprocess
        timestamp = now('%Y%m%dT%H%M%S')
        logpath = prepend_workdir(
            self.config, f'logs/log2timeline-{timestamp}.log.gz'
        )
        ensure_parent_dir(logpath)
        proc = await self._start_subprocess(
            'datashark.processors.log2timeline.bin',
            ['-q', '-u', '--log-file', str(logpath)],
            [
                # optional
                ('artifact_definitions', '--artifact-definitions'),
                ('artifact_filters_file', '--artifact-filters_file'),
                ('filter_file', '--filter-file'),
                ('hasher_file_size_limit', '--hasher-file-size-limit'),
                ('hashers', '--hashers'),
                ('parsers', '--parsers'),
                ('partitions', '--partitions'),
                ('volumes', '--volumes'),
                ('no_vss', '--no-vss'),
                ('vss_only', '--vss-only'),
                ('vss_stores', '--vss-stores'),
                ('credential', '--credential'),
                # positional
                ('storage_file', None),
                ('source', None),
            ],
            arguments,
            stdout=DEVNULL,
            stderr=PIPE,
        )
        await self._handle_communicating_process(proc)
