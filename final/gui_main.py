"""
This is what I want the gui to do:

Modes:

example mode - do everything. You can adjust the number of students and workload. We'll handle everything else.

irl mode 1 - you already have the matchups, assignemnts and judgements. We'll give you the verdict.

irl mode 2 - you already have the students. We'll give you the matchups and assignements. Next you'll give them to the real students and give us the judgements. We'll give you the verdict.

First things first, let's get a UI to input students.

Task 1:
gui to :
input a number.
after inputting a number, generate a classroom of that size
show results in a table
show a gui next to it, allowing you to edit values

Task 2:
We have all the students
now we'll let you input the number of matchups you want each student to mark
next we'll make a massive table of who marks who
and give you a visualisation

Task 3:
Run the mip 
print the assignments in a table
preview the graph 

Task 4:
run the rankers
show results in a plot

Add user options

"""

# from gui.test import test
import dearpygui.dearpygui as dpg
import graphviz

from classroom import Classroom
from generate_tourney import TournamentGenerator
from graph_utils import fair_graph
import distribute_papers as dp

# ------ GLOBAL STATE -------------------

inital_num_students = 5
classroom = Classroom(inital_num_students)
nc2 = (inital_num_students * (inital_num_students - 1)) / 2
pairs = None


def get_img_tag():
    num = 0
    while True:
        yield (f"img_{num - 1}", f"img_{num}")
        num += 1


tag_gen = get_img_tag()

# ---------GLOBAL STATE END --------------


# -------------------- CALLBACKS -------------------------
def set_classroom(_, app_data):
    old_size = len(classroom)
    new_size = app_data

    if new_size > old_size:
        num_to_add = new_size - old_size

        for i in range(num_to_add):
            classroom.add_student()
            row_id = old_size + i
            with dpg.table_row(
                parent="Classroom_Table", tag=f"Classroom_Table_Row{row_id}"
            ):
                dpg.add_text(str(old_size + i))
                dpg.add_text(str(classroom.grades[old_size + i]))

    elif new_size < old_size:
        num_to_del = old_size - new_size
        for i in range(num_to_del):
            classroom.del_student()
            row_id = (old_size - i) - 1
            dpg.delete_item(f"Classroom_Table_Row{row_id}")

    # When you increase or decrease the classroom size,
    # we should also update avg workload
    edges = dpg.get_value("Edges Input")
    update_avg_workload(new_size, edges)

    ub = new_size * (new_size - 1) / 2
    lb = len(classroom)
    clamp = lambda v: max(min(ub, v), lb)
    dpg.set_value("Edges Input", clamp(edges))
    dpg.configure_item("Edges Input", max_value=ub, min_value=lb)


def update_avg_workload(num_students, edges):
    avg_workload = num_students / edges
    dpg.set_value("Workload String", f"Average Workload of student: {avg_workload}")


def gen_graph():
    global pairs
    n = len(classroom)
    e = dpg.get_value("Edges Input")
    pairs = fair_graph(n, e)

    dot = graphviz.Graph("Matchups", engine="circo")
    dot.attr("node", shape="circle")
    for i in classroom.grades:
        dot.node(str(i), str(i))

    for a, b in pairs:
        dot.edge(str(a), str(b))

    dot.format = "png"
    dot.render(directory="./temp/")

    width, height, _, data = dpg.load_image("./temp/Matchups.gv.png")

    with dpg.window(
        on_close=lambda sender: dpg.delete_item(sender),
        label=f"Graph with {len(classroom)} students and {dpg.get_value('Edges Input')} matchups",
        autosize=True,
    ):
        old_tag, new_tag = next(tag_gen)
        with dpg.texture_registry():
            dpg.delete_item(old_tag)
            dpg.add_static_texture(
                width=width, height=height, default_value=data, tag=new_tag
            )
        dpg.add_image(new_tag)

    # Table Stuff
    if dpg.does_alias_exist("Edge Table"):
        dpg.delete_item("Edge Table")

    with dpg.table(tag="Edge Table", parent="Matchup Group"):
        dpg.add_table_column(label="First Student")
        dpg.add_table_column(label="Second Student")
        for i, (a, b) in enumerate(pairs):
            with dpg.table_row(tag=f"Edge Table Row {i}"):
                dpg.add_text(str(a))
                dpg.add_text(str(b))


# ----------------CALLBACKS END ------------------------

dpg.create_context()

with dpg.window(
    label="Classroom Generation", autosize=True, pos=(0, 0)
) as primary_window:
    dpg.add_input_int(
        label="Number of Students",
        default_value=inital_num_students,
        callback=set_classroom,
        min_value=1,
        min_clamped=True,
        on_enter=True,
    )

    with dpg.table(tag="Classroom_Table"):
        dpg.add_table_column(label="Student ID")
        dpg.add_table_column(label="Test Score")
        for i in range(inital_num_students):
            with dpg.table_row(tag=f"Classroom_Table_Row{i}"):
                dpg.add_text(str(i))
                dpg.add_text(str(classroom.grades[i]))


with dpg.window(
    label="Matchup Generation", autosize=True, pos=(0, 300)
) as secondary_window:
    with dpg.group(tag="Matchup Group"):
        dpg.add_input_int(
            label="Number of Matchups",
            tag="Edges Input",
            default_value=inital_num_students,
            callback=lambda _, app_data: update_avg_workload(len(classroom), app_data),
            min_value=1,
            max_value=int(nc2),
            min_clamped=True,
            max_clamped=True,
            on_enter=True,
        )

        dpg.add_text(
            default_value=f"Average Workload of student: 1", tag="Workload String"
        )

        dpg.add_button(label="Generate graph - Preview", callback=gen_graph)

# with dpg.window(label="Assignment", autosize=True, pos=(100, 0)) as tertiary_window:
#     dpg.add


dpg.create_viewport(title="Tournament Ranking")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()