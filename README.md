# Lab 4


Final project for **W23 COM SCI M152A**.


## [Converter](converter/)


### Setup


**Requirement:** Python 3.8+

After checking out to this branch, set up the necessary dependencies:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You will also need [FFmpeg](https://ffmpeg.org/download.html) installed.
You can probably obtain it using your local package manager. For Windows, you
can download a static build and place the `ffmpeg.exe` binary some place
on your `PATH`. I used the [Chocolatey](https://chocolatey.org/) package manager
for Windows instead:

```powershell
# In an elevated PowerShell session:
choco install ffmpeg
```


### Overview


The following graphic shows the different file formats into which an input MP4
file is transformed:

```mermaid
flowchart LR;
  mp4[foo.mp4\nOrdinary video file];
  rgb[foo.rgb\n160x120px RGB24 16fps];
  bin[foo.bin\n160x120px 8-bit VGA pixels 16fps];
  txt[foo/frame_xxxx.txt\n19.2K 8-bit VGA pixels];
  tgz[foo.tgz\nTransfer medium between ISE];
  mp4-.->rgb;
  rgb-.->bin;
  rgb-.->txt;
  txt-.->tgz;
  tgz-.->txt;
  txt--> |$readmemh| fpga("reg [7:0] frame[0:19200-1]");
```


### Serializing


I provided Makefile rules as front-ends for invoking my
[serialize.py](converter/serialize.py) script for building each format from the
original MP4 file. Suppose it is named `foo.mp4`.

* `make foo.rgb`: Convert to a 160x120px resolution, 16 frames-per-second, RGB24
  file.
* `make foo.bin`: Convert to a 160x120px resolution, 16 frames-per-second, 8-bit
  VGA color-encoded (`rrrgggbb` per pixel) file.
* `make foo.tgz`: The same video properties as the `.bin` format but saved as
  separate text files for each frame instead, with each text file containing a
  newline-separated list of hexadecimal digit pairs representing the 8-bit color
  for that pixel.

`foo.tgz` is the final product we want at this step, and it's the file we can
transfer onto a flash drive and then onto the host machine of the Xilinx ISE
where we can then un`tar` the `.txt` frame files back out.

> At the time of writing this, I am still uncertain about how to transfer
arbitrary data files onto the FPGA, so the process outlined above may be subject
to change.


### Visualizing


For debugging, you can use the [show.sh](show.sh) script as a shortcut for
invoking my [visualize.py](converter/visualize.py) script, which takes any of
the binary formats above and displays in a GUI the specified frame. Both frame
numbers are seconds into the video are supported. For example:

```sh
# Show the frame 8 seconds into foo.mp4:
./show.sh foo.mp4 -s 8
# Compare the coloring of the 200th frame (assuming 16fps):
./show.sh foo.bin -f 200 & ./show.sh foo.rgb -f 200 &
# Confirm that a frame txt file has the right bytes:
./show.sh foo -f 0x30 & ./how.sh foo.bin -f 0x30 &
```


### Cleanup


To clean the directory of binary and `.txt` intermediates, simply run:

```sh
make clean
```

Original MP4 video files as well as the TGZ distributables are preserved.
