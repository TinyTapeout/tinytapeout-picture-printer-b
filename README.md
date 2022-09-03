![](../../workflows/wokwi/badge.svg)

Prints this the [Edinburgh Hacklab](https://edinburghhacklab.com/) logo pixel by pixel, line by line, left to right, top to bottom. 1 pixel per clock cycle.
Image is 41 by 41 pixels. 1 = black pixel, 0 = white pixel.

![alt text](https://github.com/ElectricPotato/tinytapeout-picture-printer-b/blob/main/images/img1_ehlab.png?raw=true)


## Pin list
| Pin  | Function |
|------|------|
| in0  | CLK  |
| in1  | Synchronous reset  |
| out0 | Pixel output |


## Run Length Encoding

The image is compressed with [run length encoding (RLE)](https://en.wikipedia.org/wiki/Run-length_encoding), I am unsure if this made the silicon are smaller or not.
The conversion script is in the images/ directory.

Example:
  start with a black pixel and the list [41, 136, 3, 9, 3, ...], decodes to 41 black pixels, 136 white pixels, 3 black pixels, 9 white pixels, etc

The design previously had horizontal and veritical sync signals, but I removed them in an attempt to get the design to fit.

(This repo is using the Tiny Tapeout [verilog template](https://github.com/H-S-S-11/tinytapeout-verilog-test))