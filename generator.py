import os
import re
from shutil import copyfile
import sys
import generator_proto as genProto
import config

names =['Item']

if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) >0:
		names = [re.split(r"\.|-", name)[0] for name in args]
		print(names)

	config.Init(names)
	genProto.run()		# 必须先生成代码
	# genrbytes.run()	# 然后将excel数据打包成 flatbuffers 的二进制

	# config.mkdir(config.outputBytesDir)
	# config.mkdir(config.outputCSDir)
	# for name in names:
	# 	bytes_file_path = os.path.join(config.generatedBytesDir, f"{name}.bytes")
	# 	copBytes_path = os.path.join(config.outputBytesDir, f"{name}.bytes")
	# 	cs_file_path = os.path.join(config.generatedCSDir, f"{name}.cs")
	# 	copCs_path = os.path.join(config.outputCSDir, f"{name}.cs")
		
	# 	if  os.path.exists(bytes_file_path)  and  os.path.exists(cs_file_path):
	# 		try:
	# 			copyfile(bytes_file_path, copBytes_path)
	# 			copyfile(cs_file_path, copCs_path)
	# 		except IOError as e:
	# 			print(f"An error occurred while copying {name}.bytes or {name}.cs: {e}")

	print("Done")