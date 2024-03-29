import tkinter as tk
from tkinter import ttk
import functions
import cfg


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def execute_submit(grammar_str, init_combo, rule_combo, rules, file_error):
    try:
        file_error.pack_forget()
        functions.submit(file_variable, grammar_str, init_combo, rule_combo, rules)
    except Exception as e:
        load_initial_page(e)


def execute_run():
    try:
        load_page2()
    except KeyError as k:
        load_initial_page(f"Invalid file {k}")
    except Exception as e:
        load_initial_page(e)


def load_initial_page(error_text=''):
    clear_widgets(page1_frame)
    clear_widgets(page2_frame)
    page1_frame.pack_forget()
    page2_frame.pack_forget()
    initial_page_frame.pack(fill=tk.BOTH, expand=1)

    # top_frame
    top_frame = tk.Frame(master=initial_page_frame)
    top_frame.pack(fill='both', expand=1)

    # list_frame
    list_frame = tk.Frame(master=top_frame)
    list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    listbox = tk.Listbox(master=list_frame, height=25, width=80)
    listbox.pack(padx=80, pady=10, anchor=tk.E)
    listbox.bind("<<ListboxSelect>>",
                 lambda event: functions.display_grammar(listbox.get(tk.ANCHOR), grammar_str, file_variable))

    for item in listbox_items:
        listbox.insert(tk.END, item)

    # btn_frame
    btn_frame = tk.Frame(master=top_frame)
    btn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=110)

    add_btn = tk.Button(master=btn_frame, text="Add", width=10,
                        command=lambda: functions.open_files(listbox, listbox_items))
    add_btn.pack(pady=20, anchor=tk.W)

    remove_btn = tk.Button(master=btn_frame, text="Remove", width=10,
                           command=lambda: functions.remove_file(listbox, listbox_items))
    remove_btn.pack(anchor=tk.W)

    edit_btn = tk.Button(master=btn_frame, text="Edit", width=10,
                         command=lambda: load_page1(file_error))
    edit_btn.pack(pady=20, anchor=tk.W)

    run_btn = tk.Button(master=btn_frame, text="Run", width=10,
                        command=lambda: execute_run())
    run_btn.pack(anchor=tk.W)

    file_error = tk.Label(master=list_frame, text=error_text, fg="red")
    file_error.pack()

    # grammar_frame
    grammar_frame = tk.LabelFrame(master=initial_page_frame, text="Grammar", height=400)
    grammar_frame.pack(fill=tk.X, side=tk.BOTTOM)
    grammar_frame.pack_propagate(0)

    grammar_str = tk.StringVar()
    grammar_l1 = tk.Label(master=grammar_frame, textvariable=grammar_str, justify='left')
    grammar_l1.pack()


def load_page1(file_error):
    clear_widgets(initial_page_frame)
    clear_widgets(page2_frame)
    initial_page_frame.pack_forget()
    page2_frame.pack_forget()
    page1_frame.pack(fill="both")

    # edit_frame
    edit_frame = tk.LabelFrame(master=page1_frame, text="Edit", height=165)
    edit_frame.pack(fill="x")
    edit_frame.pack_propagate(0)

    nt_frame = tk.Frame(master=edit_frame, height=155, width=edit_frame.winfo_width() / 2)
    nt_frame.pack(side='left', fill='x', expand=1, padx=100)

    back_btn = tk.Button(master=nt_frame, text='Back', width=7, command=lambda: load_initial_page())
    back_btn.pack(side=tk.LEFT)

    entry_str = tk.StringVar()
    entry = tk.Entry(master=nt_frame, textvariable=entry_str)
    entry.pack(pady=5)

    edit_f1 = tk.Frame(master=nt_frame)
    edit_f1.pack(pady=10)

    choice = tk.StringVar()
    choice.set("nonterminals")
    nt_radio = tk.Radiobutton(edit_f1, text="Non-Terminal", variable=choice, value="nonterminals")
    nt_radio.pack(side='left', padx=10)
    t_radio = tk.Radiobutton(edit_f1, text="Terminal", variable=choice, value="terminals")
    t_radio.pack(side='left', padx=10)

    edit_f2 = tk.Frame(master=nt_frame)
    edit_f2.pack(pady=10)

    add_btn = tk.Button(master=edit_f2, text="Add", width=7,
                        command=lambda: functions.add(file_variable.get(), choice.get(), entry_str.get(), grammar_str,
                                                      init_combo, rule_combo, rules, error_label))
    add_btn.pack(side="left", padx=10)

    remove_btn = tk.Button(master=edit_f2, text="Remove", width=7,
                           command=lambda: functions.remove(file_variable.get(), choice.get(), entry_str.get(),
                                                            grammar_str, init_combo, rule_combo, rules, error_label))
    remove_btn.pack(side="left", padx=10)

    rule_frame = tk.Frame(master=edit_frame, height=155, width=edit_frame.winfo_width() / 2)
    rule_frame.pack(side="left", fill='both', expand=1)

    rule_l1 = tk.Label(master=rule_frame, text="Initial Nonterminal:")
    rule_l1.grid(row=0, column=0, pady=10)

    init_val = tk.StringVar()
    nt_options = []
    init_combo = ttk.Combobox(master=rule_frame, textvariable=init_val, state="readonly", values=nt_options)
    init_combo.grid(row=0, column=1)

    rule_l2 = tk.Label(master=rule_frame, text="Rules:")
    rule_l2.grid(row=1, column=0, sticky='e', pady=12)

    rule_val = tk.StringVar()
    rule_options = []
    rule_combo = ttk.Combobox(master=rule_frame, textvariable=rule_val, state="readonly", values=rule_options)
    rule_combo.grid(row=1, column=1)
    rule_combo.bind("<<ComboboxSelected>>",
                    lambda event: functions.on_select_rule(file_variable.get(), rule_val, rules))

    rules = tk.StringVar()
    rule_entry = tk.Entry(master=rule_frame, width=30, textvariable=rules)
    rule_entry.grid(row=1, column=2, padx=10)

    save_btn = tk.Button(master=rule_frame, text="Modify", width=7,
                         command=lambda: functions.save_to_config(file_variable.get(), rule_val, rules, init_val,
                                                                  grammar_str, error_label))
    save_btn.grid(row=2, columnspan=3, pady=10)

    # transform frame
    transform_frame = tk.LabelFrame(master=page1_frame, text='Transform', height=155)
    transform_frame.pack(fill='x', expand=1)

    reduce_btn = tk.Button(master=transform_frame, text="Reduce", width=20,
                           command=lambda: functions.reduce(window, file_variable.get()))
    reduce_btn.grid(row=0, column=0, padx=10)

    epsilon_btn = tk.Button(master=transform_frame, text="Remove Epsilon Rules", width=20,
                            command=lambda: functions.remove_epsilon_rules(window, file_variable.get()))
    epsilon_btn.grid(row=1, column=0, pady=10)

    unit_btn = tk.Button(master=transform_frame, text="Remove Unit Rules", width=20,
                         command=lambda: functions.remove_unit_rules(window, file_variable.get()))
    unit_btn.grid(row=0, column=1)

    chomsky_btn = tk.Button(master=transform_frame, text="Chomsky Normal Form", width=20,
                            command=lambda: functions.chomsky_normal_form(window, file_variable.get()))
    chomsky_btn.grid(row=0, column=2, padx=20)

    greibach_btn = tk.Button(master=transform_frame, text="Greibach Normal Form", width=20,
                             command=lambda: functions.greibach_normal_form(window, file_variable.get()))
    greibach_btn.grid(row=1, column=2)

    first_btn = tk.Button(master=transform_frame, text="FIRST and FOLLOW", width=20,
                          command=lambda: functions.compute_first_and_follow(window, file_variable.get()))
    first_btn.grid(row=0, column=3, padx=10)

    error_label = tk.Label(master=page1_frame, fg="red")
    error_label.pack()

    # grammar_frame
    grammar_frame = tk.LabelFrame(master=page1_frame, text="Grammar", height=400)
    grammar_frame.pack(fill="x")
    # grammar_frame.pack_propagate(0)

    grammar_str = tk.StringVar()
    grammar_l1 = tk.Label(master=grammar_frame, textvariable=grammar_str, justify='left')
    grammar_l1.pack()

    execute_submit(grammar_str, init_combo, rule_combo, rules, file_error)


def load_page2():
    clear_widgets(initial_page_frame)
    clear_widgets(page1_frame)
    initial_page_frame.pack_forget()
    page1_frame.pack_forget()
    page2_frame.pack(fill="both", expand=1)

    grammar = cfg.main(file_variable.get())

    # top_frame
    top_frame = tk.Frame(master=page2_frame)
    top_frame.pack(fill='both', expand=1)

    # execute_frame
    execute_frame = tk.LabelFrame(master=top_frame, text="Execute")
    execute_frame.pack(side="left", fill='both', expand=1)
    execute_frame.pack_propagate(0)

    # button_frame
    button_frame = tk.Frame(master=execute_frame)
    button_frame.pack(fill='x')

    back_btn = tk.Button(master=button_frame, text="Back", command=lambda: load_initial_page())
    back_btn.pack(side='left', padx=10)

    redo_btn = tk.Button(master=button_frame, text="-->",
                         command=lambda: functions.redo(output_str, input_str, sentential_str, canvas, execute_e1,
                                                        grammar, execute_btn, undo_btn, redo_btn, sentential_canvas),
                         state="disabled")
    redo_btn.pack(side='right', padx=10)

    undo_btn = tk.Button(master=button_frame, text="<--",
                         command=lambda: functions.undo(output_str, input_str, sentential_str, canvas, execute_e1,
                                                        grammar, execute_btn, undo_btn, redo_btn, sentential_canvas),
                         state="disabled")
    undo_btn.pack(side='right')

    output_str = tk.StringVar()
    execute_l1 = tk.Label(master=execute_frame, textvariable=output_str, justify='left')
    execute_l1.pack()

    input_str = tk.StringVar()
    options = [grammar.initial_nonterminal]
    execute_e1 = ttk.Combobox(master=execute_frame, textvariable=input_str, values=options, state='readonly')
    execute_e1.current(0)
    execute_e1.pack()

    execute_btn = tk.Button(master=execute_frame, text="Execute",
                            command=lambda: functions.execute(output_str, input_str, sentential_str, canvas,
                                                              execute_e1, grammar, grammar.initial_nonterminal,
                                                              execute_btn, undo_btn, redo_btn, sentential_canvas, True,
                                                              True))
    execute_btn.pack(pady=10)

    # tree_frame
    tree_frame = tk.LabelFrame(master=top_frame, text="Derivation Tree")
    tree_frame.pack(side="left", fill='both', expand=1)
    tree_frame.pack_propagate(0)

    canvas = functions.create_scrollbars(tree_frame)

    # sentential_frame
    sentential_frame = tk.LabelFrame(master=page2_frame, text="Sentential Form", height=100)
    sentential_frame.pack(fill="x")
    sentential_frame.pack_propagate(0)

    sentential_sb = ttk.Scrollbar(master=sentential_frame, orient="horizontal")
    sentential_canvas = tk.Canvas(master=sentential_frame, xscrollcommand=sentential_sb.set)
    sentential_sb.config(command=sentential_canvas.xview)
    sentential_sb.pack(side="bottom", fill="x")
    sentential_canvas.pack(fill="both", expand=1)
    sentential_canvas.bind("<MouseWheel>",
                           lambda event: sentential_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units"))

    sentential_str = tk.StringVar()


# window
window = tk.Tk()
window.title("CFG")
window.geometry(f'{window.winfo_screenwidth() - 16}x{window.winfo_screenheight() - 80}+0+0')

# global variables
file_variable = tk.StringVar()
listbox_items = []

# initial_page
initial_page_frame = tk.Frame(master=window)

# page1
page1_frame = tk.Frame(master=window)

# page2
page2_frame = tk.Frame(master=window)

# load initial_page
load_initial_page()

# run
window.mainloop()
