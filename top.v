`timescale 1 ns / 1 ns


module top(i_clk, rgb, vs, hs, rst, seg, an);
   input        i_clk;
   input        rst;
   output [7:0] rgb;
   output       vs;
   output       hs;
	output      seg;
	output[3:0]  an;
	//output		 Led6;
   assign seg = rst;
	assign an = tempAn;
   
   wire         clk25;
   wire         clk16;
   wire         frameClk;
   wire [9:0]   vcount;
   wire [9:0]   hcount;
   wire [3:0]   keynum;
	reg [3:0] 	tempAn = 4'b1111;
   
  
   clk_div u1(.clk_in(i_clk), .clk_25(clk25) .clk_16(clk_16));
   
   vga u2(.clk_25(clk25), .vs(vs), .hs(hs), .vpixel(vcount), .hpixel(hcount));
   
   controlLogic log(.sysClk(i_clk) .clk16(clk16) .frameClk(frameClk));

   frameGetter u3(.frameClk(frameClk) .clk_25(clk25), .v_count(vcount), .h_count(hcount), .rgb(rgb), .rst(rst), .jump(jump));
   
endmodule
