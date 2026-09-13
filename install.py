import launch
from importlib import metadata
from pathlib import Path
from packaging.requirements import Requirement


repo_root = Path(__file__).parent
main_req_file = repo_root / "requirements.txt"


def get_installed_version(package: str) -> str | None:
    try:
        return metadata.version(package)
    except Exception:
        return None


def install_requirements(req_file):
    with open(req_file, encoding="utf-8") as file:
        for requirement_line in file:
            package = requirement_line.strip()
            if not package or package.startswith("#"):
                continue

            try:
                requirement = Requirement(package)
                if requirement.marker and not requirement.marker.evaluate():
                    continue

                installed_version = get_installed_version(requirement.name)
                if installed_version is not None and requirement.specifier.contains(
                    installed_version
                ):
                    continue

                launch.run_pip(
                    f'install -U "{package}"',
                    f"sd-webui-birefnet requirement: changing {requirement.name} "
                    f"version from {installed_version} to {requirement.specifier or 'latest'}",
                )
            except Exception as e:
                print(e)
                print(
                    f"Warning: Failed to install {package}, some preprocessors may not work."
                )


install_requirements(main_req_file)
