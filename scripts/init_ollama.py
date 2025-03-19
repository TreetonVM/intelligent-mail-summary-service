import os
import subprocess
import sys

# Add the parent directory to the Python path
# This allows importing modules from the parent directory (project root)
# which is necessary to import modules when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logger.logger import configure_root_logger, get_logger

configure_root_logger()
logger = get_logger("init_ollama")


def check_ollama_installed() -> bool:
    try:
        subprocess.run(
            ["ollama", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Ollama not found. Install from https://ollama.ai/")
        return False


def ensure_model_available(model_name: str = "mistral") -> bool:
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        return model_name in result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Model check failed: {e.stderr}")
        return False


def pull_model(model_name: str) -> None:
    try:
        logger.info(f"Downloading {model_name} model...")
        subprocess.run(["ollama", "pull", model_name], check=True)
        logger.info("Model download successful")
    except subprocess.CalledProcessError as e:
        logger.error(f"Model download failed: {e.stderr}")
        sys.exit(1)


def main():
    if not check_ollama_installed():
        sys.exit(1)

    if not ensure_model_available():
        pull_model("mistral")

    logger.info("Ollama setup validation complete")


if __name__ == "__main__":
    main()
