import pyverilog.vparser.ast as vast

from node import Node
from node_type import NodeType
from circuit_graph import CircuitGraph

def parse_ast(ast):
    """Parses a Verilog abstract syntax tree into a CircuitGraph.

    Args:
        ast: the pyverilog AST

    Returns:
        CircuitGraph: the graph representation of the circuit

    """
    ast_parser = ASTParser()

    return ast_parser.parse(ast)

class ASTParser():
    def __init__(self):
        self.nodes = {}
        self.outputs = []
        self.inputs = []
        self.assigns = []

    def parse(self, ast):
        """Parses a Verilog AST into a Circuit Graph.

        Args:
            ast: the pyverilog AST

        Returns:
            CircuitGraph: the graph representation of the circuit

        """
        description = ast.children()[0]
        moduledef = description.children()[0]

        for child in moduledef.children()[2:]:
            if isinstance(child, vast.Decl):
                self._parse_decl(child)
            elif isinstance(child, vast.InstanceList):
                self._parse_instance_list(child)
            elif isinstance(child, vast.Assign):
                self._parse_assign(child)
            else:
                import pdb; pdb.set_trace()

        if len(self.assigns) > 0:
            for output in self.outputs:
                self._remove_assigns(output, None, set())

            self._delete_assigns()

        return CircuitGraph(self.nodes, self.outputs, self.inputs)

    def _parse_decl(self, decl):
        """Parses a Verilog declaration.

        A declaration can be an input, output, or wire statement.

        Args:
            decl: the pyverilog declaration object

        """
        for child in decl.children():
            if isinstance(child, vast.Input):
                self._parse_input(child)
            elif isinstance(child, vast.Output):
                self._parse_output(child)
            elif isinstance(child, vast.Wire):
                self._parse_wire(child)
            else:
                import pdb; pdb.set_trace()

    def _parse_input(self, input):
        """Parses a Verilog input.

        Args:
            input: the pyverilog input object

        """
        base_name = input.name

        if input.width is not None:
            for i in range(int(input.width.lsb.value), int(input.width.msb.value) + 1):
                name = base_name + "_" + str(i)
                self.nodes[name] = Node(name, [], NodeType.INPUT)
                self.inputs.append(name)
        else:
            if "key" in base_name:
                self.nodes[base_name] = Node(base_name, [], "Key Input")
            else:
                self.nodes[base_name] = Node(base_name, [], "Primary Input")

            self.inputs.append(base_name)

    def _parse_output(self, output):
        """Parses a Verilog output.

        Args:
            input: the pyverilog output object

        """
        base_name = output.name

        if output.width is not None:
            for i in range(int(output.width.lsb.value), int(output.width.msb.value) + 1):
                name = base_name + "_" + str(i)
                self.nodes[name] = Node(name, [], NodeType.OUTPUT)
                self.outputs.append(name)
        else:
            self.nodes[base_name] = Node(base_name, [], NodeType.OUTPUT)
            self.outputs.append(base_name)


    def _parse_wire(self, wire):
        """Parses a Verilog wire.

        Args:
            wire: the pyverilog wire object

        """
        name = wire.name
        self.nodes[name] = Node(name, [], NodeType.WIRE)

    def _parse_instance_list(self, ilist):
        """Parses a Verilog instance list.

        An "instance list" is a single gate declaration.

        Args:
            ilist: the pyverilog instance list object.

        """
        itype = ilist.module
        instance = ilist.children()[0]

        output, inputs = self._parse_portargs(instance)

        # output = self._parse_arg(instance.children()[0])
        # inputs = [self._parse_arg(c) for c in instance.children()[1:]]

        if not output in self.nodes:
            self.nodes[output] = Node(output, [], "wire")

        self.nodes[output].inputs = inputs
        self.nodes[output].type = itype.lower()

    def _parse_portargs(self, instance):
        inputs = []
        output = None

        for i, portarg in enumerate(instance.children()):
            port = portarg.portname
            name = self._parse_arg(portarg)

            if port is None and i == 0:
                output = name
            elif port == "Y":
                output = name
            else:
                inputs.append(name)

        return output, inputs

    def _parse_arg(self, arg):
        """Parses a Verilog argument.

        An argument is a variable name. This method assumes the argument is of width one. It
        can be a single wire or part of a bus, but it does not support something like w1[3:0]

        Args:
            arg: the pyverilog argument

        """
        if isinstance(arg.children()[0], vast.Identifier):
            return str(arg.children()[0].name)
        elif isinstance(arg.children()[0], vast.Pointer):
            return str(arg.children()[0].var) + "_" + str(arg.children()[0].ptr)
        elif isinstance(arg.children()[0], vast.IntConst):
            return int(str(arg.children()[0])[0])
        else:
            import pdb; pdb.set_trace()

    def _parse_assign(self, assign):
        """Parses a Verilog assign statement.

        Args:
            assign: the pyverilog assign statement

        """
        left_arg = self._parse_arg(assign.left)
        right_arg = self._parse_arg(assign.right)
        self.assigns.append(left_arg)

        if not left_arg in self.nodes:
            self.nodes[left_arg] = Node(left_arg, [], "wire")

        self.nodes[left_arg].inputs = [right_arg]
        self.nodes[left_arg].type = "assign"

    def _remove_assigns(self, name, prev_name, visited):
        """Removes all references to assign nodes from a circuit graph.

        The assign nodes are not a part of the actual circuit and as such do not need to be in the graph.
        This method recursively removes all assign nodes from the graph. The nodes still exist in the graph
        must be deleted after calling this method. However, there will be no references to them.

        Args:
            name: the name of the root node to remove assigns from
            prev_name: the name of the parent of the root node

        """
        visited.add(name)
        if self.nodes[name].type == "assign":
            RHS = self.nodes[name].inputs[0]
            LHS = self.nodes[name].name

            if prev_name is None:
                # Occurs only when name is an output, we rename the output and move on
                self.outputs = [RHS if o == LHS else o for o in self.outputs]
                self._remove_assigns(RHS, prev_name, visited)
            elif prev_name in self.nodes:
                # We must swap the name of the input. The input name is the LHS, we swap
                # it to the RHS
                prev_node = self.nodes[prev_name]
                prev_node.inputs = [RHS if i == LHS else i for i in prev_node.inputs]

                self._remove_assigns(RHS, prev_name, visited)
            else:
                import pdb; pdb.set_trace()
        else:
            # This isn't an assign node, check all children
            for i in self.nodes[name].inputs:
                if i not in visited:
                    self._remove_assigns(i, name, visited)

    def _delete_assigns(self):
        """Deletes all assign nodes from a circuit graph.

        The method _remove_assigns removes all references. This method
        removes the actual nodes.

        """
        for name in self.assigns:
            del self.nodes[name]
