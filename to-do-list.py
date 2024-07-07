"""
TodoApp - A To-Do List Application

This application allows users to manage tasks with different priorities and mark them as completed or delete them.

Dependencies:
    - customtkinter: A custom themed extension of tkinter for enhanced GUI development.
    - PIL.Image, PIL.ImageTk: Required for handling and displaying images in the GUI.

Classes:
    - TaskCard: Represents a task card with options to mark completion and delete.
    - TodoApp: Main application class managing task creation, display, and interaction.

Usage:
    - Run this script to launch the To-Do List application.
    - Enter task names, select priority, and press 'Add Task' to create new tasks.
    - Tasks can be marked as completed by clicking the check button or deleted using the delete button.

"""

import customtkinter as ctk
from tkinter import StringVar, messagebox, Radiobutton
from PIL import Image, ImageTk

class TaskCard:
    """
    Represents a task card in the To-Do List application.

    Attributes:
        app (TodoApp): The parent application instance.
        task_name (str): The name of the task.
        is_completed (bool): Flag indicating if the task is completed.
        priority (str): Priority level of the task ("low", "medium", "high").
        card_frame (customtkinter.CTkFrame): Frame containing task details and controls.
        task_label (customtkinter.CTkLabel): Label displaying the task name.
        delete_button (customtkinter.CTkButton): Button to delete the task.
        check_button (customtkinter.CTkButton): Button to mark task completion.
    """

    def __init__(self, master, task_name, app, priority="low"):
        """
        Initializes a TaskCard instance.

        Args:
            master (tk.Tk or tk.Frame): Parent widget to place the task card.
            task_name (str): Name of the task.
            app (TodoApp): Parent TodoApp instance.
            priority (str, optional): Priority level of the task ("low", "medium", "high"). Default is "low".
        """
        self.app = app
        self.task_name = task_name
        self.is_completed = False
        self.priority = priority

        self.card_frame = ctk.CTkFrame(master, fg_color="#bdbdbd", border_color='#12d8db', border_width=2.2, corner_radius=10, width=20)
        self.card_frame.pack(padx=10, pady=5, fill='x')

        self.create_task_name()
        self.create_priority_bar()

    def create_task_name(self):
        """Creates and packs the task name label."""
        task_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        task_frame.pack(padx=10, pady=(10, 0), fill='x')

        self.task_label = ctk.CTkLabel(task_frame, text=self.task_name, font=('Arial', 20), text_color='black')
        self.task_label.pack(side='left', anchor='w', fill='x')

    def create_priority_bar(self):
        """Creates and packs the priority indicator bar and control buttons."""
        priority_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        priority_frame.pack(padx=10, pady=(5, 10), fill='x')

        colors = {
            "low": ["#167d21", "transparent", "transparent"],
            "medium": ["#a3a112", "#a3a112", "transparent"],
            "high": ["#962011", "#962011", "#962011"]
        }
        for color in colors[self.priority]:
            priority_label = ctk.CTkLabel(priority_frame, text="", fg_color=color, width=26, height=20, corner_radius=12)
            priority_label.pack(side='left', padx=3)

        delete_image = Image.open("images/delete.png")
        self.delete_button = ctk.CTkButton(priority_frame, text="", image=ctk.CTkImage(delete_image, size=(20, 20)),
                                           fg_color='transparent', command=self.delete_task,
                                           width=20, height=20, corner_radius=10, border_color='black', border_width=2)
        self.delete_button.pack(side='right', padx=5)

        check_image = Image.open("images/check.png")
        self.check_button = ctk.CTkButton(priority_frame, text="", image=ctk.CTkImage(check_image, size=(20, 20)),
                                          fg_color='transparent', command=self.toggle_task_completion,
                                          width=20, height=20, corner_radius=10, border_color='black', border_width=2)
        self.check_button.pack(side='right', padx=5)

    def toggle_task_completion(self):
        """Toggles the completion status of the task."""
        self.is_completed = not self.is_completed
        if self.is_completed:
            self.card_frame.configure(fg_color="#8c8c8c")  # Change card color to light grey
            self.check_button.configure(fg_color="green")  # Change check button color to green
        else:
            self.card_frame.configure(fg_color="#bdbdbd")  # Revert card color to normal
            self.check_button.configure(fg_color="transparent")  # Revert check button color

    def delete_task(self):
        """Deletes the task from the application."""
        self.app.remove_task(self)

class TodoApp:
    """
    Main application class for the To-Do List.

    Attributes:
        root (tk.Tk): The main application window.
        tasks (list): List of TaskCard instances representing current tasks in the application.
        main_frame (customtkinter.CTkFrame): Main frame containing all UI elements.
        title_label (customtkinter.CTkLabel): Label displaying the application title.
        task_frame (customtkinter.CTkScrollableFrame): Scrollable frame for displaying tasks.
        entry_frame (customtkinter.CTkFrame): Frame containing task entry and controls.
        task_entry (customtkinter.CTkEntry): Entry widget for entering new tasks.
        priority_var (tk.StringVar): Variable storing the selected priority ("low", "medium", "high").
        priority_buttons (dict): Dictionary storing priority radio buttons.
        priority_label (customtkinter.CTkLabel): Label displaying the priority selection title.
        add_button (customtkinter.CTkButton): Button to add a new task.

    Methods:
        create_priority_buttons(): Creates and packs priority selection buttons.
        add_task(): Adds a new task to the application based on user input.
        remove_task(task_card): Removes the specified task from the application.
    """

    def __init__(self, root):
        """
        Initializes the TodoApp instance.

        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x600")
        self.root.resizable(False, False)  # Fix the overall geometry

        # Load and set the new icon
        root.iconbitmap('images/to-do-list.ico')

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.tasks = []

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="To-Do List", font=("Helvetica", 24))
        self.title_label.pack(pady=10)

        self.task_frame = ctk.CTkScrollableFrame(self.main_frame)  # Use CTkScrollableFrame for scrollable tasks
        self.task_frame.pack(pady=10, fill="both", expand=True)

        self.entry_frame = ctk.CTkFrame(self.main_frame)
        self.entry_frame.pack(pady=5, fill='x')

        self.task_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter a new task")
        self.task_entry.pack(padx=10, pady=10, fill='x')
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.priority_var = StringVar(value="low")

        self.priority_label = ctk.CTkLabel(self.entry_frame, text="Priority", font=("Arial", 18))
        self.priority_label.pack(padx=(2))

        self.create_priority_buttons()

        self.add_button = ctk.CTkButton(self.main_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

    def create_priority_buttons(self):
        """Creates and packs priority selection buttons."""
        priority_info = [("Low", "green"), ("Medium", "yellow"), ("High", "red")]
        self.priority_buttons = {}
        for priority, color in priority_info:
            self.priority_field_label = ctk.CTkLabel(self.entry_frame, text=f"{priority}:", font=("Arial", 14))
            self.priority_field_label.pack(padx=(15, 10), side='left')

            button = Radiobutton(self.entry_frame, variable=self.priority_var, value=priority.lower(),
                                 indicatoron=0, width=5, height=1, selectcolor=color, bg='white')
            button.pack(side='left', padx=10)

            self.priority_buttons[priority.lower()] = button

    def add_task(self):
        """Adds a new task based on user input."""
        task_name = self.task_entry.get()
        if task_name:
            priority = self.priority_var.get()
            task_card = TaskCard(self.task_frame, task_name, self, priority)
            self.tasks.append(task_card)
            self.task_entry.delete(0, "end")
        else:
            messagebox.showwarning("Warning", "You must enter a task")

    def remove_task(self, task_card):
        """Removes the specified task from the application."""
        self.tasks.remove(task_card)
        task_card.card_frame.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()
