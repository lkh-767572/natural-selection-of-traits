from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import json

def analyze(name, generations_list, num_list, avg_speed_list, avg_sense_list):

        def write_file(name, generations_list, num_list):
            data = {
                "Generations": generations_list,
                "NumberOfCreatures": num_list,
                "AverageSpeed": avg_speed_list,
                "AverageSense": avg_sense_list}
            with open(name, "w") as file:
                json.dump(data, file)

        def read_file(name):
            with open(name, "r") as file:
                data = json.loads(file.read())

            return data

        def visualize(data):
            x, y1, y2, y3 = data["Generations"], data["NumberOfCreatures"],\
            data["AverageSpeed"], data["AverageSense"]
            
            host = host_subplot(111, axes_class=AA.Axes)
            plt.subplots_adjust(right=0.75)

            par1 = host.twinx()
            par2 = host.twinx()

            offset = 60
            new_fixed_axis = par2.get_grid_helper().new_fixed_axis
            par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
                                                    offset=(offset, 0))

            par1.axis["right"].toggle(all=True)
            host.set_xlabel("Generations")
            host.set_ylabel("Number creatures")
            par1.set_ylabel("Average speed")
            par2.set_ylabel("Average sense")

            p1, = host.plot(x, y1, label="Number creatures")
            p2, = par1.plot(x, y2, label="Average speed")
            p3, = par2.plot(x, y3, label="Average sense")

            host.legend()

            host.axis["left"].label.set_color(p1.get_color())
            par1.axis["right"].label.set_color(p2.get_color())
            par2.axis["right"].label.set_color(p3.get_color())

            plt.draw()
            plt.show()

        write_file(name, generations_list, num_list)
        data = read_file(name)
        visualize(data)
