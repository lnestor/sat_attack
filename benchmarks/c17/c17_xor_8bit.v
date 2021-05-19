// Verilog File 
module c17_xor_8bit.bench (N1,N2,N3,N6,N7,keyinput0,keyinput1,keyinput2,keyinput3,
keyinput4,keyinput5,keyinput6,keyinput7,N22,N23);

input N1,N2,N3,N6,N7,keyinput0,keyinput1,keyinput2,keyinput3,
keyinput4,keyinput5,keyinput6,keyinput7;


output N22, N23;

wire n14, xenc4, iw_0, xenc6, iw_2, iw_3, n12, xenc5, iw_5, 
n13, xenc2, xenc7, xenc3, n15, iw_9, n16, n17, n18, n19, 
n20, iw_1, xenc0, iw_4, xenc1, iw_6, iw_7, iw_8;

not g0(xenc4, n14);
and g1(N23, iw_0, xenc6);
and g2(n12, iw_2, iw_3);
and g3(n13, xenc5, iw_5);
and g4(n14, xenc2, xenc7);
and g5(n15, iw_0, xenc3);
and g6(n16, iw_2, iw_9);
not g7(n17, N3);
not g8(n18, N1);
not g9(n19, N2);
not g10(n20, N6);
not g11(iw_0, n12);
not g12(iw_1, n13);
not g13(iw_2, xenc0);
not g14(iw_3, n20);
not g15(iw_4, N2);
not g16(iw_5, N7);
not g17(iw_6, xenc1);
not g18(iw_7, n16);
not g19(iw_8, n19);
not g20(iw_9, n18);
xor g21(xenc0, n17, keyinput0);
xor g22(xenc1, n15, keyinput1);
xor g23(xenc2, iw_6, keyinput2);
xnor g24(xenc3, iw_8, keyinput3);
xnor g25(N22, xenc4, keyinput4);
xnor g26(xenc5, iw_4, keyinput5);
xor g27(xenc6, iw_1, keyinput6);
xnor g28(xenc7, iw_7, keyinput7);
endmodule
