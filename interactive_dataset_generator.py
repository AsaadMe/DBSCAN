import matplotlib.pyplot as plt


fig, ax = plt.subplots()
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])

def onclick(event):
    print(f"xdata={event.xdata}, ydata={event.ydata}")
    plt.plot(event.xdata, event.ydata, 'o')
    with open("data.txt", "a") as dataset:
        dataset.write(f"{event.xdata},{event.ydata}\n")
    event.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()