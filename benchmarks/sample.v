`timescale 1ns / 1ps
module sample (G1,G2,G3,key);

input G1, G2, key;
output G3;

wire G4;

and AND(G4,G1,G2);
xor KeyGate(G3, key, G4);

endmodule
