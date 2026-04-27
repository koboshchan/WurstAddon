from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FABRIC_MOD_JSON = ROOT / "src/main/resources/fabric.mod.json"
SERVICE_FILE = (
	ROOT / "src/client/resources/META-INF/services/net.wurstclient.addon.Addon"
)
README = ROOT / "README.md"
GRADLE_PROPERTIES = ROOT / "gradle.properties"


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Rename the addon Java package and related metadata."
	)
	parser.add_argument(
		"package",
		nargs="?",
		help="New full Java package, for example com.example.torchaddon.",
	)
	parser.add_argument(
		"--addon-name",
		help="New display name for the addon. Defaults to the current name.",
	)
	parser.add_argument(
		"--description",
		help="Optional replacement description for fabric.mod.json.",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Print planned changes without modifying files.",
	)

	args = parser.parse_args()
	if not args.package:
		parser.error("the following arguments are required: package")

	validate_package(args.package)
	return args


def validate_package(package_name: str) -> None:
	parts = package_name.split(".")
	if not parts or any(not part or not part.replace("_", "a").isalnum() for part in parts):
		raise SystemExit(f"Invalid package name: {package_name}")
	if any(part[0].isdigit() for part in parts):
		raise SystemExit(f"Invalid package name: {package_name}")


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as handle:
		return json.load(handle)


def write_json(path: Path, data: dict, dry_run: bool) -> None:
	if dry_run:
		print(f"Would update {relative_path(path)}")
		return

	with path.open("w", encoding="utf-8") as handle:
		json.dump(data, handle, indent=2)
		handle.write("\n")


def relative_path(path: Path) -> Path:
	return path.relative_to(ROOT)


def read_text(path: Path) -> str:
	with path.open("r", encoding="utf-8") as handle:
		return handle.read()


def write_text(path: Path, content: str, dry_run: bool) -> None:
	if dry_run:
		print(f"Would update {relative_path(path)}")
		return

	with path.open("w", encoding="utf-8") as handle:
		handle.write(content)


def replace_in_file(path: Path, replacements: list[tuple[str, str]], dry_run: bool) -> None:
	if not path.exists():
		return

	original = read_text(path)
	updated = original
	for old, new in replacements:
		updated = updated.replace(old, new)

	if updated == original:
		return

	write_text(path, updated, dry_run)


def move_path(source: Path, target: Path, dry_run: bool) -> None:
	if not source.exists() or source == target:
		return
	if target.exists():
		raise SystemExit(
			f"Refusing to move {relative_path(source)} to existing path {relative_path(target)}"
		)

	if dry_run:
		print(f"Would move {relative_path(source)} -> {relative_path(target)}")
		return

	target.parent.mkdir(parents=True, exist_ok=True)
	shutil.move(str(source), str(target))
	cleanup_empty_parents(source.parent)


def cleanup_empty_parents(start: Path) -> None:
	current = start
	while current != ROOT and current.exists() and current.is_dir():
		try:
			current.rmdir()
		except OSError:
			break
		current = current.parent


def detect_current_package(mod_json: dict) -> str:
	main_entries = mod_json.get("entrypoints", {}).get("main", [])
	if not main_entries:
		raise SystemExit("Could not detect current package from fabric.mod.json entrypoints.main")

	entrypoint = main_entries[0]
	if "." not in entrypoint:
		raise SystemExit(f"Unexpected main entrypoint: {entrypoint}")

	return entrypoint.rsplit(".", 1)[0]


def update_fabric_mod(
	path: Path,
	old_package: str,
	new_package: str,
	old_mod_id: str,
	new_mod_id: str,
	old_addon_name: str,
	new_addon_name: str,
	new_description: str | None,
	dry_run: bool,
) -> None:
	data = load_json(path)
	data["id"] = new_mod_id
	data["name"] = new_addon_name
	data["icon"] = f"assets/{new_mod_id}/icon.png"

	description = data.get("description", "")
	if new_description is not None:
		data["description"] = new_description
	else:
		data["description"] = description.replace(old_addon_name, new_addon_name).replace(
			old_package, new_package
		)

	entrypoints = data.get("entrypoints", {})
	for key, values in entrypoints.items():
		entrypoints[key] = [value.replace(old_package, new_package) for value in values]

	updated_mixins = []
	for item in data.get("mixins", []):
		if isinstance(item, str):
			updated_mixins.append(item.replace(old_mod_id, new_mod_id))
		else:
			updated_item = dict(item)
			config = updated_item.get("config")
			if isinstance(config, str):
				updated_item["config"] = config.replace(old_mod_id, new_mod_id)
			updated_mixins.append(updated_item)
	data["mixins"] = updated_mixins

	write_json(path, data, dry_run)


def update_gradle_properties(
	path: Path,
	old_addon_name: str,
	new_addon_name: str,
	new_package: str,
	dry_run: bool,
) -> None:
	if not path.exists():
		return

	lines = read_text(path).splitlines()
	new_maven_group = new_package.rsplit(".", 1)[0] if "." in new_package else new_package
	updated_lines = []

	for line in lines:
		if line.startswith("archives_base_name="):
			updated_lines.append(f"archives_base_name={new_addon_name}")
		elif line.startswith("maven_group="):
			updated_lines.append(f"maven_group={new_maven_group}")
		else:
			updated_lines.append(line.replace(old_addon_name, new_addon_name))

	updated = "\n".join(updated_lines) + "\n"
	if updated != read_text(path):
		write_text(path, updated, dry_run)


def update_service_file(path: Path, new_package: str, dry_run: bool) -> None:
	content = f"{new_package}.client.WurstAddonHackAddon\n"
	write_text(path, content, dry_run)


def rename_package_directories(old_package: str, new_package: str, dry_run: bool) -> None:
	old_rel = Path(*old_package.split("."))
	new_rel = Path(*new_package.split("."))

	move_path(ROOT / "src/main/java" / old_rel, ROOT / "src/main/java" / new_rel, dry_run)
	move_path(ROOT / "src/client/java" / old_rel, ROOT / "src/client/java" / new_rel, dry_run)


def rename_mixin_files(old_mod_id: str, new_mod_id: str, dry_run: bool) -> None:
	move_path(
		ROOT / "src/client/resources" / f"{old_mod_id}.client.mixins.json",
		ROOT / "src/client/resources" / f"{new_mod_id}.client.mixins.json",
		dry_run,
	)
	move_path(
		ROOT / "src/main/resources" / f"{old_mod_id}.mixins.json",
		ROOT / "src/main/resources" / f"{new_mod_id}.mixins.json",
		dry_run,
	)


def rename_assets_directory(old_mod_id: str, new_mod_id: str, dry_run: bool) -> None:
	move_path(
		ROOT / "src/main/resources/assets" / old_mod_id,
		ROOT / "src/main/resources/assets" / new_mod_id,
		dry_run,
	)


def iter_java_files(package_name: str) -> list[Path]:
	package_rel = Path(*package_name.split("."))
	java_files: list[Path] = []

	for source_root in (ROOT / "src/main/java", ROOT / "src/client/java"):
		package_root = source_root / package_rel
		if package_root.exists():
			java_files.extend(sorted(package_root.rglob("*.java")))

	return java_files


def update_text_surfaces(
	old_package: str,
	new_package: str,
	old_mod_id: str,
	new_mod_id: str,
	old_addon_name: str,
	new_addon_name: str,
	dry_run: bool,
) -> None:
	replacements = [
		(old_package, new_package),
		(old_mod_id, new_mod_id),
		(old_addon_name, new_addon_name),
	]

	for java_file in iter_java_files(new_package):
		replace_in_file(java_file, replacements, dry_run)

	replace_in_file(
		ROOT / "src/client/resources" / f"{new_mod_id}.client.mixins.json",
		[(old_package, new_package)],
		dry_run,
	)
	replace_in_file(
		ROOT / "src/main/resources" / f"{new_mod_id}.mixins.json",
		[(old_package, new_package)],
		dry_run,
	)
	replace_in_file(README, replacements, dry_run)


def main() -> None:
	args = parse_args()

	mod_json = load_json(FABRIC_MOD_JSON)
	old_package = detect_current_package(mod_json)
	new_package = args.package
	old_mod_id = mod_json["id"]
	new_mod_id = new_package.rsplit(".", 1)[-1]
	old_addon_name = mod_json["name"]
	new_addon_name = args.addon_name or old_addon_name

	rename_package_directories(old_package, new_package, args.dry_run)
	rename_mixin_files(old_mod_id, new_mod_id, args.dry_run)
	rename_assets_directory(old_mod_id, new_mod_id, args.dry_run)

	update_fabric_mod(
		FABRIC_MOD_JSON,
		old_package,
		new_package,
		old_mod_id,
		new_mod_id,
		old_addon_name,
		new_addon_name,
		args.description,
		args.dry_run,
	)
	update_service_file(SERVICE_FILE, new_package, args.dry_run)
	update_gradle_properties(
		GRADLE_PROPERTIES,
		old_addon_name,
		new_addon_name,
		new_package,
		args.dry_run,
	)
	update_text_surfaces(
		old_package,
		new_package,
		old_mod_id,
		new_mod_id,
		old_addon_name,
		new_addon_name,
		args.dry_run,
	)

	print(
		"Updated package "
		f"{old_package} -> {new_package} "
		f"and addon name {old_addon_name} -> {new_addon_name}."
	)


if __name__ == "__main__":
	main()
