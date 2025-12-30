#!/usr/bin/env python
"""Django CLI utility - entry point cho các lệnh manage.py"""
import os
import sys


def main():
    """Chạy Django management commands"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Không import được Django. Kiểm tra:\n"
            "- Django đã cài chưa?\n"
            "- Virtual environment đã activate chưa?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()