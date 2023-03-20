`timescale 1 ns / 1 ns


module top(i_clk, pause,so,st, rgb, vs, hs, rst, seg, an);
   input        i_clk;
   input        rst,pause,so,st;
   output [7:0] rgb;
   output       vs;
   output       hs;
	output      seg;
	output[3:0]  an;
	//output		 Led6;
   assign seg = rst;
	assign an = tempAn;
   
   wire         clk25;//25MHz
   wire         clk16;//16Hz
   wire         clk32;//32Hz
   wire         clk8;//8Hz
   wire [9:0]   vcount;
   wire [9:0]   hcount;
   wire [3:0]   keynum;
	reg [3:0] 	tempAn = 4'b1111;
   
  
   clk_div u1(.clk_in(i_clk), .clk_25(clk25), .clk_16(clk16), .clk_32(clk32), .clk_8(clk8));
   
   vga u2(.clk_25(clk25), .vs(vs), .hs(hs), .vpixel(vcount), .hpixel(hcount));
   
  draw_new u3(.clk_25(clk25),.clk_16(clk16),.clk_32(clk32),.clk_8(clk8),.pause(pause),.switchOne(so),.switchTwo(st),  .v_count(vcount), .h_count(hcount), .rgb(rgb), .rst(rst), .jump(jump));
   
endmodule
