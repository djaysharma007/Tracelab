import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StringVisualizer:
    """
    Visualizes intermediate states generated
    by string-matching algorithms.
    """

    def __init__(self, text, pattern, states, algorithm):

        self.text = text
        self.pattern = pattern
        self.states = states
        self.algorithm = algorithm

        self.fig, self.ax = plt.subplots(
            figsize=(12, 5)
        )

    def draw_text(self, text_index=None, pattern_index=None):

        self.ax.clear()

        # -----------------------------
        # Text
        # -----------------------------

        self.ax.text(
            0.02,
            0.75,
            "TEXT:",
            fontsize=14,
            fontweight="bold",
            transform=self.ax.transAxes
        )

        for i, char in enumerate(self.text):

            x = 0.02 + i * 0.055

            self.ax.text(
                x,
                0.55,
                char,
                fontsize=18,
                ha="center"
            )

        # -----------------------------
        # Pattern
        # -----------------------------

        self.ax.text(
            0.02,
            0.30,
            "PATTERN:",
            fontsize=14,
            fontweight="bold",
            transform=self.ax.transAxes
        )

        pattern_position = 0

        if text_index is not None:
            pattern_position = max(
                0,
                text_index - (
                    pattern_index
                    if pattern_index is not None
                    else 0
                )
            )

        for i, char in enumerate(self.pattern):

            x = (
                0.02
                + (pattern_position + i)
                * 0.055
            )

            self.ax.text(
                x,
                0.10,
                char,
                fontsize=18,
                ha="center"
            )

        self.ax.set_xlim(0, max(
            1,
            len(self.text) * 0.055 + 0.1
        ))

        self.ax.set_ylim(0, 1)

        self.ax.axis("off")

        self.ax.set_title(
            f"{self.algorithm} - String Matching"
        )

    def animate(self):

        comparison_states = [
            state
            for state in self.states
            if state["type"] in {
                "comparison",
                "match",
                "mismatch",
                "alignment"
            }
        ]

        if not comparison_states:

            self.draw_text()
            plt.show()
            return

        def update(frame):

            state = comparison_states[frame]

            state_type = state["type"]

            if state_type == "comparison":

                self.draw_text(
                    state["text_index"],
                    state["pattern_index"]
                )

                self.ax.text(
                    0.02,
                    0.90,
                    "Comparing characters...",
                    fontsize=12
                )

            elif state_type == "mismatch":

                self.draw_text(
                    state["text_index"],
                    state["pattern_index"]
                )

                self.ax.text(
                    0.02,
                    0.90,
                    "Mismatch",
                    fontsize=12
                )

            elif state_type == "match":

                position = state["position"]

                self.draw_text(
                    position,
                    0
                )

                self.ax.text(
                    0.02,
                    0.90,
                    f"Pattern found at index {position}",
                    fontsize=12
                )

            else:

                self.draw_text()

                self.ax.text(
                    0.02,
                    0.90,
                    f"Pattern alignment: {state['position']}",
                    fontsize=12
                )

        animation = FuncAnimation(
            self.fig,
            update,
            frames=len(comparison_states),
            interval=500,
            repeat=False
        )

        # Keep reference to animation
        self.animation = animation

        plt.show()