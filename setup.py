#!/usr/bin/env python
from setuptools import setup, find_packages
 
setup(
         name = "Procinfo",
         version = "0.1",
         description="Provides information for /proc or sysctl tunables",
         long_description="""\
         Provides easy access to documentation for /proc or sysctl tunables. That
         is, the data from the "Documentation" tree in the linux kernel sources.
         """,
         author="Raghu Udiyar",
         author_email="", # Removed to limit spam harvesting.
         url="https://github.com/raags/procinfo",
         include_package_data = True,
         package_data = {
             'procinfo': ['data/*']
            },
         packages = find_packages(exclude=["writer.py", "tests"]),
      
         entry_points = {
            'console_scripts': [
                'procinfo = procinfo.procinfo:main'
            ]},
         download_url = "https://github.com/raags/procinfo"
 )
