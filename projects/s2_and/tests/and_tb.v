module and_testbench;
reg a, b;
wire y;
m_and test_and(a, b, y);

initial begin
    a = 1;
    b = 1;
    #1;
    $display("1,%d,2", ((a & b) == y) * 2);
    #1;
    a = 0;
    b = 1;
    #1;
    $display("2,%d,2", ((a & b) == y) * 2);
    a = 1;
    b = 0;
    #1;
    $display("3,%d,2", ((a & b) == y) * 2);
    #1;
    a = 0;
    b = 0;
    #1;
    $display("4,%d,2", ((a & b) == y) * 2);

end

initial begin
    $dumpfile("dumpfile.vcd");
    $dumpvars(0, test_and);
end
endmodule