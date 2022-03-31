def generate_table(input_vars, output_vars, output_values=[]):
    """
    docstring
    """
    # Extract variables from arguments
    n_of_inputs = len(input_vars)
    n_of_rows = 2**n_of_inputs
    n_of_outputs = len(output_vars)

    # Argument validation
    if n_of_inputs < 1 or n_of_outputs < 1:
        raise ValueError

    # Begin table
    table = "\\begin{array}{" + "c " * n_of_inputs + "|" + " c" * n_of_outputs + "}\n"

    # Create table header
    table += "\t"
    for inv in input_vars:
        table += inv + " & "
    for outv in output_vars:
        table += outv + (" " if outv == output_vars[-0] else " & ")
    table += "\\\\\n"
    table += "\t\\hline\n"

    # Create table body
    for m in range(n_of_rows):
        # Generate binary value and pad it with 0s
        m = bin(m)[2:].zfill(n_of_inputs)
        table += '\t'
        # Insert input values
        for i in range(n_of_inputs):
            table += m[i] + (" " if i == n_of_inputs-1 else " & ")
        # insert output values or leave blank space
        if n_of_outputs == n_of_rows:
            for val in output_values[m]:
                val = str(val)
                table += f"& {val.strip()} "
        else:
            for i in range(n_of_outputs):
                table += "&  "
        table += "\\\\\n"
    
    # End table
    table += "\\end{array}"

    # Return the finished table
    return table

if __name__ == "__main__":
    print(generate_table(['x_1', 'x_2', 'x_3', 'x_4', 'x_5'], ['f(x_1, x_2, x_3, x_4, x_5)']))