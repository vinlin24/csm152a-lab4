`timescale 1 ns / 1 ns

//yws
module frameGetter(frameClk, clk_25, v_count, h_count, rgb);
input               frameClk;
input               clk_25;
input     [9:0]     v_count;
input     [9:0]     h_count;
output    [7:0]     rgb;
reg       [7:0]     rgb;
   

//Pixel Coordinate: (x,y) -> (h_count,v_count)

//TODO: fill in the logic to read in the correct frame here
always @(posedge frameClk)
begin

end

always @(posedge clk_25)
begin //DISPLAY (rrrgggbb)
	rgb = 8'b11100011;//rgb for the correct pixel (from above logic)
end
   
endmodule
