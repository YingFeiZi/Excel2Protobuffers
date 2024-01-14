import os
import re
from shutil import copyfile
import sys
import config
import generator_proto as genProto
import generator_bytes as genBytes

names =['Item']

if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) >0:
		names = [re.split(r"\.|-", name)[0] for name in args]
		print(names)
	#从本地配置文件复制配置到工具目录
	# config.Init(names)
	genProto.run()		# 必须先生成代码
	genBytes.run()	# 然后将excel数据打包成 flatbuffers 的二进制

	# for name in names:
	# 	bytesext =config.scriptExtDict['bytes']
	# 	bytes_file_path = config.GetFullPathExtension(config.GEN_DIR_DICT['bytes'],name, bytesext) 
	# 	copBytes_path = config.GetFullPathExtension(config.outputBytesDir, name, bytesext)
	# 	csext = config.scriptExtDict['csharp']
	# 	cs_file_path = config.GetFullPathExtension(config.GEN_DIR_DICT['csharp'],name, csext)
	# 	copCs_path = config.GetFullPathExtension(config.outputCSDir, name, csext)
	# 	if  os.path.exists(bytes_file_path)  and  os.path.exists(cs_file_path):
	# 		try:
	# 			copyfile(bytes_file_path, copBytes_path)
	# 			copyfile(cs_file_path, copCs_path)
	# 		except IOError as e:
	# 			print(f"An error occurred while copying {name}.bytes or {name}.cs: {e}")

	print("Done")