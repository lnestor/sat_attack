// Verilog File 
module c17_aor_8bit.bench (N1,N2,N3,N6,N7,keyinput0,keyinput1,keyinput2,keyinput3,
keyinput4,keyinput5,keyinput6,keyinput7,N22,N23);

input N1,N2,N3,N6,N7,keyinput0,keyinput1,keyinput2,keyinput3,
keyinput4,keyinput5,keyinput6,keyinput7;


output N22, N23;

wire n14, xenc3, xenc5, iw_1, iw_2, iw_3, n12, iw_4, iw_5, 
n13, iw_6, xenc2, xenc0, n15, iw_9, n16, n17, n18, n19, 
n20, xenc1, iw_0, xenc7, xenc6, iw_7, iw_8, xenc4;

not g0(xenc3, n14);
and g1(N23, xenc5, iw_1);
and g2(n12, iw_2, iw_3);
and g3(n13, iw_4, iw_5);
and g4(n14, iw_6, xenc2);
and g5(n15, xenc5, xenc0);
and g6(n16, iw_2, iw_9);
not g7(n17, N3);
not g8(n18, N1);
not g9(n19, N2);
not g10(n20, N6);
not g11(iw_0, xenc1);
not g12(iw_1, xenc7);
not g13(iw_2, xenc6);
not g14(iw_3, n20);
not g15(iw_4, N2);
not g16(iw_5, N7);
not g17(iw_6, n15);
not g18(iw_7, n16);
not g19(iw_8, n19);
not g20(iw_9, xenc4);
and g21(xenc0, iw_8, keyinput0);
or g22(xenc1, n12, keyinput1);
or g23(xenc2, iw_7, keyinput2);
and g24(N22, xenc3, keyinput3);
or g25(xenc4, n18, keyinput4);
or g26(xenc5, iw_0, keyinput5);
or g27(xenc6, n17, keyinput6);
and g28(xenc7, n13, keyinput7);
endmodule
