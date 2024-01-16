import os
import re
from shutil import copyfile
import sys
import config
import generator_proto as genProto
import generator_bytes as genBytes


def CopyToFolder(name, outDir,language_sign):
	fext =config.scriptExtDict[language_sign]
	From_path = config.getRootPathFileExtension(config.GEN_DIR_DICT[language_sign],name, fext)
	To_path = config.getRootPathFileExtension(outDir, name, fext)
	if  os.path.exists(From_path) :
			try:
				copyfile(From_path, To_path)
			except IOError as e:
				print(f"--->ERROR: An error occurred while copying {name}.bytes or {name}.cs: {e}")

# names =['Item']
names =[]

if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) >0:
		names = [re.split(r"\.|-", name)[0] for name in args]
		# print(names)
	#从本地配置文件复制配置到工具目录
	config.Init(names)
	genProto.run()		# 必须先生成代码
	genBytes.run()	# 然后将excel数据打包成 flatbuffers 的二进制
	if len(names) < 1:
		excels = config.GetFilesByExtension(config.inputDir,config.scriptExtDict['xlsx'])
		names = [f.split('.')[0] for f in excels]
	for name in names:
		CopyToFolder(name, config.getOutBytesDir(), 'bytes')
		CopyToFolder(name, config.getOutputCSDir(), 'csharp')
		CopyToFolder(f"{name}Config", config.getOutputConfigCSDir(), 'configcs')

	print('')
	input("Done, input anykey to exit")
	sys.exit(0)