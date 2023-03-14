`timescale 1 ns / 1 ns
module clk_div(clk_in, clk_25, clk_16);

input       clk_in;
output      clk_25;
output      clk_16;

reg         clk_25;
reg [1:0]   clkdiv25;
reg [31:0]   clkdiv16;

parameter   killclk25 = 2'b01;
parameter   killclk16 = 22'b1011111010111100000111;

always @(posedge clk_in)
	begin
		clkdiv25 <= clkdiv25 + 1'b1;
		if (clkdiv25 == killclk25)
			begin
			clk_25 <= ~clk_25;
			clkdiv25 <= 0;
			end
		clkdiv16 <= clkdiv16 + 1'b1;
		if (clkdiv16 == killclk16)
			begin
			clk_16 <= ~clk_16;
			clkdiv16 <= 0;
			end
	end



endmodule
