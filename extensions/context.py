import json
import logging
import subprocess
import typing
from functools import lru_cache
from urllib.request import urlopen

from copier_templates_extensions import ContextHook
from jinja2 import Environment
from jinja2.ext import Extension

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # noqa: F821


@lru_cache
def _get_version_for_python_dependency(dependency: str) -> str:
    try:
        logger.debug(f"Getting version for '{dependency}'")
        # NOTE: Getting the whole json is the only way to get the version.
        #       For some of the packages it has a lot of information so it takes
        #       a while to get the response.
        with urlopen(
            f"https://pypi.org/pypi/{dependency}/json", timeout=10
        ) as response:
            data = json.loads(response.read())
            version = data["info"]["version"]
            logger.info(f"Got version for '{dependency}': {version}")
            return version
    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Error getting version for {dependency}: {e}")
        return ""


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
    def update_required_dependencies_version(self, context):
        required_dependencies_version = context["required_dependencies_version"]
        for dep_name, _ in required_dependencies_version.items():
            required_dependencies_version[dep_name] = (
                _get_version_for_python_dependency(dep_name)
            )

        context["required_dependencies_version"] = required_dependencies_version

    def update_dependencies_version(self, context):
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

    def hook(self, context):
        should_get_newest_version_of_libraries_from_web = context[
            "get_newest_version_of_libraries_from_web"
        ]
        if not should_get_newest_version_of_libraries_from_web:
            return context
        self.update_dependencies_version(context)
        self.update_required_dependencies_version(context)
        return context


def get_author_name_from_git() -> str:
    output = subprocess.check_output(["git", "config", "user.name"])
    return output.decode("utf-8").strip()


def get_author_email_from_git() -> str:
    output = subprocess.check_output(["git", "config", "user.email"])
    return output.decode("utf-8").strip()


class AuthorFromGit(Extension):
    def __init__(self, environment: Environment):
        environment.globals["get_author_name_from_git"] = get_author_name_from_git
        environment.globals["get_author_email_from_git"] = get_author_email_from_git
        super().__init__(environment)


class InitGitRepo(ContextHook):
    def hook(self, context):
        dst = context["_copier_conf"]["dst_path"]
        is_git_repo = subprocess.run(
            ["test", "-d", ".git"],
            capture_output=True,
            text=True,
            cwd=dst,
        )

        if is_git_repo.returncode != 0:
            logger.info("Initializing git repository")
            subprocess.run(["git", "init"], cwd=dst)
        return context
