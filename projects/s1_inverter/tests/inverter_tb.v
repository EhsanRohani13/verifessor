module inv_testbench;

reg test_result;

reg x;
wire y;
inverter test_inverter(x, y);

initial begin
    x = 1;
    #1;
    $display("1,%d,2", (x != y) * 2);
    #1;
    x = 0;
    #1;
    $display("2,%d,2", (x != y) * 2);
    for (integer i = 0; i < 1; i++) begin
        x = ~x;
        #1;
    end
end

initial begin
    $dumpfile("dumpfile.vcd");
    $dumpvars(0, test_inverter);
end
endmodule