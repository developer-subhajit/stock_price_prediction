import matplotlib.pyplot as plt
import streamlit as st


def draw_neural_net(ax, left, right, bottom, top, layer_sizes):
    """
    Draw a neural network cartoon using matplotlib.

    Parameters:
        ax: matplotlib.axes.Axes
            The axes on which to plot the cartoon (get e.g. by plt.gca())
        left: float
            The center of the leftmost node(s) will be placed here
        right: float
            The center of the rightmost node(s) will be placed here
        bottom: float
            The center of the bottommost node(s) will be placed here
        top: float
            The center of the topmost node(s) will be placed here
        layer_sizes: list of int
            List of layer sizes, including input and output dimensionality
    """
    v_spacing = (top - bottom) / float(max(layer_sizes))
    h_spacing = (right - left) / float(len(layer_sizes) - 1)

    # Nodes
    for n, layer_size in enumerate(layer_sizes):
        layer_top = v_spacing * (layer_size - 1) / 2.0 + (top + bottom) / 2.0
        for m in range(layer_size):
            circle = plt.Circle(
                (n * h_spacing + left, layer_top - m * v_spacing),
                v_spacing / 4.0,
                color="w",
                ec="k",
                zorder=5,
            )
            ax.add_artist(circle)

            # Add node number
            plt.text(n * h_spacing + left, layer_top - m * v_spacing, f"{m+1}", ha="center", va="center", fontsize=10)

            # Annotation
            if n == 0:
                plt.annotate(
                    "Input",
                    xy=(n * h_spacing + left, (top + bottom) / 2),
                    xytext=(-20, 20),
                    textcoords="offset points",
                    ha="center",
                    va="center",
                    fontsize=12,
                )
            elif n == len(layer_sizes) - 1:
                plt.annotate(
                    "Output",
                    xy=(n * h_spacing + left, (top + bottom) / 2),
                    xytext=(20, 20),
                    textcoords="offset points",
                    ha="center",
                    va="center",
                    fontsize=12,
                )
            else:
                plt.annotate(
                    f"",
                    xy=(n * h_spacing + left, (top + bottom) / 2),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center",
                    va="center",
                    fontsize=12,
                )

    # Edges
    for n, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        layer_top_a = v_spacing * (layer_size_a - 1) / 2.0 + (top + bottom) / 2.0
        layer_top_b = v_spacing * (layer_size_b - 1) / 2.0 + (top + bottom) / 2.0
        for m in range(layer_size_a):
            for o in range(layer_size_b):
                line = plt.Line2D(
                    [n * h_spacing + left, (n + 1) * h_spacing + left],
                    [layer_top_a - m * v_spacing, layer_top_b - o * v_spacing],
                    c="k",
                )
                ax.add_artist(line)


def main():
    # Set title
    st.title("Neural Network Architecture Diagram")

    # Add checkbox for default or customize
    default_settings = st.checkbox("Default settings", value=True)

    if default_settings:
        # Default settings
        num_hidden_layers = 2
        hidden_layer_sizes = [4, 4]
    else:
        # Ask user for the number of hidden layers and the number of nodes in each hidden layer
        num_hidden_layers = st.number_input(
            "Enter the number of hidden layers", min_value=1, max_value=10, value=2, step=1
        )
        hidden_layer_sizes = []
        for i in range(num_hidden_layers):
            layer_size = st.number_input(
                f"Enter the number of nodes in hidden layer {i+1}", min_value=1, max_value=100, value=4, step=1
            )
            hidden_layer_sizes.append(layer_size)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Draw neural network diagram
    draw_neural_net(ax, left=0.1, right=0.9, bottom=0.1, top=0.9, layer_sizes=[1] + hidden_layer_sizes + [1])

    # Set axis properties
    ax.axis("off")

    # Display diagram
    st.pyplot(fig)


if __name__ == "__main__":
    main()
