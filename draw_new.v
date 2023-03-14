`timescale 1 ns / 1 ns

//yws
module draw_new(clk_25, v_count, h_count, rgb, rst, jump);
input               clk_25;
input     [9:0]     v_count;
input     [9:0]     h_count;
input               rst;
input               jump;
output    [7:0]     rgb;
reg       [7:0]     rgb;
   
reg       [9:0]     box_x = 10'd400;
reg       [9:0]     box_y = 10'd200;
parameter [6:0]     box_height = 7'b1001000;
parameter [6:0]     box_width = 7'b1001000;
   
parameter [9:0]     porchleft = 10'b0010010000;   //144
parameter [9:0]     porchtop = 10'b0000100100;    //36
parameter [9:0]     porchbottom = 10'b0111110100; //500
parameter [9:0]     porchright = 10'b1100010000;  //784

parameter BLACK = 8'b000_000_00;
parameter DEFAULT_X = 10'd400;
parameter DEFAULT_Y = 10'd200;
  
reg                 flag_up;
reg                 flag_left;
reg       [5:0]     velocity = 6'd31;   ////pixels/cycle
parameter [5:0] 		velocity_offset  = 6'd31;
                                
reg       [7:0]     accel = 8'd1; //(downwards)
  //6 bits: 0-63

wire [7:0]  rom_dout; 
wire [15:0] addr;
//synthesis attribute box_type <akalin> "black_box" 
//akalin akalin(
//	.clka(clk_25),
//	.addra(addr),
//	.douta(rom_dout)
//	);
assign addr = ((v_count-box_y)*16'd72+(h_count-box_x)); 

always @(posedge clk_25)
//////////////////////////////////////////////////////////////////////
begin //DISPLAY
	if ((h_count >= box_x) & (h_count < box_x + box_width) & (v_count >= box_y) & (v_count < box_y + box_height))
		rgb = 8'b11100011;
	else
		rgb = 8'b00000000;


/////////////////////////////////////////////////////////////////////
  //GAME LOGIC - start of draw cycle
  if (h_count == 10'b0000000001 & v_count == 10'b0000000001) 
		begin
      if (rst) //rst
        begin
          box_y = DEFAULT_Y;
          velocity = 6'd31;
        end
      else if (box_y + box_height == porchbottom - 1'b1) //if at or below bottom, start move up
        begin
			velocity = 6'd10;//flag_up <= 1'b1;
			//box_y = porchbottom - box_height-50;
		  end

	     box_y = box_y + (velocity - velocity_offset);//1'b1;  //move by velocity
		  velocity = velocity + accel;  //pos velocity is down
	  end
end
   
endmodule
