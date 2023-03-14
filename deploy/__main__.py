from github import (
    Github
)
from os import environ
from faker import Faker
from pathlib import Path


dist_root = Path(__file__).parent / "dist"
github_token = environ.get("GITHUB_TOKEN")
assert github_token
github_repo = environ.get("GITHUB_REPO")
assert github_repo
package_name = environ.get("PACKAGE_NAME")
assert package_name
dmg_path = dist_root / f"{package_name}-arm64.dmg"
assert dmg_path.exists()
src_root = Path(__file__).parent / package_name
version_path = src_root / "version.py"
assert version_path.exists()
version = version_path.read_text().split("=")[-1].strip().strip('"')
fake = Faker()
release_description = fake.paragraph()
print(release_description)

repo = Github(github_token).get_repo(github_repo)

release_version = f"v{version}"

commit = repo.get_branch("master").commit

release = repo.create_git_tag_and_release(
    release_version,
    release_description,
    release_version,
    release_description,
    commit.sha, ''
)

release.upload_asset(dmg_path.as_posix())
