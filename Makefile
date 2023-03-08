.PHONY: all
all:
	@echo >&2 "Specify a make target." && exit 1

# For example, if you have a video named foo.mp4, run `make foo.rgb`.
%.rgb: %.mp4
	ffmpeg -i $< -vf scale=160:120 -r 16 -pix_fmt rgb24 $@

.PHONY: clean
clean:
	-find . -type f -name "*.bin" -delete
	-find . -type f -name "*.rgb" -delete
