from kivy.config import Config
Config.set('graphics', 'width', '414')
Config.set('graphics', 'height', '736')

import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty

class CheckBoxLabel(BoxLayout):
    text = StringProperty("")
    completed = BooleanProperty(False)
    
class ToDoRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_tasks()
            
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf=8") as f:
                try:
                    tasks = json.load(f)
                    self.ids.rv.data = [
                        {
                            "text": t["text"],
                            "completed": t.get("completed", False)
                        }
                        for t in tasks
                    ]
                except json.JSONDecodeError:
                    print("Error loading JSON")
    
    def toggle_completed(self, text):
        for item in self.ids.rv.data:
            if item["text"] == text:
                item["completed"] = not item ["completed"]
                break
        self.save_tasks()
        
    def add_task(self, text):
        if text.strip():
            self.ids.rv.data.append({"text": text, "completed": False})
            self.ids.task_input.text = ""
            self.save_tasks()
            
    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.ids.rv.data, f, ensure_ascii=False, indent=4)
            
class ToDoApp(App):
    def build(self):
        return ToDoRoot()
    
if __name__ == "__main__":
    ToDoApp().run()