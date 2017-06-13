import os
import exifread
import mimetypes
import json
import datetime

def RepresentsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def get_extensions_for_type(general_type):
	mimetypes.init()
	for ext in mimetypes.types_map:
		if mimetypes.types_map[ext].split('/')[0] == general_type:
			yield ext

def extractEXIF(f,path_name):
	ret = {}
	ret['path']=path_name
	# Return Exif tags
	tags = exifread.process_file(f)
	for tag in tags.keys():
		if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote'):
			value = str(tags[tag])
			if(RepresentsInt(value)):
				ret[tag] = int(value)
			else:
				ret[tag] = value
			#	print "Key: %s, value %s" % (tag, tags[tag])
	return ret


if __name__ == '__main__':
	pictures = []
	directory = 'pictures/'
	exts = tuple(get_extensions_for_type('image'))
	files = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(directory)] for val in sublist]
	for path_name in files:
		#check extension
		ext = '.'+path_name.split(".")[-1].strip().lower()
		if(ext in exts):
			# Open image file for reading (binary mode)
			f = open(path_name, 'rb')
			try:
				#pictures.append(extractEXIF(f,path_name))
				pictures.append(extractEXIF(f,path_name))
			finally:
				f.close()
	result = {}
	result['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	result['pictures'] = pictures
	result['total pictures'] = len(pictures)
	with open('json/pictures.json', 'w') as outfile:
		json.dump(result, outfile)


