module top(
	// Inputs
	input wire clk,
	// Buttons
	input wire button_display,
	// Outputs
	output [7:0] rgb,
	output wire hsync,
	output wire vsync
    );

	// Wires for horizontal and vertical counters
	wire [9:0] xCoord;
	wire [9:0] yCoord;
	
	// Wires for clocks
	wire dclk;
	
	// Generate display clock and in-game clock
	clk_div clk_div(
		.clk(clk),
		.rst(button_display),
		.dclk(dclk)
	);
	
	// VGA controller
	vga_controller controller(
		.clk(dclk),
		.rst(button_display),
		.hsync(hsync),
		.vsync(vsync),
		.xCoord(xCoord),
		.yCoord(yCoord)
	);
	
	// VGA display
	vga_display display(
		.clk(clk),
		.xCoord(xCoord),
		.yCoord(yCoord),
		.rgb(rgb)
	);

endmodule