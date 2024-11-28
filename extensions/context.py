import typing
from functools import lru_cache

import requests
from copier_templates_extensions import ContextHook


@lru_cache
def _get_version_for_python_dependency(dependency: str) -> str:
    response = requests.get(f"https://pypi.org/pypi/{dependency}/json")
    return response.json()["info"]["version"]


def _get_versions_for_python_dependencies(
    dependencies: typing.List[str], *, set_version_operator: str
) -> list[str]:
    deps_with_versions = {}
    for dependency in dependencies:
        version = _get_version_for_python_dependency(dependency)
        if version:
            deps_with_versions[dependency] = f"{set_version_operator}{version}"
        else:
            deps_with_versions[dependency] = ""
    return [
        f"{dependency}{version}" for dependency, version in deps_with_versions.items()
    ]


class Dependency(typing.TypedDict):
    name: str
    version: str


class DependenciesUpdater(ContextHook):
    def hook(self, context):
        should_get_newest_version_of_libraries_from_web = context[
            "get_newest_version_of_libraries_from_web"
        ]
        if not should_get_newest_version_of_libraries_from_web:
            return context

        should_freeze_dependencies = context["should_freeze_dependencies"]
        set_version_operator = "==" if should_freeze_dependencies else ">="

        app_dependencies = context["app_dependencies"]

        app_dependencies_with_versions = _get_versions_for_python_dependencies(
            app_dependencies, set_version_operator=set_version_operator
        )
        context["app_dependencies"] = app_dependencies_with_versions

        dev_dependencies = context["dev_dependencies"]
        dev_dependencies_with_versions = _get_versions_for_python_dependencies(
            dev_dependencies, set_version_operator=set_version_operator
        )
        context["dev_dependencies"] = dev_dependencies_with_versions

        return context
