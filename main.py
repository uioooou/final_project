from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarListItem, ImageLeftWidget, TwoLineListItem, ThreeLineAvatarIconListItem, OneLineAvatarListItem
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
import cv2
import os
import time
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
import time
import requests
import json
import pyrebase
from threading import Thread
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import csv 
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage





config = {
    "apiKey": "AIzaSyALpYJGrYwu25DebuwBQ94Majt2iwnOXYI",
    "authDomain": "examattendance-ab116.firebaseapp.com",
    "databaseURL": "https://examattendance-ab116-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "examattendance-ab116",
    "storageBucket": "examattendance-ab116.appspot.com",
    "messagingSenderId": "181886439951",
    "appId": "1:181886439951:web:6c8f2c13ffcd46bd87497a",
    "measurementId": "G-S32HBLPMPX"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def csv_to_json(csv_file_path):
    data = {}
    
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            venue = row["venue"]
            student_id = row["Students"]
            
            # Check if the venue exists in the data dictionary
            if venue not in data:
                data[venue] = {
                    "administrator": row["Administrator"],
                    "invigilators": [row["Invigilators"]],
                    "Students": {},
                    "date": row["date"]
                }
            else:
                # Add invigilator if not already added
                if row["Invigilators"] not in data[venue]["invigilators"]:
                    data[venue]["invigilators"].append(row["Invigilators"])
                
            # Add student information
            data[venue]["Students"][student_id] = {
                "status": row["status"],
                "time": row["time"],
                "venue": row["venue"],
                "student_id": row["student_id"],
                "email": row["email"],
            }
    
    return data

class LoginManager():
    def __init__(self):
        self.logged_in_user = None

    def login(self, username):
        self.logged_in_user = username

    def logout(self):
        self.logged_in_user = None


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    def on_touch_down(self, touch):
        # Ignore touch events
        return True

class NormalThreeLineAvatarListItem(ThreeLineAvatarIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.venue= ""
        self.size = (800,120)
        self.bg_color = [0.84, 0.84, 0.84, 1]

class VenueListItem(ThreeLineAvatarIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.venue= ""
        self.data = ""
        self.size = (800,120)
        self.bg_color = [0.84, 0.84, 0.84, 1]
    
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # If the touch event occurred within the bounds of the list item
            self.on_item_click()
            return True
        return super().on_touch_down(touch)
    
    def on_item_click(self, *args):
        App.get_running_app().root.get_screen('Attendance_student').ids.student_screen.title = f'{self.venue}|{self.data}'
        App.get_running_app().root.current = 'Attendance_student'

class studentThreeLineAvatarListItem(ThreeLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.image_source = ""
        self.size = (800,120)
        self.subject = ""
        self.bg_color = [0.84, 0.84, 0.84, 1]
        mycheckbox = self.ids.checkbox
        mycheckbox.active = False
        if App.get_running_app().username == "liewyikpui_1utar_my":
            print("U are admin")

    def checkbox_active(self):
        mycheckbox = self.ids.checkbox
        mycheckbox.active = True
    
    def change_image_source(self, student_name, database):
        print("u are inside change_image")
        print(student_name)
        db = firebase.database()
        all_users = db.child("Users").get().val()
        user_found =""

        # Iterate through the users' data to find the user with the matching name
        for user_id, user_data in all_users.items():
            if user_data.get("name") == student_name:
                print("Local ID:", user_id)
                user_found = user_id
            break  # Exit loop after finding the first matching user
        user_data2 = db.child("Users").child(user_found).get().val()
        print(user_data2)
        image_source = user_data2.get("image_source", "")
        print(f"image here: {image_source}")
        return image_source
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Create and display the image popup
            print("u found this")
            image = AsyncImage(source=self.image_source)
            popup = Popup(title='Face image', content=image, size_hint=(None, None), size=(400, 400))
            popup.open()
            return True
        return super().on_touch_down(touch)
class CustomThreeLineAvatarListItem(ThreeLineAvatarIconListItem):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.size = (800,120)
        self.subject = ""
        self.bg_color = [0.84, 0.84, 0.84, 1]
        mycheckbox = self.ids.checkbox
        mycheckbox.active = False
        if App.get_running_app().username == "liewyikpui_1utar_my":
            print("U are admin")
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # If the touch event occurred within the bounds of the list item
            self.on_item_click()
            return True
        return super().on_touch_down(touch)

    def on_item_click(self, *args):
        App.get_running_app().root.get_screen('Attendance_check').ids.venue_screen.title = self.subject
        print(f'{self.subject}')
        App.get_running_app().root.current = 'Attendance_check'

    def checkbox_active(self):
        mycheckbox = self.ids.checkbox
        mycheckbox.active = True
    

class LoginScreen(Screen):
    database_url = "https://examattendance-ab116-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_manager = App.get_running_app().login_manager

    def verify_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            print("login firebase succesful")
            db = firebase.database()
            user_id = user['localId'] 
            user_data = db.child("Users").child(user_id).get().val()
            user_data2 = user_data.get("name", {})
            App.get_running_app().username = user_data2
            App.get_running_app().local_id = user_id
            print(user_data)
            print(user_data2)
            
            self.manager.current = "ExamScreen"

        except Exception as e:
            print("Login failed! Incorrect password.")
            self.ids.error_label.text = "Incorrect password"
        
        

class MainScreen(Screen):
    def on_pre_enter(self):
        username = App.get_running_app().username
        print("Logged in user:", username)

class Attendance_student(Screen):
    
    def on_pre_enter(self):
        self.ids.student_attendance_check.clear_widgets()
        self.database_url = App.get_running_app().database_firebase
        self.subject = self.ids["student_screen"].title

    def student_list(self):
    
        res = requests.get(url=self.database_url)
        exam_data = res.json().get("Exams", {})
        exam_info = self.subject
        for exam_id, exam_details1 in exam_data.items():
            if exam_id ==  exam_info.split("|")[0]:
                for venue_id, exam_details2 in exam_details1.items():
                    if venue_id == exam_info.split("|")[1]:
                        students = exam_details2.get('Students', {})
                        for student_name, students_info in students.items():
                            item = studentThreeLineAvatarListItem(
                                text = f"{student_name}",
                                secondary_text=f"student id: {students_info.get('student_id', '')}",
                                tertiary_text=f"checktime: {students_info.get('time', '')}",

                            )
                            status =  students_info.get('status',{})
                            if status == "present":
                                studentThreeLineAvatarListItem.checkbox_active(self = item)

                                
                            try:
                                item.image_source = item.change_image_source(student_name, self.database_url)
                            except Exception as e:
                                print(f"Error in Venue_list: {e}")
                            self.ids.student_attendance_check.add_widget(item)

                            
    


    def back(self):
        App.get_running_app().root.current = 'Attendance_check'

class Attendance_check(Screen):
    
    def on_pre_enter(self):
        self.ids.exam_attendance_check.clear_widgets()
        self.database_url = App.get_running_app().database_firebase
        self.subject = self.ids["venue_screen"].title

    def Venue_list(self):
        try:
            res = requests.get(url=self.database_url)
            exam_data = res.json().get("Exams", {})
            for exam_id, exam_details1 in exam_data.items():
                if exam_id ==  self.subject:
                    for venue_id, exam_details2 in exam_details1.items():
                        item = VenueListItem(
                            text=f"{venue_id}",
                            secondary_text=f"Exam date: {exam_details2.get('date', '')},",
                        )
                        item.data = venue_id
                        item.venue = self.subject
                        self.ids.exam_attendance_check.add_widget(item)
        except Exception as e:
            print(f"Error in Venue_list: {e}")


    def back(self):
        App.get_running_app().root.current = 'ExamScreen'

class ExamScreen(Screen):

    exam_database = "https://examattendance-ab116-default-rtdb.asia-southeast1.firebasedatabase.app/Exams.json"

    def on_pre_enter(self):
        self.ids.exam_container_go.clear_widgets()
        self.username = App.get_running_app().username
        self.database_url = App.get_running_app().database_firebase
        print("Logged in user:", self.username)


    def populate_exam_container(self):
        res = requests.get(url=self.database_url)
        exam_data = res.json().get("Exams", {})
        for exam_id, exam_details1 in exam_data.items():
            for venue_id , exam_details in exam_details1.items():
                students = exam_details.get('Students', {})
                if self.username in students:
                    item = CustomThreeLineAvatarListItem(
                        text=f"Exam {exam_id}",
                        secondary_text=f"Exam venue: {venue_id}",
                        tertiary_text=f"Exam date: {exam_details.get('date', '')}",
                    )
                    status =  students[self.username].get('status',{})
                    item.subject = exam_id
                    if status == "present":
                        CustomThreeLineAvatarListItem.checkbox_active(self = item)
                    image = ImageLeftWidget()
                    image.source = "Mobile_photo\icon\exam.png"
                    item.add_widget(image)
                    self.ids.exam_container_go.add_widget(item)
        
    def Go_examscreen(self):
        self.manager.current = "CreateExam"
        
class ProfileScreen(Screen):

    def on_pre_enter(self):
        self.username = App.get_running_app().username
        self.database_url = App.get_running_app().database_firebase
        self.local_id = App.get_running_app().local_id
        print("Logged in user:", self.username)
    
    def show_profile(self):
        res = requests.get(url=self.database_url)
        profile_data = res.json().get("Users", {}).get(self.local_id)
        print(profile_data)
        self.ids.profile_image.source = profile_data.get("image_source", "")
        self.ids.profile_name.text = "Name: " + profile_data.get("name", "")
        self.ids.profile_email.text = "Email: " + profile_data.get("email", "")
        self.ids.profile_id.text = "ID: " + profile_data.get("student_id", "")
        self.ids.profile_faculty.text = "Faculty: " + profile_data.get("faculty", "")
    
class ScreenManagement(ScreenManager):
   pass

class NotificationScreen(Screen):
    def on_pre_enter(self):
        self.ids.notify_container_go.clear_widgets()
        self.username = App.get_running_app().username
        self.local_id = App.get_running_app().local_id
        self.database_url = App.get_running_app().database_firebase
        print("Logged in user:", self.username)


    def populate_notify_container(self):
        res = requests.get(url=self.database_url)
        exam_data = res.json().get("Exams", {})
        for exam_id, exam_details in exam_data.items():
            for venue_id, exam_details1 in exam_details.items():
                students = exam_details1.get('Students', {})
                student = students.get(self.username, {})
                status = student.get('status')  # Removed default value '{}'
                if status == "absent":
                    item = NormalThreeLineAvatarListItem(
                        text=f"Exam {exam_id} Incoming !",
                        secondary_text=f"Exam venue: {exam_details.get('venue', '')} , Exam date: {exam_details.get('date', '')} ",
                        tertiary_text=f"Remember to Update your Face ID data for verification"
                    )
                    self.ids.notify_container_go.add_widget(item)


class CreateExam(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_url = "https://console.firebase.google.com/u/0/project/examattendance-ab116/storage/examattendance-ab116.appspot.com/files"
        Window.bind(on_keyboard=self.events)
        self.csv_path = ""
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".csv"],
        )
        self.name = "create_exam"

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):

        self.exit_manager()
        toast(path)
        base_filename = path.split("\\")[-1]
        self.csv_path = path
        self.ids.file_label.text = base_filename
        

    def exit_manager(self, *args):

        self.manager_open = False
        self.file_manager.close()
    

    def Back_home(self):
        self.manager.current = "ExamScreen"


    def events(self, instance, keyboard, keycode, text, modifiers):

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    
    def create_exam(self):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        json_data = csv_to_json(self.csv_path)

        exam_name = self.ids["exam_name"].text

        # Specify the Firebase Realtime Database path to store the JSON data
        database_path = f"Exams/{exam_name}"

        # Store JSON data in Firebase Realtime Database
        try:
            db.child(database_path).set(json_data)
            print("Data successfully stored in Firebase Realtime Database")
            self.Go_back()  # Call the back() function after success
        except Exception as e:
            print("Error:", e)
            # Provide feedback to the user
            self.show_error_message("Database upload failed. Please try again.")
    
    def Go_back(self):
        self.manager.current = "ExamScreen"

class CameraCapture(Screen):#######this one need to change ios and andorid apk
    def on_pre_enter(self):
        self.ids['instruction'].text = "Put your face Inside the box"
        self.username = App.get_running_app().username
        self.database_url = "https://console.firebase.google.com/u/0/project/examattendance-ab116/storage/examattendance-ab116.appspot.com/files"
        print("Logged in user:", self.username)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Start the continuous face detection
        Clock.schedule_interval(self.detect_face, 1.0 / 60.0)  # 30 frames per second
    

    def BackHome(self):
        self.manager.current = "ExamScreen"
    
    def on_leave(self):
        # Stop the continuous face detection when leaving the screen
        Clock.unschedule(self.detect_face)

    def detect_face(self, dt):
        # Capture a frame from the camera
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("temp_frame.png")
        img = cv2.imread("temp_frame.png")
        
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Perform face detection
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Update the font color based on face detection
        label = self.ids['label_face']
        if len(faces) > 0:
            # Face detected, change font color to green
            label.color = [0, 1, 0, 1]  # Green color
            label.text = "Face Detected"
        else:
            # No face detected, change font color to red
            label.color = [1, 0, 0, 1]  # Red color
            label.text = "No Face Detected"
    
    def uploadphoto_firebase(self):

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        base_dir ="C:/Users/user/Downloads/FYP_mobile/"
        exam_photo_dir = os.path.join(base_dir, "exam_photo")
        print(exam_photo_dir)
        for filename in os.listdir(exam_photo_dir):
            print("error here")
            if filename.endswith(".jpg"):
                path_on_cloud = f"{self.username}/{filename}"
                print(path_on_cloud)
                path_local = f"{exam_photo_dir}/{filename}"
                storage.child(path_on_cloud).put(path_local)
                os.remove(path_local)

    def capture(self):
        
        camera = self.ids['camera']
        base_dir ="C:/Users/user/Downloads/FYP_mobile"
        exam_photo_dir = os.path.join(base_dir, "exam_photo")
    
        # Check if the exam_photo directory exists, if not, create it
        if not os.path.exists(exam_photo_dir):
            os.makedirs(exam_photo_dir)
        for i in range(5):
            timestr = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(exam_photo_dir, "IMG_{}_{}.jpg".format(timestr, i+1))
            camera.export_to_png(filename)

            print("Captured photo", i+1)
            # Wait for 2 seconds before capturing the next photo
            time.sleep(0.2)
        label2 =  self.ids['instruction']
        label2.text = "Face Image Capture Completed"
        upload_thread = Thread(target=self.uploadphoto_firebase)
        upload_thread.start()

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_manager = LoginManager()
        self.screen_manager = ScreenManager()
        self.database_firebase = "https://examattendance-ab116-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
        self.username = None  # Global variable to store username
        self.local_id =None

    
    def build(self):

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        return Builder.load_file('exam_App.kv') #Replaced load_string with load_file
    

if __name__ == '__main__':
    MyApp().run()
