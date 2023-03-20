`timescale 1 ns / 1 ns


module vga(clk_25, vs, hs, vpixel, hpixel);
input              clk_25;
output             vs;
output             hs;
output    [9:0]    vpixel;
output    [9:0]    hpixel;
   
parameter [9:0]    hpixel_temp = 10'b1100100000;
parameter [9:0]    vpixel_temp = 10'b1000001001;
   
parameter [9:0]    hspluse_wide = 10'b0001100000;
parameter [2:0]    vspluse_wide = 3'b010;
   
reg                synch;
reg                syncv;
   
reg       [9:0]    h_count;
reg       [9:0]    v_count;
initial begin
	h_count=0;
	v_count=0;
end
always @(posedge clk_25)
begin
	if (h_count == hpixel_temp - 1'b1)
		begin
			synch <= 1'b1;
			h_count <= 10'b0000000000;
			v_count <= v_count + 1'b1;
		end
	else
		h_count <= h_count + 1'b1;
	if (v_count == vpixel_temp - 1'b1)
		begin
			syncv <= 1'b1;
			v_count <= 10'b0000000000;
		end
	if (synch == 1'b1)
		begin
			if (h_count + 1'b1 == hspluse_wide)
				synch <= 1'b0;
		end
	if (syncv == 1'b1)
		begin
			if (v_count == vspluse_wide)
				syncv <= 1'b0;
		end
end

assign vs = syncv;
assign hs = synch;
assign vpixel = v_count;
assign hpixel = h_count;
   
endmodule
