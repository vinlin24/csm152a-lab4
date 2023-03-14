`timescale 1 ns / 1 ns
module clk_div(clk_in, clk_25);

input       clk_in;
output      clk_25;

reg         clk_25;
reg [1:0]   clkdiv;

parameter   killclk = 2'b01;

always @(posedge clk_in)
	begin
		clkdiv <= clkdiv + 1'b1;
		if (clkdiv == killclk)
			begin
			clk_25 <= ~clk_25;
			clkdiv <= 0;
			end
	end

endmodule
