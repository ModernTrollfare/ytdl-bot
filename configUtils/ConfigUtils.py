import os

import argparse

import pickle

defaultInstancePath = os.path.join(os.path.expanduser("~"), "telegram-sticker-manager-collections")
configName = ".Config.in"

# Helper functions
def argparseInit():
	"""Initialize the Argparse."""
	parser = argparse.ArgumentParser(description='Sticker manager bot for Telegram.', epilog='To setup your first instance, call ')
	confGroup = parser.add_mutually_exclusive_group(required=True)
	confGroup.add_argument("-s", "--setup",
		nargs='?',
		type=str,
		const=defaultInstancePath,
		help="""Setup bot instance at path specified.
		Target directory will be created(recursively) if it doesn't exist, and Configuration file will be created under the destination.
		Default path is '"""+defaultInstancePath+"'.",
		dest="setupPath",
		metavar="setup-path")
	confGroup.add_argument("-c", "--config-file",
		nargs=1,
		type=str,
		help="Specify Configuration file for bot instance.",
		dest="configFilePath",
		metavar="config-file-path")
	return (parser.prog, parser.parse_args())

def initConfig(prog, setupRootPath):
	"""Creates a fresh setup, then returns and prompt the user to start with -c."""
	#print(setupRootPath)
	if os.path.isdir(setupRootPath) == False:
		ans = input("The directory "+setupRootPath+" does not exist. Create it?(y/n):\t\t")
		if ans == 'y' or ans == 'Y':
			try:
				os.makedirs(setupRootPath)
			except OSError as e:
				raise OSError("Failed to create directory "+setupRootPath +" ! Aborting.")
		elif ans == 'N' or ans == 'n':
				print("Not creating directory "+setupRootPath +" ! Aborting.")
				print("Setup is not successful. Please run '"+prog+' -s '+setupRootPath+"' again.")
				exit()
		else:
			print("Invalid response. Please input y or n!")
			initConfig(prog,setupRootPath)
			return

	configPath = os.path.join(os.path.realpath(setupRootPath), configName)

	if os.path.isfile(configPath):
		while True:
			ans = input("Config file already found in the specified path. Overwrite it?(y/n):\t\t")
			if ans == 'y' or ans == 'Y':
				break
			elif ans == 'N' or ans == 'n':
					print("Not overwriting Config file in "+setupRootPath +" ! Aborting.")
					print("Setup is not successful. Please run '"+prog+' -s '+setupRootPath+"' again.")
					exit()
			else:
				print("Invalid response. Please input y or n!")

	token = ''
	while True:
		token = input("Please input your token:\n")
		confirm = input("Please reenter to confirm your token:\n")
		if token == confirm:
			break
		else:
			print("Inputs does not match!")

	persist = {"token": token}

	try:
		with open(configPath, 'wb') as f:
			pickle.dump(persist, f)
	except OSError as e:
		raise OSError("Error occurred when creating Config file under "+setupRootPath +" ! Aborting.")

def importConfig(configPath):
	"""Read config file and parse it."""
	# TODO: use a telegram.ext.DictPersistence
	try:
		with open(configPath, 'rb') as f:
			return pickle.load(f)
	except OSError as e:
		raise OSError("Error occurred when reading Config file "+configPath +" ! Aborting.")


def init():
	prog, argv = argparseInit()
	if argv.setupPath:
		initConfig(prog, argv.setupPath)
		print("Congratulations! The bot instance is ready to go! Simply run:\n'"
			+ prog
			+" -c "
			+ argv.setupPath
			+"/.Config.in'\nto start using the bot! *Beep-Bop* ")
		exit()
	elif argv.configFilePath:
		return importConfig(argv.configFilePath[0])
	raise OSError("Undefined state: either one of -s or -c should be set!")
	exit()