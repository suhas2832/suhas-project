import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

# Default JSON template
default_json = {
    "scenario_spec": {
        "name": "",
        "user_agent_spec": {
            "priming_inputs": [
                {
                    "input_type": "system_instruction",
                    "content": "Hey Siri set a reminder tomorrow at 8 AM to look into that green invoice"
                }
            ]
        },
        "assistant_agent_spec": {
            "priming_inputs": []
        },
        "conversation": [
            {
                "input_type": "agent_response",
                "content": "Hey Siri set a reminder tomorrow at 8 AM to look into that green invoice",
                "tool_calls": None,
                "introspection": None,
                "source": "user"
            }
        ],
        "initial_state": {
            "entities": [],
            "reference_time": "2024-01-01T00:00:00+00:00"
        },
        "joint_resolver_mock_config": None,
        "max_num_turns": 30,
        "required_tools": ["create_reminder"],
        "tool_allow_list": [],
        "tool_deny_list": [],
        "tags": ["SiriX", "EVAL", "Reminder", "BaselineTaskExecution"]
    },
    "evaluation_spec": {
        "evaluators": []
    },
    "locale": "en_US",
    "name": None
}

class JSONScenarioGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Scenario Generator")

        # Variables
        self.scenario_name = tk.StringVar()
        self.entities = []

        # Scenario Name
        ttk.Label(root, text="Scenario Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.scenario_name_entry = ttk.Entry(root, textvariable=self.scenario_name, width=40)
        self.scenario_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Entities Section
        ttk.Label(root, text="Initial Entities:").grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        self.entities_frame = ttk.Frame(root)
        self.entities_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Add Entity Button
        ttk.Button(root, text="Add Entity", command=self.add_entity).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Export Button
        ttk.Button(root, text="Export JSON", command=self.export_json).grid(row=3, column=1, padx=10, pady=5, sticky="e")

    def add_entity(self):
        """Add a new entity entry"""
        entity_window = tk.Toplevel(self.root)
        entity_window.title("Add Entity")

        # Entity Fields
        entity_type = tk.StringVar()
        entity_id = tk.StringVar()
        entity_name = tk.StringVar()

        ttk.Label(entity_window, text="Entity Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(entity_window, textvariable=entity_type, width=30).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(entity_window, text="Entity ID:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(entity_window, textvariable=entity_id, width=30).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(entity_window, text="Entity Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(entity_window, textvariable=entity_name, width=30).grid(row=2, column=1, padx=10, pady=5)

        def save_entity():
            entity = {
                "type_name": entity_type.get(),
                "id": entity_id.get(),
                "name": entity_name.get()
            }
            self.entities.append(entity)
            entity_window.destroy()
            messagebox.showinfo("Success", "Entity added successfully!")

        ttk.Button(entity_window, text="Save", command=save_entity).grid(row=3, column=1, padx=10, pady=10, sticky="e")

    def export_json(self):
        """Export the JSON with the provided data"""
        # Populate the default JSON structure
        default_json["scenario_spec"]["name"] = self.scenario_name.get()
        default_json["scenario_spec"]["initial_state"]["entities"] = self.entities

        # Save to file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(default_json, f, indent=4)
            messagebox.showinfo("Success", f"JSON exported successfully to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONScenarioGenerator(root)
    root.mainloop()
