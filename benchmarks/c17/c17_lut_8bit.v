// Verilog File 
module c17_lut_8bit.bench (N1,N2,N3,N6,N7,keyinput0_1,keyinput0_0,keyinput1_0,keyinput2_0,
keyinput3_0,keyinput1_1,keyinput2_1,keyinput3_1,N22,N23);

input N1,N2,N3,N6,N7,keyinput0_1,keyinput0_0,keyinput1_0,keyinput2_0,
keyinput3_0,keyinput1_1,keyinput2_1,keyinput3_1;


output N22, N23;

wire n14, iw_0, iw_1, iw_2, iw_3, n12, iw_4, iw_5, n13, 
iw_8, n15, n17, n18, n19, n20, iw_6, iw_9, iw_7, in0not_0, 
in1not_0, T0_0, T1_0, T2_0, T3_0, in0not_1, in1not_1, T0_1, T1_1, T2_1, 
T3_1;

not g0(N22, n14);
and g1(N23, iw_0, iw_1);
and g2(n12, iw_2, iw_3);
and g3(n13, iw_4, iw_5);
and g4(n15, iw_0, iw_8);
not g5(n17, N3);
not g6(n18, N1);
not g7(n19, N2);
not g8(n20, N6);
not g9(iw_0, n12);
not g10(iw_1, n13);
not g11(iw_2, n17);
not g12(iw_3, n20);
not g13(iw_4, N2);
not g14(iw_5, N7);
not g15(iw_6, n15);
not g16(iw_8, n19);
not g17(iw_9, n18);
not g18(in0not_0, iw_7);
not g19(in1not_0, iw_6);
and g20(T0_0, keyinput0_0, in0not_0, in1not_0);
and g21(T1_0, keyinput1_0, iw_7, in1not_0);
and g22(T2_0, keyinput2_0, in0not_0, iw_6);
and g23(T3_0, keyinput3_0, iw_7, iw_6);
or g24(n14, T0_0, T1_0, T2_0, T3_0);
not g25(in0not_1, iw_9);
not g26(in1not_1, iw_2);
and g27(T0_1, keyinput0_1, in0not_1, in1not_1);
and g28(T1_1, keyinput1_1, iw_9, in1not_1);
and g29(T2_1, keyinput2_1, in0not_1, iw_2);
and g30(T3_1, keyinput3_1, iw_9, iw_2);
or g31(iw_7, T0_1, T1_1, T2_1, T3_1);
endmodule
