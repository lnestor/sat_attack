`timescale 1ns / 1ps
module sample (G1, G2, G3);

input G1, G2;
output G3;

and AND(G3, G1, G2);

endmodule
