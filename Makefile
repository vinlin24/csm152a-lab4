.PHONY: all
all:
	@echo >&2 "Specify a make target." && exit 1

# For example, if you have a video named foo.mp4, run `make foo.rgb`.
%.rgb: %.mp4
	ffmpeg -i $< -vf scale=160:120 -r 16 -pix_fmt rgb24 $@

# For example, if you have a video named foo.mp4, run `make foo.bin`.
%.bin: %.mp4
	python converter/serialize.py $< $@

# For example, if you have a video named foo.mp4, run `make foo.tgz`.
%.tgz: %.mp4
	python converter/serialize.py $< $(basename $<).bin \
		--txt $(basename $<)
	cd $(basename $<) && tar -czf ../$@ .

.PHONY: clean
clean:
	-find . -type f -name "*.bin" -delete
	-find . -type f -name "*.rgb" -delete
	-find . -type f -name "frame_*.txt" -delete
	-find . -type d -empty -delete
