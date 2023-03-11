module clk_div(
	// Inputs
	input wire clk,						//master clock: 50MHz
	input wire rst,						//asynchronous reset
	// Outputs
	output wire dclk//,						pixel clock: 25MHz
	//output wire flying_saucer_clk,	//flying saucer clock: 1000Hz 
	//output wire alien_clk				//alien clock: 100Hz
	);

reg [1:0] pixel_count;
reg pixel_clk_reg;

initial begin
	pixel_count = 0;
	pixel_clk_reg = 0;
end

always @(posedge clk or posedge rst)
begin
	if (rst == 1) begin
		pixel_count <= 0;
		pixel_clk_reg <= 0;
	end
	else if (pixel_count == 1) begin
		pixel_count <= 0;
		pixel_clk_reg <= ~pixel_clk_reg;
	end
	else begin
		pixel_count <= pixel_count + 1;
		pixel_clk_reg <= pixel_clk_reg;
	end
end
 
assign dclk = pixel_clk_reg;

endmodule 