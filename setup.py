from setuptools import setup

setup(
    name="am_tools",
    version="1.0.0",
    packages=["am_tools"],
    url="",
    license="BSD-2-Clause",
    author="ExpLog",
    author_email="lobo.fontoura@gmail.com",
    description="A set of tools for those working in AM.",
    install_requires=["click", "networkx", "mechanicalsoup"],
    entry_points={
        "console_scripts": [
            "leave=am_tools.cli:time_to_leave",
            "rule-dep=am_tools.cli:rule_dependencies"
        ]
    }
)
