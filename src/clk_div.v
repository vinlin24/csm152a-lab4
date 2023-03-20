`timescale 1 ns / 1 ns
module clk_div(clk_in, clk_25,clk_16,clk_32,clk_8);

input       clk_in;
output      clk_25,clk_16,clk_32,clk_8;

reg         clk_25;
reg [1:0]   clkdiv;
reg         clk_16;
reg [31:0]   clkdiv16;
reg         clk_32;
reg [31:0]   clkdiv32;
reg         clk_8;
reg [31:0]   clkdiv8;

parameter   killclk = 2'b01;
parameter   killclk16 = 24999999;
parameter   killclk32 = 12499999;
parameter   killclk8 = 49999999;

always @(posedge clk_in)
	begin
		clkdiv <= clkdiv + 1'b1;
		if (clkdiv == killclk)
			begin
			clk_25 <= ~clk_25;
			clkdiv <= 0;
			end

		clkdiv16 <= clkdiv16 + 1'b1;
		if (clkdiv16 == killclk16)
			begin
			clk_16 <= ~clk_16;
			clkdiv16 <= 0;
			end

		clkdiv32 <= clkdiv32 + 1'b1;
		if (clkdiv32 == killclk32)
			begin
			clk_32 <= ~clk_32;
			clkdiv32 <= 0;
			end

		clkdiv8 <= clkdiv8 + 1'b1;
		if (clkdiv8 == killclk8)
			begin
			clk_8 <= ~clk_8;
			clkdiv8 <= 0;
			end
	end

endmodule
