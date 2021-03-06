import click

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
 The web API is provided at odin.deadtired.me/api/docs
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
def list():
	"""
	Print all of the available GPT-2 models by name.
	"""

	import odin
	print("\n".join(odin.models()))

@main.command()
@click.argument("model")
def generate(model):
	"""
	Generate text via the specified model name.
	"""

	import odin
	print("\n".join(odin.generate(model)["data"]))


if __name__ == "__main__":
	main()
