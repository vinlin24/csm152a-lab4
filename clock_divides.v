`define MASTER_CLOCK_HERTZ 50000000

module clk_div(
    // Inputs
    input wire clk,     // Master clock: 50MHz
    input wire rst,     // Asynchronous reset
    // Outputs
    output wire new_clk // Frequency equal to param hertz
);

    parameter integer HERTZ = 16;

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
        else if (pixel_count == `MASTER_CLOCK_HERTZ / HERTZ) begin
            pixel_count <= 0;
            pixel_clk_reg <= ~pixel_clk_reg;
        end
        else begin
            pixel_count <= pixel_count + 1;
            pixel_clk_reg <= pixel_clk_reg;
        end
    end

    assign new_clk = pixel_clk_reg;

endmodule
