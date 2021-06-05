import click

from neuraltextserver import *

class RichGroup(click.Group):
	def format_help(self, ctx, formatter):
		print(f"""
    ███████    ██████████   █████ ██████   █████
  ███░░░░░███ ░░███░░░░███ ░░███ ░░██████ ░░███
 ███     ░░███ ░███   ░░███ ░███  ░███░███ ░███
░███      ░███ ░███    ░███ ░███  ░███░░███░███
░███      ░███ ░███    ░███ ░███  ░███ ░░██████
░░███     ███  ░███    ███  ░███  ░███  ░░█████
 ░░░███████░   ██████████   █████ █████  ░░█████
   ░░░░░░░    ░░░░░░░░░░   ░░░░░ ░░░░░    ░░░░░

 A centralized API for my various GPT-2 neural networks.
 The REST API is provided at odin.deadtired.me/api/docs
		""")

		print()

		self.format_usage(ctx, formatter)
		self.format_options(ctx, formatter)
		self.format_epilog(ctx, formatter)

@click.group(cls=RichGroup)
@click.version_option("1.0")
@click.pass_context
def main(ctx):
	pass

@main.command()
@click.argument("model")
def generate():
	print("Generate called")


if __name__ == "__main__":
	main()
