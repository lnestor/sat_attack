`timescale 1ns / 1ps
module sample(I1, I2, I3, I4, I5, I6, I7, O1, O2, O3);

input I1, I2, I3, I4, I5, I6, I7;
output O1, O2, O3;

wire W1, W2, W3;
wire [0:2] bus;

and AND(W1, I1, I2);
not NOT(W2, I3);
or OR(bus[0], W1, W2);
and AND(O1, I4, bus[0]);
not NOT(bus[1], I4);
and AND(O2, I5, bus[1]);
or OR(W3, I6, I7);
not NOT(bus[2], W3);
or OR(O3, bus[2], W2);

endmodule
