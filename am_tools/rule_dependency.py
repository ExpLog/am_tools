from typing import Set, Dict, List

import networkx as nx
import os
import re

name_re = re.compile("ALMGR[A-Z]+-(\\d+)\\.drl")
rule_id_re = re.compile("ruleID.*?(\\d+)")


def rule_dependencies_components(path: str, filter_no_dep: bool) -> List[Set[str]]:
    """
    Calculates the dependency groups of a set of drools rule files for Alarm Manager.
    """
    dependency = find_dependencies(path)
    graph = dependency_graph(dependency)

    return [component for component in nx.connected_components(graph) if filter_no_dep or len(component) > 1]


def dependency_graph(dependencies: Dict[str, Set[str]]) -> nx.Graph:
    graph = nx.Graph()
    for rule, dep_set in dependencies.items():
        for node in dep_set:
            graph.add_edge(rule, node)

    return graph


def find_dependencies(path: str) -> Dict[str, Set[str]]:
    if not os.path.isdir(path):
        raise Exception(f"The given path {path} is not a directory.")

    count = 0
    dependency = {}
    for file_name in os.listdir(path):
        match = name_re.match(file_name)
        if match:
            rule = match.group(1)
            dependency[rule] = find_rule_ids(os.path.join(path, file_name))
            count += 1

    if count == 0:
        raise Exception(f"Could not find any Alarm Manager .drl files at {path}.")

    return dependency


def find_rule_ids(file_name: str) -> Set[str]:
    id_set = set()
    with open(file_name) as file_:
        for line in file_:
            for match_ in rule_id_re.finditer(line):
                id_set.add(match_.group(1))
    return id_set
