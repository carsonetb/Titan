import importlib
import importlib.util
import os
import traceback
import sys
import raylib

class TestFramework:
	def __init__(self):
		self.test_success_num = 0
		self.test_failed_num = 0
		self.check_success_num = 0
		self.check_failed_num = 0
		self.checks_failed_this_test = False

	def run_tests(self):# Initialise raylib.
		raylib.SetConfigFlags(raylib.FLAG_WINDOW_RESIZABLE)
		raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
		raylib.SetTraceLogLevel(raylib.LOG_NONE)
		raylib.InitWindow(1170, 950, ("TESTS RENDER WINDOW").encode("ascii"))
		raylib.SetExitKey(0)
		raylib.SetTargetFPS(60)

		test_filepaths = os.listdir("editor/tests")

		for test_filepath in test_filepaths:
			if not test_filepath.endswith("test_framework.py") and test_filepath.endswith(".py"):
				self.checks_failed_this_test = False

				script_exception = False

				try:
					spec = importlib.util.spec_from_file_location("test_script", "editor/tests/" + test_filepath)
					script = importlib.util.module_from_spec(spec)
					sys.modules["test_script"] = script
					spec.loader.exec_module(script)
					script.run_tests(self)

				except Exception as e:
					script_exception = True
					self.check_failed_num += 1
					print(f"ERROR: SCRIPT ERRORED OUT: {test_filepath}, {e}")
				
				if self.checks_failed_this_test:
					self.check_failed_num += 1
					print(f"ERROR: TEST FAILED: {test_filepath}")
				
				if not script_exception and not self.checks_failed_this_test:
					self.test_success_num += 1

		print("INFO: Tests finished! Let's see the results ...")
		if self.test_failed_num > 0:
			print("INFO: Some tests failed.")
			print(f"INFO: {self.test_success_num} tests succeeded, but {self.test_failed_num} failed.")
			print(f"INFO: {self.check_success_num} checks succeeded, but {self.check_failed_num} failed.")
		else:
			print("INFO: All tests succeeded!")
	
	def check_eq(self, left, right):
		if left == right:
			self.check_success_num += 1
			return
		
		self.fail_check(left, right, "equal to")
	
	def check_greater(self, left, right):
		if left > right:
			self.check_success_num += 1
			return
		
		self.fail_check(left, right, "greater than")
	
	def check_less(self, left, right):
		if left < right:
			self.check_success_num += 1
			return
		
		self.fail_check(left, right, "less than")
	
	def check(self, to):
		if to:
			self.check_success_num += 1
			return
		
		self.checks_failed_this_test = True
		print(f"ERROR: CHECK FAILED: But I don't know what it was. Printing out the stack so you can figure it out for yourself.")
		traceback.format_exc()
	
	def fail_check(self, left, right, operator):
		self.checks_failed_this_test = True
		print(f"ERROR: CHECK FAILED: Is {left} {operator} {right}")