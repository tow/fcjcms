#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tobycms.settings")

    from django.core.management import execute_from_command_line

    import pdb;pdb.set_trace()
    execute_from_command_line(sys.argv)