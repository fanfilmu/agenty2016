all: image clean

image:
	ffmpeg -pattern_type glob -i '*.png' -c:v libx264 -crf 6 -preset medium -c:a libfdk_aac -vbr 4 -movflags +faststart -vf scale=1000:1000:flags=neighbor output.mp4

clean:
	rm sim*
	rm result.dat
