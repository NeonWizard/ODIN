from neuraltextserver import *

def main():
	print(f"""
    ███████    ██████████   █████ ██████   █████
  ███░░░░░███ ░░███░░░░███ ░░███ ░░██████ ░░███
 ███     ░░███ ░███   ░░███ ░███  ░███░███ ░███
░███      ░███ ░███    ░███ ░███  ░███░░███░███
░███      ░███ ░███    ░███ ░███  ░███ ░░██████
░░███     ███  ░███    ███  ░███  ░███  ░░█████
 ░░░███████░   ██████████   █████ █████  ░░█████
   ░░░░░░░    ░░░░░░░░░░   ░░░░░ ░░░░░    ░░░░░

  A centralized API for all of my GPT-2 neural networks.
  The REST API is provided at neuraltext.deadtired.me/api/docs

  Usage: odin <command> [options]

  Options:
	-v, --version		output the version number
	-h, --help			output the usage information
	""")

if __name__ == "__main__":
	main()
