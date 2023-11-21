import tkinter as tk
import functions


def clear_widgets(frame):
    # select all frame widgets and delete them
    for widget in frame.winfo_children():
        widget.destroy()


def load_page1():
    clear_widgets(page2_frame)
    page2_frame.pack_forget()
    page1_frame.pack(fill="both")

    # select_frame
    select_frame = tk.LabelFrame(master=page1_frame, text="Select A File", height=100, width=500)
    select_frame.pack(fill="x")
    select_frame.pack_propagate(0)

    select_f1 = tk.Frame(master=select_frame)
    select_f1.pack(pady=5)

    select_l1 = tk.Label(master=select_f1, text="File:")
    select_l1.pack(side="left")

    file_variable = tk.StringVar()
    file_textbox = tk.Entry(master=select_f1, textvariable=file_variable, width=100)
    file_textbox.pack(side="left")

    browse_btn = tk.Button(master=select_f1, text="Browse", command=lambda: functions.open_file(file_variable))
    browse_btn.pack(side="left", padx=5)

    select_f2 = tk.Frame(master=select_frame)
    select_f2.pack()

    submit_btn = tk.Button(master=select_f2, text="Submit",
                           command=lambda: functions.submit(file_variable.get(), grammar_str))
    submit_btn.pack(side="left", padx=5)
    # submit_btn.config(state="disabled")

    run_btn = tk.Button(master=select_f2, text="Run", width=5, command=lambda: load_page2())
    run_btn.pack(side="left", padx=10)
    # run_btn.config(state="disabled")

    # edit_frame
    edit_frame = tk.LabelFrame(master=page1_frame, text="Edit", height=155, width=500)
    edit_frame.pack(fill="x")
    edit_frame.pack_propagate(0)

    entry_str = tk.StringVar()
    entry = tk.Entry(master=edit_frame, textvariable=entry_str)
    entry.pack(pady=10)

    edit_f1 = tk.Frame(master=edit_frame)
    edit_f1.pack(pady=10)

    choice = tk.StringVar()
    choice.set("nonterminals")
    nt_radio = tk.Radiobutton(edit_f1, text="Non-Terminal", variable=choice, value="nonterminals")
    nt_radio.pack(side='left', padx=10)
    t_radio = tk.Radiobutton(edit_f1, text="Terminal", variable=choice, value="terminals")
    t_radio.pack(side='left', padx=10)
    rule_radio = tk.Radiobutton(edit_f1, text="Rule", variable=choice, value="rules")
    rule_radio.pack(side='left', padx=10)

    edit_f2 = tk.Frame(master=edit_frame)
    edit_f2.pack(pady=10)

    add_btn = tk.Button(master=edit_f2, text="Add", width=7,
                        command=lambda: functions.add(file_variable.get(), choice.get(), entry_str.get(), grammar_str))
    add_btn.pack(side="left", padx=10)

    remove_btn = tk.Button(master=edit_f2, text="Remove",
                           command=lambda: functions.remove(file_variable.get(), choice.get(), entry_str.get(),
                                                            grammar_str))
    remove_btn.pack(side="left", padx=10)

    # grammar_frame
    grammar_frame = tk.LabelFrame(master=page1_frame, text="Grammar", height=400)
    grammar_frame.pack(fill="x")
    # grammar_frame.pack_propagate(0)

    grammar_str = tk.StringVar()
    grammar_l1 = tk.Label(master=grammar_frame, textvariable=grammar_str)
    grammar_l1.pack()


def load_page2():
    clear_widgets(page1_frame)
    page1_frame.pack_forget()
    page2_frame.pack(fill="both", expand=1)

    # top_frame
    top_frame = tk.Frame(master=page2_frame, height=500, width=1300)
    top_frame.pack()

    # execute_frame
    execute_frame = tk.LabelFrame(master=top_frame, text="Execute", height=500, width=620)
    execute_frame.pack(side="left")
    execute_frame.pack_propagate(0)

    back_btn = tk.Button(master=execute_frame, text="Back", command=lambda: load_page1())
    back_btn.pack()

    undo_btn = tk.Button(master=execute_frame, text="<--")
    undo_btn.pack()

    redo_btn = tk.Button(master=execute_frame, text="-->")
    redo_btn.pack()

    output_str = tk.StringVar()
    execute_l1 = tk.Label(master=execute_frame, textvariable=output_str)
    execute_l1.pack()

    input_str = tk.StringVar()
    execute_e1 = tk.Entry(master=execute_frame, textvariable=input_str)
    execute_e1.pack()

    execute_btn = tk.Button(master=execute_frame, text="Execute")
    execute_btn.pack()

    # tree_frame
    tree_frame = tk.LabelFrame(master=top_frame, text="Derivation Tree", height=500, width=650)
    tree_frame.pack(side="left")

    tree_str = tk.StringVar()
    tree_l1 = tk.Label(master=tree_frame, textvariable=tree_str)
    tree_l1.pack

    # sentential_frame
    sentential_frame = tk.LabelFrame(master=page2_frame, text="Sentential Form", height=150, width=900)
    sentential_frame.pack(fill="x")

    sentential_str = tk.StringVar()
    sentential_l1 = tk.Label(master=sentential_frame, textvariable=sentential_str)
    sentential_l1.pack


# window
window = tk.Tk()
window.title("CFG")
# window.eval("tk::PlaceWindow . center")
window.geometry(f'{window.winfo_screenwidth() - 16}x{window.winfo_screenheight() - 80}+0+0')

# page1
page1_frame = tk.Frame(master=window)
page1_frame.pack(fill="both")

# page2
page2_frame = tk.Frame(master=window)

# load page1
load_page1()

# run
window.mainloop()
