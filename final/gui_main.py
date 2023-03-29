"""
This is what I want the gui to do:
Modes:

example mode - do everything. You can adjust the number of students and workload. We'll handle everything else.

irl mode 1 - you already have the matchups, assignemnts and judgements. We'll give you the verdict.

irl mode 2 - you already have the students. We'll give you the matchups and assignements. Next you'll give them to the real students and give us the judgements. We'll give you the verdict.

Task 4:
run the rankers
show results in a plot

Add user options
"""

# from gui.test import test
import dearpygui.dearpygui as dpg
import graphviz
from math import floor

from classroom import Classroom
from generate_tourney import TournamentGenerator
from graph_utils import fair_graph
from metrics import kendall_tau
from tourney_runner import run_iterative_tourney as run_iter

import distribute_papers as dp
import rankers as rk


# ------ GLOBAL STATE -------------------

RANKING_METHODS = {
    "Win Count": rk.win_count,
    "Borda": rk.copeland,
    "Weighted Borda": rk.weighted_borda,
    "Kemeny": rk.kemeny,
    "RBTL": rk.rbtl,
    "BTL": rk.btl,
}

inital_num_students = 5
classroom = Classroom(inital_num_students)
nc2 = (inital_num_students * (inital_num_students - 1)) / 2
pairs = None
assignments = None

def get_img_tag():
    num = 0
    while True:
        yield (f"img_{num - 1}", f"img_{num}")
        num += 1

tag_gen = get_img_tag()

# ---------GLOBAL STATE END --------------

dpg.create_context()

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


with dpg.window(
    label="Classroom Generation", autosize=True, pos=(0, 0), no_close=True
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

#---------------------
def gen_graph():
    if pairs == None:
        return 

    with dpg.window(
        on_close=lambda sender: dpg.delete_item(sender),
        label=f"Graph with {len(classroom)} students and {dpg.get_value('Edges Input')} matchups",
        autosize=True,
    ):
        dpg.add_text(
            "Loading...",
            tag="Graph Loading Text",
        )

        dot = graphviz.Graph("Matchups", engine="circo")
        dot.attr("node", shape="circle")
        for i in classroom.grades:
            dot.node(str(i), str(i))

        for a, b in pairs:
            dot.edge(str(a), str(b))

        dot.format = "png"
        dot.render(directory="./temp/")

        width, height, _, data = dpg.load_image("./temp/Matchups.gv.png")

        old_tag, new_tag = next(tag_gen)
        with dpg.texture_registry():
            dpg.delete_item(old_tag)
            dpg.add_static_texture(
                width=width, height=height, default_value=data, tag=new_tag
            )

        dpg.delete_item("Graph Loading Text")
        dpg.add_image(new_tag)


def save_matchups():
    global pairs
    n = len(classroom)
    e = dpg.get_value("Edges Input")
    pairs = fair_graph(n, e)

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

    if dpg.does_alias_exist("Assignment Table"):
        dpg.delete_item("Assignment Table")

    with dpg.table(tag="Assignment Table", parent="Assignment Table Group"):
        dpg.add_table_column(label="Grading Student")
        dpg.add_table_column(label="First Student")
        dpg.add_table_column(label="Second Student")
        for i, (a, b) in enumerate(pairs):
            with dpg.table_row(tag=f"Assignment Table Row {i}"):
                dpg.add_text("?")
                dpg.add_text(str(a))
                dpg.add_text(str(b))


def update_avg_workload(num_students, edges):
    avg_workload = edges / num_students
    dpg.set_value("Workload String", f"Average Workload of student: {avg_workload}")

with dpg.window(
    label="Matchup Generation", autosize=True, pos=(0, 300), no_close=True
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

        dpg.add_button(label="Save", callback=save_matchups)
        dpg.add_button(label="Generate graph - Preview", callback=gen_graph)

def assign_students():
    global assignments
    n = len(classroom)
    distributor = dp.PaperDistributor(n, pairs)

    # Create loading label 
    dpg.add_text(
        "Loading...",
        tag="Loading Text",
        parent="Assignment Control Group"
    )

    assignments = distributor.get_solution()

    # Delete loading label
    dpg.delete_item("Loading Text")

    if dpg.does_alias_exist("Assignment Table"):
        dpg.delete_item("Assignment Table")

    with dpg.table(tag="Assignment Table", parent="Assignment Table Group"):
        dpg.add_table_column(label="Grading Student")
        dpg.add_table_column(label="First Student")
        dpg.add_table_column(label="Second Student")

        id_num = 0
        for grader in assignments:
            for p1, p2 in assignments[grader]:
                with dpg.table_row(tag=f"Assignment Table Row {id_num}"):
                    dpg.add_text(str(grader))
                    dpg.add_text(str(p1))
                    dpg.add_text(str(p2))
                id_num += 1


with dpg.window(label="Assignment", autosize=True, pos=(100, 0), no_close=True) as tertiary_window:
    with dpg.group(horizontal=True, tag="Assignment Control Group"):
        dpg.add_button(label="Assign Students", callback=assign_students)
        dpg.add_text("Warning, this operation may take a while.")


    dpg.add_group(tag="Assignment Table Group")

#-----------------------

def run_rankers():
    if assignments == None or pairs == None:
        return
    
    tourney_gen = TournamentGenerator(classroom)
    acc = {}

    # Create loading label 
    dpg.add_text(
        "Loading...",
        tag="Loading Text Results",
        parent="Ranking Group"
    )
    
    # This is quite messy, however because iterative tournaments do not share 
    # the exact assignments, they must be ran first
    for method in RANKING_METHODS:
        if dpg.get_value(f"iter_{method}_checkbox"):
            ranking_func = RANKING_METHODS[method]
            n = len(classroom)
            rounds = floor(len(pairs)/n)
            results = run_iter(n, rounds, ranking_func, tourney_gen)
            acc[f"Iterative {method}"] = results
        print("done")

    tourney = tourney_gen.generate_tournament(assignments)
    for method in RANKING_METHODS:
        if dpg.get_value(f"{method}_checkbox"):
            ranking_func = RANKING_METHODS[method]
            results = ranking_func(tourney)
            acc[method] = results

        print("done")

    if dpg.does_alias_exist("Results Table"):
        dpg.delete_item("Results Table")


    # Sort by kendall tau
    real = classroom.get_true_ranking()
    acc = dict(sorted(acc.items(), key=lambda item: kendall_tau(real, item[1])))

    with dpg.table(
            tag="Results Table",
            parent="Ranking Group",
            policy=dpg.mvTable_SizingStretchProp
    ):
        dpg.add_table_column(label="Method")
        dpg.add_table_column(label="Ranking")
        dpg.add_table_column(label="Kendall Tau Score")

        for method in acc:
            with dpg.table_row(tag=f"{method}_row"):
                res = acc[method]
                kt = kendall_tau(real, res)
                dpg.add_text(method)
                dpg.add_text(str(res))
                dpg.add_text(str(kt))

    dpg.delete_item("Loading Text Results")

            
            
        
with dpg.window(label="Ranking", autosize=True, pos=(100,100), no_close=True) as quaternary_window:
    with dpg.group(tag="Ranking Group"):
        for i, method in enumerate(RANKING_METHODS):
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label=method,
                    tag=f"{method}_checkbox",
                    default_value=True
                )

                dpg.add_checkbox(
                    label=f"Iterative {method}",
                    tag=f"iter_{method}_checkbox",
                    default_value=False
                )


    dpg.add_button(
        label="Run ranking methods",
        callback=run_rankers
    )

#-----------------------

dpg.create_viewport(title="Tournament Ranking")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
