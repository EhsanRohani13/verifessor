module inv_testbench;

reg x;
wire y;
inverter test_inverter(x, y);

initial begin
    x = 1;
    #1;
    // if (x != y)
    //     $finish_and_return(1);
    $display("%d: %d", x, y);
    #1;
    x = 0;
    #1;
    $display("%d: %d", x, y);
end

initial begin
    $dumpfile("my_dumpfile.vcd");
    $dumpvars(0, test_inverter);
end
endmodule