from akon.ast.nodes import Node

def print_ast(node: Node, indent="", is_last=True):
    """
    Pretty-print an AST tree in a generic way.
    """

    if node is None:
        return

    # Node name
    node_name = node.__class__.__name__

    # Tree branches
    branch = "└── " if is_last else "├── "
    print(indent + branch + node_name)

    # New indentation
    new_indent = indent + ("    " if is_last else "│   ")

    # Collect child attributes
    children = []

    for attr, value in vars(node).items():
        if isinstance(value, list):
            for item in value:
                if hasattr(item, "__dict__"):
                    children.append((attr, item))
        elif hasattr(value, "__dict__"):
            children.append((attr, value))
        else:
            # Leaf attribute (value, name, operator, etc.)
            print(new_indent + f"├── {attr}: {value}")

    # Print children nodes
    for i, (_, child) in enumerate(children):
        print_ast(child, new_indent, i == len(children) - 1)
