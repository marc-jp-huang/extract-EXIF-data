import os
import exifread
import mimetypes

def get_extensions_for_type(general_type):
	mimetypes.init()
	for ext in mimetypes.types_map:
		if mimetypes.types_map[ext].split('/')[0] == general_type:
			yield ext

def extractEXIF(f):
	# Return Exif tags
	tags = exifread.process_file(f)
	for tag in tags.keys():
		if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote'):
			print "Key: %s, value %s" % (tag, tags[tag])

if __name__ == '__main__':
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
				extractEXIF(f)
			finally:
				f.close()


