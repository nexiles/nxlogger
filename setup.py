from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='nexiles.logger',
      version=version,
      description="RabbitMQ Logging Facility",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ramon Bartl',
      author_email='ramon.bartl@nexiles.de',
      url='https://github.com/nexiles/nxlogger',
      license='CC',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nexiles'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pika>=0.9.5',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
