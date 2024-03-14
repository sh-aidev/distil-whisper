from dotenv import load_dotenv
load_dotenv()

import sys
import warnings
warnings.filterwarnings("ignore")

ANSI_RESET="\033[0m"        # Reset all formatting
ANSI_BOLD="\033[1m"         # Bold text
ANSI_YELLOW="\033[33m"      # Yellow text

sys.stdout.write(ANSI_BOLD + ANSI_YELLOW)
print("Inferencing with HuggingFace's Distil-Whisper Model:")
import pyfiglet
distil_whisper_art = pyfiglet.figlet_format("distil-whisper")
print(distil_whisper_art)

sys.stdout.write(ANSI_RESET)

from internal import App

from internal.utils.logger import logger

def main():
    app = App()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        logger.error("Keyboard Interrupted...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Exited due to {e}")
        sys.exit(0)