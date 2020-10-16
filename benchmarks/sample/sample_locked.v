`timescale 1ns / 1ps
module sample(I1, I2, I3, I4, I5, I6, I7, key1, key2, key3, key4, O1, O2, O3);

input I1, I2, I3, I4, I5, I6, I7;
input key1, key2, key3, key4;
output O1, O2, O3;

wire W1, W2, W3, W4;
wire [0:3] bus;

and AND(W1, I1, I2);
not NOT(W2, I3);
or OR(W4, W1, W2);
xor KeyGate(bus[0], W4, key4);
and AND(O1, I4, bus[0]);
xor KeyGate(bus[1], I4, key2);
and AND(bus[2], I5, bus[1]);
xor KeyGate(O2, bus[2], key3);
or OR(W3, I6, I7);
xor KeyGate(bus[3], W3, key1);
or OR(O3, bus[3], W2);

endmodule
