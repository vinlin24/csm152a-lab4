module clk_div(
    // Inputs
    input wire clk,   // master clock: 50MHz
    input wire rst,   // asynchronous reset
    // Outputs
    output wire dclk  // pixel clock: 16Hz (3.125M master clock pulses)
);

    integer pixel_count;
    reg pixel_clk_reg;

    initial begin
        pixel_count = 0;
        pixel_clk_reg = 0;
    end

    always @(posedge clk or posedge rst) begin
        if (rst == 1) begin
            pixel_count <= 0;
            pixel_clk_reg <= 0;
        end
        else if (pixel_count == 3_125_000) begin
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
