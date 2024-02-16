from tkinter import filedialog
from cfg import CFG, main, Stack
import tkinter as tk


def update_label(label, text):
    label.set(text)


def update_options(combobox, options):
    combobox['values'] = options
    combobox.current(0)


def open_file(file_variable):
    filename = filedialog.askopenfilename(
        initialdir="/Users/ruube/PycharmProjects/Thesis",
        title="Select A File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    file_variable.set(filename)


def read_file(file):
    with open(file, 'r') as f:
        text = f.read()
        return text


def submit(file, grammar_str, init_combo, rule_combo, rules):
    text = read_file(file)
    grammar_str.set(text)

    grammar = CFG().read_config(file)
    init_combo['values'] = grammar['input']['nonterminals'].split(',')
    init_combo.current(0)

    rule_combo['values'] = grammar['input']['nonterminals'].split(',')
    rule_combo.current(0)
    rules.set(grammar['rules'][rule_combo['values'][0]])


def on_pressing_right(transform_str, stack_transformation, index):
    if index.get() < len(stack_transformation.data) - 1:
        index.set(index.get() + 1)
        text = transform_str.get()
        text += f"\n{stack_transformation.data[index.get()]}"
        update_label(transform_str, text)


def on_pressing_left(transform_str, stack_transformation, index):
    pass
    # if index.get() > 0:
    #     index.set(index.get() - 1)


def create_popup_window(window, stack_transformation):
    popup_window = tk.Toplevel(window)
    popup_window.title("View Transformation")
    # popup_window.geometry("250x150")
    popup_window.focus()

    grammar_frame = tk.LabelFrame(master=popup_window, text="Grammar")
    grammar_frame.pack(side="left", fill="both", expand=1)
    grammar_str = tk.StringVar()
    grammar_label = tk.Label(master=grammar_frame, textvariable=grammar_str, justify="left")
    grammar_label.pack()

    transform_frame = tk.LabelFrame(master=popup_window, text="Transformation Steps")
    transform_frame.pack(side="left", fill="both", expand=1)
    transform_str = tk.StringVar()
    transform_label = tk.Label(master=transform_frame, textvariable=transform_str, justify="left")
    transform_label.pack()

    explain_frame = tk.LabelFrame(master=popup_window, text="Explanation")
    explain_frame.pack(side="left", fill="both", expand=1)
    explain_str = tk.StringVar()
    explain_label = tk.Label(master=explain_frame, textvariable=explain_str, justify="left")
    explain_label.pack()

    index = tk.IntVar()
    index.set(0)

    update_label(transform_str, stack_transformation.data[index.get()])

    popup_window.bind("<Right>", lambda event: on_pressing_right(transform_str, stack_transformation, index))
    popup_window.bind("<Left>", lambda event: on_pressing_left(transform_str, stack_transformation, index))


def update_rules(config, grammar, file_variable, set_transformation, stack_transformation):
    not_set_t = set(grammar.nonterminals) - set_transformation
    for not_t in not_set_t:
        CFG().remove_value(config, 'nonterminals', not_t, file_variable)

    text = '\n'
    for nt in config['rules']:
        for rule in config['rules'][nt].split():
            text += f"{nt} = {rule}\n"

    stack_transformation.push(text)


def reduce(window, file_variable):
    stack_transformation = Stack()
    grammar = main(file_variable)
    config = CFG().read_config(file_variable)
    set_t = set()
    grammar.reduce_phase1(config, grammar, stack_transformation, set_t, '\u2080')

    update_rules(config, grammar, file_variable, set_t, stack_transformation)

    set_d = set()
    set_d.add(grammar.initial_nonterminal)
    stack_transformation.push(f"D\u2080 = {set_d}")
    grammar.reduce_phase2(config, grammar, stack_transformation, set_t, set_d, '\u2081')

    update_rules(config, grammar, file_variable, set_d, stack_transformation)

    create_popup_window(window, stack_transformation)


def save_to_config(file, rule_val, rules, init_val, grammar_str, error_label):
    grammar = CFG().read_config(file)
    grammar.set('input', 'initial_nonterminal', init_val.get())

    substrings = grammar['input']['nonterminals'].split(',') + grammar['input']['terminals'].split(',') + ['epsilon']
    substrings = sorted(substrings, key=lambda x: not x.startswith('<'))
    new_rule = []
    for rule in rules.get().split(','):
        if CFG().check_rule(rule.strip(), substrings):
            new_rule.append(rule.strip())
            error_label.config(text="")
        else:
            error_label.config(text=f"{rule} is not a valid rule")
            return

    new_rules = [item for item in new_rule if item != '']
    grammar.set('rules', rule_val.get(), ','.join(new_rules))
    CFG().write_to_config(grammar, file)
    text = read_file(file)
    grammar_str.set(text)


def on_select_rule(file, rule_val, rules):
    grammar = CFG().read_config(file)
    for i in grammar['rules']:
        if i == rule_val.get():
            rules.set(grammar['rules'][i])


def add(file, val_type, val, grammar_str, init_combo, rule_combo, rules, error_label):
    config = CFG().read_config(file)
    error_text = CFG().add_value(config, val_type, val, file)

    if error_text is None:
        submit(file, grammar_str, init_combo, rule_combo, rules)
        error_label.config(text="")
    else:
        error_label.config(text=error_text)


def remove(file, val_type, val, grammar_str, init_combo, rule_combo, rules, error_label):
    config = CFG().read_config(file)
    error_text = CFG().remove_value(config, val_type, val, file)

    if error_text is None:
        submit(file, grammar_str, init_combo, rule_combo, rules)
        error_label.config(text="")
    else:
        error_label.config(text=error_text)


def update_sentential_scrollregion(sentential_canvas, sentential_str):
    sentential_canvas.delete("all")
    width = sentential_canvas.winfo_width() / 2
    sentential_canvas.create_text(width, 30, text=sentential_str.get())
    sentential_canvas.config(scrollregion=sentential_canvas.bbox("all"))


def calculate_subtree_width(tree, x_space):
    if not tree.children:
        return x_space
    return sum(calculate_subtree_width(child, x_space) for child in tree.children) + (len(tree.children) - 1) * x_space


def calculate_positions(canvas, tree, x, y, x_space, y_space, level=0, positions=None, nonterminal=None):
    if positions is None:
        positions = {}

    if tree.data == '':
        text = "\u03B5"
    else:
        text = tree.data

    width = calculate_subtree_width(tree, x_space)
    x_offset = -width / 2

    node_x = x
    node_y = y + y_space * level
    positions[id(tree)] = (node_x, node_y)

    if nonterminal == text and tree.children == []:
        canvas.create_text(node_x, node_y, text=text, tags="occ")
    else:
        canvas.create_text(node_x, node_y, text=text, tags="node")

    if tree.children:
        for child in tree.children:
            child_width = calculate_subtree_width(child, x_space)
            calculate_positions(canvas, child, x + x_offset + child_width / 2, y + y_space, x_space, y_space, level + 1,
                                positions, nonterminal)
            draw_lines_between_nodes(canvas, positions[id(tree)], positions[id(child)])
            x_offset += child_width + x_space


def draw_tree(canvas, tree, x=400, y=50, x_space=100, y_space=120, nonterminal=None):
    calculate_positions(canvas, tree, x, y, x_space, y_space, level=0, positions=None, nonterminal=nonterminal)

    occ = 0
    for widget in canvas.find_all():
        tags = canvas.gettags(widget)
        if "node" in tags:
            x, y, x1, y1 = canvas.bbox(widget)
            canvas.create_oval(x - 10, y - 8, x1 + 10, y1 + 8, fill="lightblue", tags='oval')
            canvas.tag_raise('node')
            canvas.config(scrollregion=canvas.bbox("all"))
        if "occ" in tags:
            occ += 1
            x, y, x1, y1 = canvas.bbox(widget)
            canvas.create_oval(x - 10, y - 8, x1 + 10, y1 + 8, fill="pink", tags='oval')
            canvas.create_text(x1 - 4, y1 + 20, text=occ, tags="occ")
            canvas.tag_raise('occ')
            canvas.config(scrollregion=canvas.bbox("all"))


def draw_lines_between_nodes(canvas, parent_pos, child_pos):
    parent_x, parent_y = parent_pos
    child_x, child_y = child_pos
    canvas.create_line(parent_x, parent_y, child_x, child_y - 15, arrow=tk.LAST)


def undo(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, undo_btn, redo_btn, sentential_canvas):
    redo_btn.config(state="normal")
    execute_btn.config(state='normal')
    execute_e1.config(state='readonly')

    sentence, ldata = grammar.stack.undo('S', grammar.nonterminals)
    tree = grammar.stack_tree.undo('T', grammar.nonterminals)
    if ldata == grammar.stack.data[0]:
        undo_btn.config(state="disabled")
        update_label(sentential_str, grammar.stack.data[0])
        update_sentential_scrollregion(sentential_canvas, sentential_str)
        x = 400
        y = 50
        canvas.delete("all")
        canvas.create_oval(x, y, x + 30, y + 30, fill="lightblue")
        canvas.create_text(x + 15, y + 15, text=grammar.stack.data[0])
        execute(output_str, input_str, sentential_str, canvas, execute_e1, grammar, ldata, execute_btn, undo_btn,
                redo_btn, sentential_canvas, tree)
    else:
        update_label(sentential_str, sentence)
        update_sentential_scrollregion(sentential_canvas, sentential_str)
        canvas.delete("all")
        draw_tree(canvas, tree, 400, 50, 50, 60)
        get_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, ldata,
                        undo_btn, redo_btn, sentential_canvas, tree)


def redo(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, undo_btn, redo_btn, sentential_canvas):
    undo_btn.config(state="normal")

    sentence, ldata = grammar.stack.redo('S', grammar.nonterminals)
    tree = grammar.stack_tree.redo('T', grammar.nonterminals)
    if ldata == grammar.stack.data[-1]:
        redo_btn.config(state="disabled")
    update_label(sentential_str, sentence)
    update_sentential_scrollregion(sentential_canvas, sentential_str)
    canvas.delete("all")
    draw_tree(canvas, tree, 400, 50, 50, 60)
    nt = [elem for elem in grammar.nonterminals if elem in ldata.split(" ")]
    if nt:
        get_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, ldata, undo_btn,
                    redo_btn, sentential_canvas)
    else:
        execute_btn.config(state='disabled')
        execute_e1.config(state='disabled')
        update_label(input_str, '')
        update_label(output_str, f'Result: {ldata}')


def choose_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, undo_btn,
                       redo_btn, sentential_canvas, undo_tree):
    non_terminal = input_str.get()
    execute(output_str, input_str, sentential_str, canvas, execute_e1, grammar, non_terminal, execute_btn, undo_btn,
            redo_btn, sentential_canvas, undo_tree)


def get_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, ldata, undo_btn,
                    redo_btn, sentential_canvas, undo_tree=None):
    val = [elem for elem in grammar.nonterminals if elem in ldata.split(" ")]
    if val:
        if len(val) == 1:
            non_terminal = val[0]
            execute(output_str, input_str, sentential_str, canvas, execute_e1, grammar, non_terminal, execute_btn,
                    undo_btn, redo_btn, sentential_canvas, undo_tree)
        else:
            update_label(output_str,
                         f"\nLast expansion : {ldata} \nChoose the next non terminal for expansion: \n ")
            update_options(execute_e1, val)
            execute_btn.config(
                command=lambda: choose_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar,
                                                   execute_btn, undo_btn, redo_btn, sentential_canvas, undo_tree))


def process_data(output_str, input_str, sentential_str, canvas, execute_e1, grammar, initial_nonterminal, execute_btn,
                 selected_expansion, undo_btn, redo_btn, sentential_canvas):
    undo_btn.config(state="normal")
    redo_btn.config(state="disabled")

    if grammar.stack.current().count(initial_nonterminal) > 1:
        position = int(input_str.get())
    else:
        position = 1

    if "\u03B5" in selected_expansion:
        selected_expansion[0] = ''

    ldata = grammar.replacer(grammar.stack.current(), initial_nonterminal, " ".join(selected_expansion), position)
    ldata = " ".join(ldata.split())
    grammar.stack.push(ldata)
    sentence = grammar.create_sentential_form(grammar.stack.data, initial_nonterminal, "".join(selected_expansion),
                                              position)
    update_label(sentential_str, sentence)
    update_sentential_scrollregion(sentential_canvas, sentential_str)
    grammar.stack_tree.push({initial_nonterminal: selected_expansion, "position": position})
    tree = grammar.build_tree(grammar.stack_tree, grammar.nonterminals)
    canvas.delete("all")
    draw_tree(canvas, tree, 400, 50, 50, 60)
    nt = [elem for elem in grammar.nonterminals if elem in ldata.split(" ")]
    if nt:
        get_nonterminal(output_str, input_str, sentential_str, canvas, execute_e1, grammar, execute_btn, ldata,
                        undo_btn, redo_btn, sentential_canvas)
    else:
        execute_btn.config(state='disabled')
        execute_e1.config(state='disabled')
        update_label(input_str, '')
        update_label(output_str, f'Result: {ldata}')


def get_occurrence(output_str, input_str, sentential_str, canvas, execute_e1, grammar, initial_nonterminal, execute_btn,
                   undo_btn, redo_btn, sentential_canvas, undo_tree):
    selected_expansion = input_str.get().split()
    if grammar.stack.current().count(initial_nonterminal) > 1:
        update_label(output_str,
                     f"Enter the occurrence of '{initial_nonterminal}' to expand in '{grammar.stack.current()}' : \n ")
        occurrences = []
        for i in range(1, grammar.stack.current().count(initial_nonterminal) + 1):
            occurrences.append(i)
        update_options(execute_e1, occurrences)

        if undo_tree is None:
            tree = grammar.build_tree(grammar.stack_tree, grammar.nonterminals)
            canvas.delete("all")
            draw_tree(canvas, tree, 400, 50, 50, 60, initial_nonterminal)
        else:
            canvas.delete("all")
            draw_tree(canvas, undo_tree, 400, 50, 50, 60, initial_nonterminal)

        execute_btn.config(
            command=lambda: process_data(output_str, input_str, sentential_str, canvas, execute_e1, grammar,
                                         initial_nonterminal, execute_btn, selected_expansion, undo_btn, redo_btn, sentential_canvas))
    else:
        process_data(output_str, input_str, sentential_str, canvas, execute_e1, grammar, initial_nonterminal,
                     execute_btn, selected_expansion, undo_btn, redo_btn, sentential_canvas)


def execute(output_str, input_str, sentential_str, canvas, execute_e1, grammar, initial_nonterminal, execute_btn,
            undo_btn, redo_btn, sentential_canvas, undo_tree, init_val=False):
    if initial_nonterminal not in grammar.rules:
        return initial_nonterminal

    if init_val:
        x = 400
        y = 50
        update_label(sentential_str, initial_nonterminal)
        update_sentential_scrollregion(sentential_canvas, sentential_str)
        canvas.create_oval(x, y, x + 30, y + 30, fill="lightblue")
        canvas.create_text(x + 15, y + 15, text=initial_nonterminal)

    update_label(output_str, f"Choose the next expansion for '{initial_nonterminal}':")
    options = []
    for i, option in enumerate(grammar.rules[initial_nonterminal], 1):
        if option[0] == '':
            options.append("\u03B5")
        else:
            options.append(' '.join(option))

    update_options(execute_e1, options)

    execute_btn.config(
        command=lambda: get_occurrence(output_str, input_str, sentential_str, canvas, execute_e1, grammar,
                                       initial_nonterminal, execute_btn, undo_btn, redo_btn, sentential_canvas, undo_tree))
