`timescale 1 ns / 1 ns

//yws
module controlLogic(sysClk, clk_16, frameClk);
input               sysClk;
input               clk_16;

output frameClk;
   


always @(posedge clk_25)
begin //DISPLAY (rrrgggbb)
	rgb = 8'b11100011;//rgb for the correct pixel (from above logic)
end
   
endmodule
