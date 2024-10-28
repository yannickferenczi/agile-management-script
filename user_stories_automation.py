import gspread
from pprint import pprint
import os
from dotenv import load_dotenv


load_dotenv()

class Epic:
    def __init__(self, title:str, body:str, milestone:str, labels:list,
                 user_stories:list=[]):
        self.title = title
        self.body = body
        self.milestone = milestone
        self.labels = labels
        self.user_stories = user_stories
    
    def create_tasks(self):
        tasks = ""
        for story in self.user_stories:
            tasks += f"\n    - [ ] #{story}"
        return tasks

    def add_tasks_to_body(self):
        self.body += self.create_tasks()



class UserStory:
    def __init__(self, title:str, body:str, milestone:str, labels:list):
        self.title = title
        self.body = body
        self.milestone = milestone
        self.labels = labels
    


if __name__ == "__main__":

    google_connection = gspread.service_account(
        filename=os.getenv("CREDENTIALS")
    )

    spreadsheet = google_connection.open("User Stories")

    # Iterate over the user stories in Google Sheet to create them on Github
    current_epic = ""
    current_milestone = ""
    agile_objects = {}
    epic_count = 0 # tracks the number of epics
    user_story_count = 0 # tracks the number of user stories
    for i in range(2, 5):
        print(f"Loop {i}")
        epic_title = spreadsheet.worksheet(
            "Features").acell(f"F{i}").value
        if current_epic == "":
            current_epic = epic_title
            epic_tracker = i
            milestone = spreadsheet.worksheet(
                "Features").acell(f"H{epic_tracker}").value
        
        if epic_title == current_epic or epic_title == None:
            user_story_count += 1
            issue_title = "USER STORY: " + spreadsheet.worksheet(
                "Features").acell(f"J{i}").value
            issue_body = spreadsheet.worksheet(
                "Features").acell(f"K{i}").value
            issue_labels = spreadsheet.worksheet(
                "Features").acell(f"L{i}").value
            object_key = f"user_story_{user_story_count}"
            agile_objects[f"user_story_{user_story_count}"] = UserStory(
                issue_title, issue_body, milestone, issue_labels
            )
            # print("User Story object created!")
        elif epic_title != current_epic:
            epic_count += 1
            epic_title = "EPIC: " + current_epic
            milestone = spreadsheet.worksheet(
                "Features").acell(f"H{epic_tracker}").value
            epic_body = spreadsheet.worksheet(
                "Features").acell(f"G{epic_tracker}").value
            epic_labels = spreadsheet.worksheet(
                "Features").acell(f"I{epic_tracker}").value
            object_key = f"epic_{epic_count}"
            agile_objects[object_key] = Epic(
                current_epic, epic_body, milestone, epic_labels
            )
            epic_tracker = i
            milestone = spreadsheet.worksheet(
                "Features").acell(f"H{epic_tracker}").value

            # print("Line 75: ", agile_objects[f"epic_{epic_count}"])
        else:
            print("Unpredicted scenario!")
    print(epic_tracker)
    print("This is the result of your hard work: ", agile_objects)

    for obj in agile_objects.values():
        print(obj.title, obj.body, sep=" - ")

    # label_names = spreadsheet.worksheet("Labels").col_values(1)
    # label_descriptions = spreadsheet.worksheet("Labels").col_values(2)
    # label_colors = spreadsheet.worksheet("Labels").col_values(3)
