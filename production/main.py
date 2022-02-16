import os



print(f"Hi {os.getlogin()}. Welcome to DDM-util!")
print("This is a utility to analyze images obtained by DDM.")
print("""Use Ctrl+C (in Windows/Linux) or Cmd+C (in Mac) to terminate this script anytime, 
while text cursor is in the terminal""")

print("The scripts run in the following order:")
print("\t DDM3.py \n \t graphing.py \n \t curvefit.py \n \t selectpoints.py")

yes = ["y", "Y", "yes", "Yes", "YES"]
no = ["n", "N", "no", "No", "NO"]

print("Do you want to analyze images using DDM3.py?")
while True:
	answer = input("Enter y for yes or n for no: ")
	print(answer)
	if answer in yes:
		print("You have chosen to run DDM3.py")
		print("""Make sure to set up all required variables in DDM3.py itself.
Mainly, you have to set up NFRAMES, total_time_in_sec, stack, outpath.
Make sure to save it too. DO NOT forget to save DDM3.py.
			""")
		x = input("Once you have saved DDM3.py, Press any key to continue:")
		print("Running DDM3.py. Please be patient as it may take several minutes to obtain output.")
		print("You will have to close the graph obtained to continue.")
		print("Code is running...")
		exec(open('DDM3.py').read())
		break

	elif answer in no:
		print("You have chosen to not run DDM3.py")
		break

	else:
		print("You have not entered a valid key.")



print("Do you want to plot initial output using graphing.py?")
while True:
	answer = input("Enter y for yes or n for no: ")
	if answer in yes:
		print("You have chosen to run graphing.py")
		print("""Make sure to set up all required variables in inputdata.py.
Mainly you have to set up "filename" of .dat file obtained after DDM.
Make sure to save it too. DO NOT forget to save inputdata.py.
			""")
		x = input("Once you have saved inputdata.py, Press any key to continue:")
		print("Please set initial parameters in inputdata.py while graph is visible.")
		print("You will have to close the window of the graph to proceed.")
		print("Code is running...")
		exec(open('graphing.py').read())

		break

	elif answer in no:
		print("You have chosen to not run graphing.py")
		break

	else:
		print("You have not entered a valid key.")



print("Do you want to curvefit obtained graphs using curvefit.py?")
while True:
	answer = input("Enter y for yes or n for no: ")
	if answer in yes:
		print("You have chosen to run curvefit.py")
		print("""Make sure to set up all required variables in inputdata.py.
Mainly you have to set up initial parameters, and checkout all other variables too.
Make sure to save it too. DO NOT forget to save inputdata.py.
			""")
		x = input("Once you have set up inputdata.py, Press any key to continue:")
		print("You will have to close the window of the graph to proceed.")
		print("Code is running...")
		exec(open('curvefit.py').read())

		break

	elif answer in no:
		print("You have chosen to not run curvefit.py")
		break

	else:
		print("You have not entered a valid key.")



print("Do you want to find the slope by selecting a region of points using selectpoints.py?")
while True:
	answer = input("Enter y for yes or n for no: ")
	if answer in yes:
		print("You have chosen to run selectpoints.py")
		x = input("Press any key to continue:")
		print("You will have to close the window of the graph to exit this utility.")
		print("Code is running...")
		exec(open('selectpoints.py').read())

		break

	elif answer in no:
		print("You have chosen to not run selectpoints.py")
		break

	else:
		print("You have not entered a valid key.")


print("Thanks for using this utility!")
x = input("Press any key to exit this script:")

