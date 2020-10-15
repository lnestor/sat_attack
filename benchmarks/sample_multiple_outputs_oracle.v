`timescale 1ns / 1ps
module sample (G1,G2,G3,key);

input G1, G2, G3, key1, key2;
output G10, G11;

wire G100, G101, G102;

and AND(G100, G1, G2);
not NOT(G10, G100);
not NOT(G101, G2);
not NOT(G102, G3);
or OR(G11, G101, G102);

endmodule
