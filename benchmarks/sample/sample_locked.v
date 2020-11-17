`timescale 1ns / 1ps
module sample(I1, I2, I3, I4, I5, I6, I7, keyIn_0_1, keyIn_0_2, keyIn_0_3, keyIn_0_4, O1, O2, O3);

input I1, I2, I3, I4, I5, I6, I7;
input keyIn_0_1, keyIn_0_2, keyIn_0_3, keyIn_0_4;
output O1, O2, O3;

wire W1, W2, W3, W4;
wire [0:3] bus;

and AND(W1, I1, I2);
not NOT(W2, I3);
or OR(W4, W1, W2);
xor KeyGate_0_0(bus[0], keyIn_0_4, W4);
and AND(O1, I4, bus[0]);
xor KeyGate_0_1(bus[1], keyIn_0_2, I4);
and AND(bus[2], I5, bus[1]);
xor KeyGate_0_2(O2, keyIn_0_3, bus[2]);
or OR(W3, I6, I7);
xor KeyGate_0_3(bus[3], keyIn_0_1, W3);
or OR(O3, bus[3], W2);

endmodule
