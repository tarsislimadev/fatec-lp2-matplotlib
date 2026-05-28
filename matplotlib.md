# Matplotlib — Quick Reference

Matplotlib is a comprehensive Python 2D plotting library that produces publication-quality figures in a variety of formats and interactive environments (scripts, Jupyter notebooks, web application servers, and graphical user interfaces).

## Key Concepts
- Figure: the overall window or page that contains one or more plots.
- Axes: a single plot area inside a Figure; contains the data, ticks, labels, and legend.
- Artist: everything you see on the figure (lines, text, patches). Most high-level plotting functions create Artists.
- pyplot: a stateful, MATLAB-like interface (`matplotlib.pyplot`) for quick plotting.
- Object-oriented (OO) API: recommended for complex figures — you explicitly create `Figure` and `Axes` objects and call methods on them.

## Installation

Install via pip (recommended):

```
pip install matplotlib
```

If you use conda:

```
conda install matplotlib
```

## Simple Examples

Using `pyplot` (quick):

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
 y = [10, 20, 25, 30]

plt.plot(x, y, label='Line')
plt.scatter(x, y, color='red')
plt.title('Simple plot')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
```

Using the object-oriented API (recommended):

```python
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(x, y, '-o', label='Series')
ax.set_title('OO API example')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
fig.tight_layout()
fig.savefig('figure.png', dpi=300)
```

## Common Plot Types
- Line plots: `plot()`
- Scatter plots: `scatter()`
- Bar charts: `bar()` / `barh()`
- Histograms: `hist()`
- Boxplots: `boxplot()`
- Heatmaps / images: `imshow()`
- Pie charts: `pie()`

## Customization and Styles
- Use `rcParams` or `matplotlib.style.use()` to change default styles (e.g., `plt.style.use('seaborn')`).
- Title, labels, ticks, and legends are set via Axes methods: `set_title`, `set_xlabel`, `set_xticks`, `legend()`.
- Annotate with `ax.annotate()` and add text with `ax.text()`.

## Integration
- Pandas: DataFrame/Series have `.plot()` which uses Matplotlib under the hood.
- Seaborn: higher-level statistical plotting built on Matplotlib; use for nicer defaults and statistical plots.
- Interactive environments: works well in Jupyter with `%matplotlib inline` or `%matplotlib notebook`.

## Saving Figures
- `fig.savefig('path.png', dpi=300, bbox_inches='tight')` supports PNG, PDF, SVG, EPS.

## Performance & Tips
- For many points, prefer `scatter()` with small markers or use downsampling.
- Reuse artists (update data) when animating rather than re-creating them for performance.
- Use `constrained_layout` or `tight_layout()` to avoid overlapping labels.

## Common Pitfalls
- Mixing `pyplot` stateful calls and OO API can lead to confusion; prefer one style per script.
- Always call `plt.close(fig)` in scripts that generate many figures to free memory.

## Where to Learn More
- Official docs: https://matplotlib.org/
- Tutorials and examples: https://matplotlib.org/stable/tutorials/index.html
- Gallery: https://matplotlib.org/stable/gallery/index.html

---

This file gives a compact overview and examples to get started. For deep dives, consult the official documentation and gallery.
