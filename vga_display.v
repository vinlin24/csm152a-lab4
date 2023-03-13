module vga_display(
    // Inputs
    input wire clk,
    input wire [9:0] xCoord,
    input wire [9:0] yCoord,
    // Outputs
    output wire [7:0] rgb
);

    // RGB Parameters [ BLUE | GREEN | RED ]
    reg [7:0] set_color;
    parameter COLOR_BLACK = 8'b11111111;

    ////////////////////////////////////////////////////////////////////////////

    always @ (posedge clk) begin
        // Display visual (in valid screen display)
        if (xCoord >= 0 && xCoord < 640 && yCoord >= 0 && yCoord < 480) begin
            set_color <= COLOR_BLACK;
        end
    end

   assign rgb = set_color;

endmodule
