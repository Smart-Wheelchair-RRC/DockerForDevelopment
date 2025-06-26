import sys
import yaml
import argparse
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def setup_logging():
    """Sets up basic logging."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Builds a docker image based on combinations.yaml.")
    parser.add_argument("target_image_suffix", help="The suffix of the target image name (e.g., humble_gpu).")
    parser.add_argument("version_tag", help="The version tag for the docker image (e.g., v1.0).")
    return parser.parse_args()

def load_combinations(combinations_file: Path):
    """Loads and parses the combinations YAML file."""
    try:
        with open(combinations_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Combinations file not found: '{combinations_file}'")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{combinations_file}': {e}")
        return None

def find_target_combination(combinations, target_image_suffix):
    """Finds the target combination from the list of combinations by suffix."""
    for combo in combinations:
        if combo.get('target_image_name', '').endswith(f'/{target_image_suffix}'):
            return combo
    return None

def validate_version_tag(version_tag):
    """Validates the version tag."""
    if not (version_tag == "latest" or version_tag == "test" or version_tag.startswith("v") or version_tag.startswith("dev")):
        logger.error(f"Invalid version tag: '{version_tag}'. Must be 'latest', 'test', start with 'v', or start with 'dev'.")
        return False
    return True

def build_docker_image(target_combo, version_tag):
    """Constructs and prints the docker build command."""
    target_image_name = target_combo.get('target_image_name')
    base_image = target_combo.get('base_image')
    dockerfile = target_combo.get('dockerfile')
    build_context = target_combo.get('docker_build_context')
    full_target_image = f"{target_image_name}:{version_tag}"

    if not all([base_image, dockerfile, build_context]):
        logger.error(f"Incomplete configuration for '{target_image_name}' in combinations file.")
        return False

    command = [
        "docker", "build",
        "--build-arg", f"BASE_IMAGE={base_image}",
        "-t", full_target_image,
        "-f", dockerfile,
        build_context
    ]

    print(' '.join(command))
    return True

def main():
    """
    Builds a docker image based on combinations.yaml.
    """
    setup_logging()
    args = parse_arguments()

    if not validate_version_tag(args.version_tag):
        sys.exit(1)

    combinations_file = Path('combinations.yaml')
    combinations = load_combinations(combinations_file)
    if not combinations:
        sys.exit(1)

    target_combo = find_target_combination(combinations, args.target_image_suffix)

    if not target_combo:
        logger.error(f"Target image with suffix '{args.target_image_suffix}' not found in '{combinations_file}'.")
        sys.exit(1)

    if not build_docker_image(target_combo, args.version_tag):
        sys.exit(1)

if __name__ == "__main__":
    main()