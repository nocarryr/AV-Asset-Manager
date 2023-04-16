#!/usr/bin/env python
import os
import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

HERE = Path(__file__).resolve().parent

def prep_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avam.avam.settings")

    if HERE == Path.cwd():
        if 'avam.avam' not in sys.modules:
            spec = spec_from_file_location('avam', str(HERE / '__init__.py'))
            module = module_from_spec(spec)
            sys.modules['avam'] = module

            spec = spec_from_file_location('avam.avam', str(HERE / 'avam' / '__init__.py'))
            module = module_from_spec(spec)
            sys.modules['avam.avam'] = module

    if str(HERE) not in sys.path:
        sys.path.append(str(HERE))

def main():
    prep_env()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
