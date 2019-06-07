from methods import square_and_multiply_graph, square_and_multiply_always_graph, montgomery_ladder_graph, to_base2

# Run timing experiment
p = 54987991
e = 66634
e_b = to_base2(e)
n = 988027
# print(bin(e))

square_and_multiply_graph(p, n, e_b)
square_and_multiply_always_graph(p, n, e_b)
montgomery_ladder_graph(p, n, e_b)
