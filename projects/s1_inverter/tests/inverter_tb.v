module inv_testbench;

reg test_result;

reg x;
wire y;
inverter test_inverter(x, y);

initial begin
    x = 1;
    #1;
    $display("0,%d,2", x != y);
    #1;
    x = 0;
    #1;
    $display("1,%d,2", x != y);
    for (integer i = 0; i < 20; i++) begin
        x = ~x;
        #1;
    end
end

initial begin
    $dumpfile("dumpfile.vcd");
    $dumpvars(0, inv_testbench);
end
endmodule