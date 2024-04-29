from pathlib import Path
import re
from shutil import copyfile
import sys
import config
import generator_proto as genProto
import generator_bytes as genBytes
import generator_csv as genCSV


def CopyToFolder(name, outDir,language_sign):
	fext =config.scriptExtDict[language_sign]
	From_path = config.getRootPathFileExtension(config.GEN_DIR_DICT[language_sign],name, fext)
	To_path = config.getRootPathFileExtension(outDir, name, fext)
	if  From_path.exists() :
			try:
				copyfile(From_path, To_path)
			except IOError as e:
				print(f"--->ERROR: An error occurred while copying {name}.bytes or {name}.cs: {e}")

names =['cfg_equip_jinjie']
# names =[]

def DoAllOpreater():
	excels = config.GetFilesByExtension(config.GEN_DIR_DICT['xlsx'],config.scriptExtDict['xlsx'])
	if len(excels) < 1:
		return
	excelnames = [f.stem for f in excels]
	

	genProto.run()		# 必须先生成代码
	genBytes.run()	# 然后将excel数据打包成 flatbuffers 的二进制
		
	for name in excelnames:
		CopyToFolder(name, config.getOutBytesDir(), 'bytes')
		CopyToFolder(name, config.getOutputCSDir(), 'csharp')
		# CopyToFolder(f"{name}Config", config.getOutputConfigCSDir(), 'configcs')
	gcs = genCSV.excel2csv()
	gcs.run()
	print("Done")



if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) >0:
		# names = [re.split(r"\.|-", name)[0] for name in args]
		names = [Path(name).stem for name in args]
		# print(names)
	#从本地配置文件复制配置到工具目录
	config.Init(names)
	DoAllOpreater()

	input("\nDone, input anykey to exit")
	# print('')
	config.Quit()