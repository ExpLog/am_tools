import json

import click
import os

import am_tools.rule_dependency as dep
import am_tools.time_to_leave as ttl


@click.command()
@click.argument("credentials_path", type=click.STRING)
def time_to_leave(credentials_json):
    """
    Logins to asmill01/millenium and calculates at what time you should leave considering a 8 hour work day.

    The credentials_path should be the path to a json object file containing user and password fields. Note that the
    file should contain only one json object.
    """
    with open(credentials_json) as file:
        credentials = json.loads(file.read())
        click.echo(ttl.build_time_to_leave_message(credentials))


@click.command()
@click.option("--dir", default=os.getcwd(), help="Directory containing .drl files.")
@click.option("--filter", is_flag=True, help="Filters dependency components that only have a single rule id.")
def rule_dependencies(path: str, filter_no_dep: bool):
    components = dep.rule_dependencies_components(path, filter_no_dep)
    for comp in components:
        click.echo(comp)
