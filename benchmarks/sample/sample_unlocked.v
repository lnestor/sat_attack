`timescale 1ns / 1ps
module sample(I1, I2, I3, I4, I5, I6, I7, O1, O2, O3);

input I1, I2, I3, I4, I5, I6, I7;
output O1, O2, O3;

wire W1, W2, W3, W5, W6, W8;

and AND(W1, I1, I2);
not NOT(W2, I3);
or OR(W5, W1, W2);
and AND(O1, I4, W5);
not NOT(W6, I4);
and AND(O2, I5, W6);
or OR(W3, I6, I7);
not NOT(W8, W3);
or OR(O3, W8, W2);

endmodule
