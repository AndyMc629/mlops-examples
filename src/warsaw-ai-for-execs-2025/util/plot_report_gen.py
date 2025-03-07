import matplotlib.pyplot as plt
import mpld3


class PlotReportGenerator:
    """
    A utility class to generate HTML reports with embedded interactive Seaborn/Matplotlib plots.
    """

    def __init__(self, title="Analysis Report", output_file="report.html"):
        self.title = title
        self.output_file = output_file
        self.sections = []

    def add_plot(self, title, description, fig):
        """
        Add a new plot to the report.

        :param title: Title of the plot section.
        :param description: Explanation of the plot.
        :param fig: Matplotlib figure object.
        """
        plot_html = mpld3.fig_to_html(fig)
        section_html = (
            f"<div class='section'>"
            f"<h2>{title}</h2>"
            f"<p>{description}</p>"
            f"<div class='plot-container'>{plot_html}</div>"
            f"</div>"
        )
        self.sections.append(section_html)

    def generate_report(self):
        """
        Generates and saves the HTML report with all added plots.
        """
        html_content = (
            "<html>"
            "<head>"
            "<title>{self.title}</title>"
            "<style>"
            "body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding: 40px; }"
            ".container { width: 80%; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); }"
            "h1 { text-align: center; color: #2c3e50; font-size: 28px; margin-bottom: 20px; }"
            ".section { border: 1px solid #ddd; padding: 20px; margin: 20px auto; border-radius: 5px; background: #ffffff; text-align: left; width: 90%; box-shadow: 0px 3px 10px rgba(0,0,0,0.1); }"
            "h2 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 8px; font-size: 22px; margin-bottom: 10px; text-align: center; }"
            "p { font-size: 16px; color: #34495e; line-height: 1.6; text-align: justify; }"
            ".plot-container { text-align: center; margin-top: 10px; }"
            "</style>"
            "</head>"
            "<body>"
            "<div class='container'>"
            f"<h1>{self.title}</h1>"
            f"{''.join(self.sections)}"
            "</div>"
            "</body>"
            "</html>"
        )

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Report saved: {self.output_file}")


# Example Usage
if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import seaborn as sns

    # Sample dataset
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "x": np.random.randn(100),
            "y": np.random.randn(100),
            "category": np.random.choice(["A", "B"], size=100),
        }
    )

    report = PlotReportGenerator(
        title="Sample Report", output_file="sample_report.html"
    )

    # Generate a scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(x="x", y="y", hue="category", data=data, ax=ax)
    ax.set_title("Scatter Plot Example")
    report.add_plot("Scatter Plot", "This is an example scatter plot.", fig)

    # Generate a box plot
    fig, ax = plt.subplots()
    sns.boxplot(x="category", y="y", data=data, ax=ax)
    ax.set_title("Box Plot Example")
    report.add_plot("Box Plot", "This is an example box plot.", fig)

    # Generate and save the report
    report.generate_report()
