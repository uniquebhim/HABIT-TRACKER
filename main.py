import requests
from datetime import datetime


class HabitTracker:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.pixela_endpoints = "https://pixe.la/v1/users"
        self.date = None
        self.graph_id = None
        self.want_end = True
        self.entry_point()

    def entry_point(self):
        while self.want_end:
            option = int(input("\n1. User Create\n2. User Delete\n3. Create New-Habit-Tracker\n4. Graph delete\n5. Add Task\n6. Update Task\n7. Delete Task\n8. EXIT\n\t\t\tEnter your Choice:"))

            if option == 1:
                self.create_user()
            elif option == 2:
                self.delete_user()
            elif option == 3:
                self.create_graph()
            elif option == 4:
                self.delete_graph()
            elif option == 5:
                self.create_pixel()
            elif option == 6:
                self.update_pixel()
            elif option == 7:
                self.delete_pixel()
            elif option == 8:
                self.end()
            else:
                print("Invalid option chosen")

    def end(self):
        self.want_end = False

    def set_date(self):
        want_change = input("Do you want to change date (YES/NO)").lower()
        if want_change == "yes":
            day, month, year = map(int, input("Enter the day, month and year (separated by commas): ").split(','))
            date_formatted = datetime(year=year, month=month, day=day)
        else:
            date_formatted = datetime.now()
        self.date = date_formatted.strftime("%Y%m%d")

    def create_user(self):
        user_params = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }
        user_response = requests.post(url=self.pixela_endpoints, json=user_params)
        check = user_response.json()
        if check["isSuccess"]:
            print("Successful User Created!")
        else:
            print("Unsuccessful User Created!")
        print(check["message"])

    def delete_user(self):
        headers = {"X-USER-TOKEN": self.token}
        delete_user_endpoint = f"{self.pixela_endpoints}/{self.username}"
        user_delete_response = requests.delete(url=delete_user_endpoint, headers=headers)
        check = user_delete_response.json()
        if check["isSuccess"]:
            print("Successful User Deleted!")
        else:
            print("Unsuccessful User Deleted!")
        print(check["message"])

    def create_graph(self):
        headers = {"X-USER-TOKEN": self.token}
        graphs_endpoint = f"{self.pixela_endpoints}/{self.username}/graphs"
        self.graph_id = str(input("Enter the graph-ID [(a-z)+(0-9)]:"))
        graphs_config = {
            "id": self.graph_id,
            "name": input("Enter the Habit name:"),
            "unit": input("Enter the Habit measurement unit(km, kilogram, calorie):").lower(),
            "type": "float",
            "color": "shibafu"
        }
        graph_response = requests.post(url=graphs_endpoint, json=graphs_config, headers=headers)
        check = graph_response.json()
        if check["isSuccess"]:
            print("Successful Graph Created!")
            print(f"{graphs_endpoint}/{self.graph_id}.html")
        else:
            print("Unsuccessful Graph_created! ")
        print(check["message"])
    
    def graph_delete(self):
        headers = {"X-USER-TOKEN": self.token}
        graphs_delete_endpoint = f"{self.pixela_endpoints}/{self.username}/graphs/{self.graph_id}"
        graph_delete_response = requests.post(
            url=graphs_delete_endpoint, headers=headers)
        check = graph_delete_response.json()
        if check["isSuccess"]:
            print("Successful Graph deleted! ")
        else:
            print("Unsuccessful Graph deleted! ")
        print(check["message"])


    def pixal_creation(self):
        headers = {"X-USER-TOKEN": self.token}
        self.date()
        pixal_creation_endpoint = f"{self.pixela_endpoints}/{self.username}/graphs/{self.graph_id}"
        pixal_creation_config = {
            "date": self.DATE,
            "quantity": str(input("Enter the value of quantity:"))
        }
        pixal_creation_response = requests.post(
            url=pixal_creation_endpoint, json=pixal_creation_config, headers=headers)
        check = pixal_creation_response.json()
        if check["isSuccess"]:
            print("Successful Pixel_created! ")
            print(f"{pixal_creation_endpoint}.html")
        else:
            print("Unsuccessful Pixel_created! ")
        print(check["message"])

    def update_pixal(self):
        self.date()
        headers = {"X-USER-TOKEN": self.token}
        update_pixel_endpoint = f"{self.pixela_endpoints}/{self.username}/graphs/{self.graph_id}/{self.date}"
        update_pixel_config = {
            "quantity": str(input("Enter the value of quantity:"))
        }
        update_pixal_response = requests.put(url=update_pixel_endpoint,
                                             json=update_pixel_config, headers=headers)
        check = update_pixal_response.json()
        if check["isSuccess"]:
            print("Successful Updated! ")
        else:
            print("Unsuccessful Updated! ")
        print(check["message"])

    def delete_pixal(self):
        headers = {"X-USER-TOKEN": self.token}
        self.date()
        delete_pixel_endpoint = f"{self.pixela_endpoints}/{self.username}/graphs/{self.graph_id}/{self.date}"
        delete_pixal_response = requests.delete(url=delete_pixel_endpoint, headers=headers)
        check = delete_pixal_response.json()
        if check["isSuccess"]:
            print("Successful Deleted! ")
        else:
            print("Unsuccessful Deleted! ")
        print(check["message"])


if __name__ == "__main__":
    print("\n\t\t\tWelcome to Habit-Tracker-Application")
    users = {}
    for i in range(int(input("Enter the number user you want to create(0-9):"))):
        username = input("Enter the username for user {} [(a-z)+(0-9)]:".format(i+1))
        token = input("Enter the password for user {} [8-18]:".format(i+1))
        if len(token)<8:
            print("Invalid password! ")
            token = input("Enter the password for user {} [8-18]:".format(i+1))
        users[f"{username}"] = f"{token}"
        
    print(users) 

    user_id = input("Enter the username to login:")
    if user_id in users:
        user=habit_tracker(users[user_id], user_id)
