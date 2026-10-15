"""Display helpers. All source-derived transformations live in each case program."""
def frame(plt, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title, loc="left", pad=16)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    return fig, ax

def finish(fig, ax, kind="bar"):
    if kind != "pie":
        ax.grid(axis="y", alpha=.2)
    if kind == "bar":
        ax.tick_params(axis="x", labelrotation=35)
        for label in ax.get_xticklabels(): label.set_ha("right")
    fig.tight_layout()

def bar(plt, series, title, xlabel, ylabel):
    fig, ax = frame(plt, title, xlabel, ylabel)
    ax.bar([str(x) for x in series.index], series.to_numpy(), color="#1766a3")
    ax.set_ylim(bottom=0)
    finish(fig, ax)

def lines(plt, data, title, xlabel, ylabel):
    fig, ax = frame(plt, title, xlabel, ylabel)
    for name in data.columns:
        ax.plot(data.index, data[name], marker="o", label=str(name))
    ax.legend(title=data.columns.name)
    ax.set_ylim(bottom=0)
    finish(fig, ax, "line")

def pie(plt, series, title):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(series.to_numpy(), labels=[str(x) for x in series.index], autopct="%1.1f%%", startangle=90)
    ax.set_title(title, loc="left", pad=16)
    ax.set_aspect("equal")
    finish(fig, ax, "pie")

def stacked(plt, data, title, xlabel, ylabel):
    fig, ax = frame(plt, title, xlabel, ylabel)
    bottom = [0.] * len(data)
    for col in data.columns:
        values = data[col].to_numpy()
        ax.bar([str(x) for x in data.index], values, bottom=bottom, label=str(col))
        bottom = [b + v for b, v in zip(bottom, values)]
    ax.legend(title=data.columns.name, bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.set_ylim(bottom=0)
    finish(fig, ax)

def scatter(plt, data, x, y, title, xlabel, ylabel, group=None):
    fig, ax = frame(plt, title, xlabel, ylabel)
    if group:
        for key, sub in data.groupby(group, sort=True, dropna=True):
            ax.scatter(sub[x], sub[y], label=str(key), s=55)
        ax.legend(title=group)
    else:
        ax.scatter(data[x], data[y], s=55, color="#1766a3")
    finish(fig, ax, "scatter")
