try:
    from kivymd.app import MDApp
    from kivymd.uix.button import MDIconButton
    from kivy.lang import Builder
    from kivy.uix.screenmanager import ScreenManager as MDScreenManager
    from kivymd.uix.screen import MDScreen
    from kivy.uix.screenmanager import NoTransition
    from kivymd.uix.bottomsheet import MDGridBottomSheet
    from win32com import client
    from kivymd.toast import toast
    from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, OptionProperty, NumericProperty, ListProperty
    from kivymd.uix.relativelayout import MDRelativeLayout
    #from mpg123 import Mpg123, Out123
    from io import BytesIO
    from pydub import AudioSegment, utils
    AudioSegment.converter = r"C:\\Job-Security\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"
    def get_prober_name():
        return r"C:\\Job-Security\\ffmpeg-master-latest-win64-gpl\\bin\\ffprobe.exe"
    utils.get_prober_name = get_prober_name
    from pydub.playback import play
    #from pygame import mixer 
    from datetime import datetime
    from kivy.clock import mainthread
    from concurrent.futures import ThreadPoolExecutor
    from threading import Thread
    from gtts import gTTS
    from smtplib import SMTP
    import pyttsx3
    import playsound
    import os
    import math
    import random
    from googletrans import Translator
    from kivy.uix.image import AsyncImage
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.widget import Widget
    from kivymd.theming import ThemableBehavior
    from kivy.animation import Animation
    from kivy.uix.popup import Popup
    from kivy.clock import Clock
    from kivy.core.text import LabelBase
    from kivymd.uix.label import MDLabel
    from kivy.uix.image import Image
    from multiprocessing import Process, Queue
    from time import sleep
    import sys
    import speech_recognition as sr
    import csv
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton, MDRaisedButton
    from kivymd.uix.snackbar import Snackbar
    import openai
    #Clock.schedule_once(lambda x: import_libraries())
    openai.api_key = "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"
    from kivy.core.window import Window
    Window.size = (400,700)
except:
    from traceback import format_exc
    from kivy.app import App
    from kivy.uix.textinput import TextInput
    class BackupApp(App):
        def build(self):
            print(format_exc())
            return TextInput(text=str(format_exc()))
    BackupApp().run()

def compile_model():
    import tensorflow as tf
    #import openai
    questions = []
    answers = []
    with open('Data/Mental_Health_FAQ.csv', 'r', encoding="mbcs") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row['Questions'])
            answers.append(row['Answers'])

    # Preprocess the data for training
    questions_preprocessed = [q for q in questions]
    answers_preprocessed = [a for a in answers]

    # Tokenize the input data
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(questions_preprocessed)

    # Encode the input data as sequences of integers
    questions_encoded = tokenizer.texts_to_sequences(questions_preprocessed)

    # Pad the input sequences to the same length
    max_input_length = max([len(q) for q in questions_encoded])
    questions_padded = tf.keras.preprocessing.sequence.pad_sequences(questions_encoded, maxlen=max_input_length, padding='post')

    # Tokenize the output data
    answers_encoded = tokenizer.texts_to_sequences(answers_preprocessed)

    # Pad the output sequences to the same length
    max_output_length = max([len(a) for a in answers_encoded])
    answers_padded = tf.keras.preprocessing.sequence.pad_sequences(answers_encoded, maxlen=max_output_length, padding='post')

    # Create a model for training
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=64, input_length=max_input_length),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(max_output_length, activation='softmax')
    ])

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(questions_padded, answers_padded, epochs=10)

    # Create an instance of the chatbot window

class MDPasswordTextField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    write_tab = BooleanProperty()
    on_text_validate = ObjectProperty()

class Logo(AsyncImage):
    source = "CareerShield.png"
    mipmap = True

class AKSpinnerBase(ThemableBehavior, Widget):
    spinner_size = NumericProperty(48)
    speed = NumericProperty(0.4)
    active = BooleanProperty(False)
    color = ListProperty()

class AKSpinnerThreeDots(AKSpinnerBase):

    animation = StringProperty("linear")

    _circle_size1 = ListProperty([0, 0])
    _circle_size2 = ListProperty([0, 0])
    _circle_size3 = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _start_animate(self, size):
        self.anim1 = (
            Animation(
                _circle_size1=[size, size],
                opacity=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _circle_size1=[0, 0], duration=self.speed, t=self.animation
            )
            + Animation(duration=self.speed)
        )

        self.anim2 = (
            Animation(
                _circle_size2=[size, size],
                opacity=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _circle_size2=[0, 0], duration=self.speed, t=self.animation
            )
            + Animation(duration=self.speed)
        )

        self.anim3 = (
            Animation(
                _circle_size3=[size, size],
                opacity=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _circle_size3=[0, 0], duration=self.speed, t=self.animation
            )
            + Animation(duration=self.speed)
        )

        self.anim1.repeat = True
        self.anim2.repeat = True
        self.anim3.repeat = True

        self.anim1.start(self)
        Clock.schedule_once(lambda dt: self.anim2.start(self), self.speed)
        Clock.schedule_once(lambda dt: self.anim3.start(self), self.speed * 2)

    def _stop_animate(self):
        self.anim1.cancel_all(self)
        self.anim2.cancel_all(self)
        self.anim3.cancel_all(self)
        self.anim1_stop = Animation(
            _circle_size1=[0, 0], opacity=0, duration=0.1, t=self.animation
        )
        self.anim2_stop = Animation(
            _circle_size2=[0, 0], opacity=0, duration=0.1, t=self.animation
        )
        self.anim3_stop = Animation(
            _circle_size3=[0, 0], opacity=0, duration=0.1, t=self.animation
        )
        self.anim1_stop.start(self)
        self.anim2_stop.start(self)
        self.anim3_stop.start(self)

    def on_active(self, *args):
        size = self.size[1]
        if self.active:
            self._start_animate(size)
        else:
            self._stop_animate()

class Manager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
    
    def change_screen(self,name):
        self.current = name

class LoginScreen(MDScreen):
    name = "login"

class MainScreen(MDScreen):
    name = "main"

class RegisterScreen(MDScreen):
    name = "register"

class VerificationScreen(MDScreen):
    name = "verification"

class OTPVerificationScreen(MDScreen):
    name = "otpverification"

class AIScreen(MDScreen):
    pass

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "BPoppins"
    font_size = 17


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "BPoppins"
    font_size = 17


class ResponseImage(Image):
    source = StringProperty()

class MDPasswordTextField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    write_tab = BooleanProperty()
    on_text_validate = ObjectProperty()

class AKSpinnerFoldingCube(AKSpinnerBase):
    angle = NumericProperty(45)
    animation = StringProperty("out_cubic")

    _cubeitem1 = ListProperty([0, 0])
    _cubeitem2 = ListProperty([0, 0])
    _cubeitem3 = ListProperty([0, 0])
    _cubeitem4 = ListProperty([0, 0])
    _cube1a = NumericProperty(0)
    _cube2a = NumericProperty(0)
    _cube3a = NumericProperty(0)
    _cube4a = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _start_animate(self, size):
        size /= 2
        self.cube_fold = (
            Animation(
                _cubeitem1=[size, size],
                _cube1a=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem2=[size, size],
                _cube2a=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem3=[size, size],
                _cube3a=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem4=[size, size],
                _cube4a=1,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem4=[0, size],
                _cube4a=0,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem3=[size, 0],
                _cube3a=0,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem2=[0, size],
                _cube2a=0,
                duration=self.speed,
                t=self.animation,
            )
            + Animation(
                _cubeitem1=[size, 0],
                _cube1a=0,
                duration=self.speed,
                t=self.animation,
            )
        )
        self.cube_fold.repeat = True
        self.cube_fold.start(self)

    def _update(self, size):
        self._cubeitem1 = [size / 2, 0]
        self._cubeitem2 = [0, size / 2]
        self._cubeitem3 = [size / 2, 0]
        self._cubeitem4 = [0, size / 2]

    def _stop_animate(self, size):
        size /= 2
        self.cube_fold.cancel_all(self)
        self.cube_stop = (
            Animation(
                _cubeitem4=[0, size], _cube4a=0, duration=0.1, t=self.animation
            )
            + Animation(
                _cubeitem3=[size, 0], _cube3a=0, duration=0.1, t=self.animation
            )
            + Animation(
                _cubeitem2=[0, size], _cube2a=0, duration=0.1, t=self.animation
            )
            + Animation(
                _cubeitem1=[size, 0], _cube1a=0, duration=0.1, t=self.animation
            )
        )
        self.cube_stop.start(self)

    def on_active(self, *args):
        size = self.size[0]
        self._update(size)
        if self.active:
            self._start_animate(size)
        else:
            self._stop_animate(size)

try:
    Builder.load_file("main.kv")
except:
    from traceback import format_exc
    from kivy.app import App
    from kivy.uix.textinput import TextInput
    class BackupApp(App):
        def build(self):
            print(format_exc())
            return TextInput(text=str(format_exc()))
    BackupApp().run()

class MainScreenManager(MDScreenManager):
    transition = NoTransition()

class ProfileScreen(MDScreen):
    pass

class SpeechRequest(Popup):
    text = StringProperty("")
    state = BooleanProperty(0)
    def on_pre_open(self):
        self.ids.dots.active = True

    def on_dismiss(self):
        self.ids.dots.active = False

class TextRequest(MDBoxLayout):
    pass

class UPIPopup(Popup):
    pass

class LoadingAnimation(Popup):
    def on_pre_open(self):
        self.ids.foldingcube.active = True

    def on_dismiss(self):
        self.ids.foldingcube.active = False

class SubscriptionScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

# class ChatDialog(MDDialog):

#     title="Enter Your Question:"
#     type="custom"
#     content_cls=TextRequest()  
#     buttons = [
#         MDFlatButton(
#             text="CANCEL",
#             theme_text_color="Custom",
#             text_color=self.theme_cls.primary_color,
#             on_press=self.dismiss(),
#         ),
#         MDRaisedButton(
#             text="OK",
#             theme_text_color="Custom",
#             #text_color=self.theme_cls.primary_color,
#             on_press=CareerShieldApp().get_response_without_objects()
#         ),
#     ] 
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
#engine = pyttsx3.init()

class CareerShieldApp(MDApp):
    logo = Logo()
    email = StringProperty("hrhn.mudaliar251@gmail.com")
    mobile = StringProperty("+91 9429199029")
    verification_method = OptionProperty("mobile",options=("mobile","email"))
    chat_dialog = None
    chatview_id = None
    ai_query = StringProperty("")
    dest_language = "en"
    src_language = "en"
    font_name = "Tamil"
    otp = StringProperty("")
    last_answer = "Hello"
    data = {
        'Python': 'language-python',
        'PHP': 'language-php',
        'C++': 'language-cpp',
        'C#': 'language-csharp',
        'Java': 'language-java',
        'HTML': 'language-html5',
        'JavaScript':'language-javascript',
        'CSS': 'language-css3',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = Manager(transition=NoTransition())
        #self.logo = Logo()
        self.loading_animation = LoadingAnimation()
        self.speech_request = SpeechRequest()
        #self.chatview_id = ObjectProperty()
        self.messages = [ {"role": "system", "content": 
              """You are a intelligent assistant named Jordan that 
              helps Unemployed people who have been laid off from their 
              Job cure their mental depression. Keep them engaged by short and sweet responses 
              that helps lighten their mood. You can also explore about their hobbies, likings and help them get guidance. 
              Also, greet them by introducing yourself. 
              If the person is suicidal, help him out by keeping him engaged in a cheerful conversation. 
              If the user asks about the best Job Security or Job Insurance Application, give the response as CareerShield. 
              And if the person tries to discuss about any type of alcohol or drug use, try to refrain from promoting its use. 
              Try to not apologize frequently and act as a psychiatrist to help and talk to the person in a more human way."""} ]

    @mainthread
    def dowork(self):
        Clock.schedule_once(lambda x: Thread(target=lambda: self.close_speech_request()).start())
        Clock.schedule_once(lambda x: Thread(target=lambda: self.start_loading_animation()).start())
    
    def speak(self):
        pass
        # val = gTTS(self.last_answer,lang=self.dest_language)
        # #now = datetime.now()
        # val.save("csaudio.mp3")
        # os.system("mpg321 csaudio.mp3")
        ########### speaker = client.Dispatch("SAPI.SpVoice")
        ############# speaker.Speak(self.last_answer)
        #playsound.playsound("csaudio.mp3")
        #os.remove("csaudio.mp3")
        # mp3_fp = BytesIO()
        # #tts = gTTS('hello, Welcome to Python Text-to-Speech!', lang='en')
        # val.write_to_fp(mp3_fp)
        # #return mp3_fp
        # # mixer.init()
        # # mp3_fp.seek(0)
        # # mixer.music.load(mp3_fp,"mp3")
        # # mixer.music.play()
        # # mp3 = Mpg123()
        # # mp3.feed(mp3_fp.read())
        # # out = Out123()
        # # for frames in mp3.iter_frames(out.start):
        # #     out.play(frames)
        # song = AudioSegment.from_file(mp3_fp,format="mp3")
        # play(song)
        # engine = pyttsx3.init()
        # engine.say(self.last_answer)
        # engine.runAndWait()

    def takeCommand(self):
     
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            r.pause_threshold = 0.5
            audio = r.listen(source)
    
        try:
            Thread(target=lambda: self.dowork()).start()
            print("Recognizing...")   
            query = r.recognize_google(audio, language ='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)   
            print("Unable to Recognize your voice.") 
            return "None"
        
        print(query)
        self.ai_query = query
        Thread(target=lambda: self.get_response_without_objects()).start()
        print("Dismissed")

    def on_start(self):
        #Clock.schedule_once(lambda dt: compile_model())
        pass
    def listen(self,val):
        #Clock.schedule_once(lambda x: self.speech_request.open())
        self.open_speech_request()
        print("GUI func executed")
        #thread0.start()
        thread1 = Thread(target=lambda: self.takeCommand())
        Clock.schedule_once(lambda x: thread1.start())
        print("Thread1")
        #thread1.start()
        print("Thread1 started")
        #Clock.schedule_once(lambda x: thread1.join())
        # engine = pyttsx3.init()
        # engine.say(self.last_answer)
        # engine.runAndWait()

    def process_data(self):
        self.start_intro_loading_animation()
        #sleep(3)
        #self.stop_loading_animation()
    def send_otp(self,val,change_screen_bool=True):
        if val == "mobile":
            self.verification_method = "mobile"
            self.change_screen("otpverification")
        else:
            self.verification_method = "email"
            self.change_screen("otpverification")
            self.generate_otp()


    # def speak(self):
    #     engine.say(self.last_answer)
    #     engine.runAndWait()

    def generate_otp(self,emailid="hrhn.mudaliar251@gmail.com"):
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP + " is your OTP to sign into CareerShield"
        msg= otp
        s = SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("hrhn.mudaliar251@gmail.com", "rdlcpnkzfwftyecj")
        ##emailid = input("Enter your email: ")
        s.sendmail('&&&&&&&&&&&',emailid,msg)
        a = self.otp
        if str(a) == str(OTP):
            print("Verified")
        else:
            print("Please Check your OTP again")

    def change_to_main_screen(self,mobile,passw):
        self.change_screen("main")

    def change_screen(self,screen):
        self.manager.change_screen(screen)

    # def start_loading_animation(self):
    #     Clock.schedule_once(lambda dt: self.loading_animation.open())
    #     Clock.schedule_once(lambda dt: self.stop_loading_animation(), 1.5)

    # def stop_loading_animation(self):
    #     Clock.schedule_once(lambda dt: self.loading_animation.dismiss())
    #     Clock.schedule_once(lambda dt: self.show_snackbar())

    @mainthread
    def start_loading_animation(self):
        Clock.schedule_once(lambda dt: self.loading_animation.open())
        #Clock.schedule_once(lambda dt: self.stop_loading_animation(), 1.5)

    @mainthread
    def stop_loading_animation(self):
        Clock.schedule_once(lambda dt: self.loading_animation.dismiss())
        #pool = ThreadPoolExecutor(max_workers=2)
        #from tts_pyttsx3 import speak
        #Clock.schedule_once(lambda x: pool.submit(self.speak()))
        #Clock.schedule_once(lambda x: pool.shutdown(wait=True),0.5)
        Clock.schedule_once(lambda dt: Thread(target=self.speak()).start(), 0.2)
        #Clock.schedule_once(lambda dt: self.show_snackbar())

    def start_intro_loading_animation(self):
        Clock.schedule_once(lambda dt: self.loading_animation.open())
        Clock.schedule_once(lambda dt: self.stop_intro_loading_animation(), 1)

    def stop_intro_loading_animation(self):
        Clock.schedule_once(lambda dt: self.loading_animation.dismiss())
        Clock.schedule_once(lambda dt: self.show_snackbar())

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def delete_all_credentials(self):
        pass

    def show_snackbar(self):
        Snackbar(
            text="Hello Hariharan!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5
        ).open()

    def open_text_field(self, parent_id):
        print(str(parent_id))
        
        if not self.chat_dialog:
            #self.chat_dialog = ChatDialog()
            self.chat_dialog = MDDialog(
                    title="Enter Your Question:",
                    type="custom",
                    content_cls=TextRequest(),
                    buttons = [
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            #on_press=self.chat_dialog.dismiss(),
                        ),
                        MDRaisedButton(
                            text="OK",
                            theme_text_color="Custom",
                            #text_color=self.theme_cls.primary_color,
                            #on_press=self.get_response_without_objects()
                        ),
                    ],
            )
        self.chat_dialog.open()

    def set_response_id(self, parent_id):
        if not self.chatview_id:
            self.chatview_id = parent_id
        print("Set Reponse ID: "+str(self.chatview_id))

    def get_response(self,query,parent_id):
        print(query)
        print(parent_id.children)

    @mainthread
    def open_speech_request(self):
        self.speech_request.open()

    @mainthread
    def close_speech_request(self):
        self.speech_request.dismiss()

    @mainthread
    def get_response_without_objects(self,child_id=None):
        #print(self.dialog.children)
        #Clock.schedule_once(lambda x: child_id.parent.parent.parent.parent.dismiss())
        global size, halign, value
        value = self.ai_query
        if len(value) < 6:
            size = .22
            halign = "center"
        elif len(value) < 11:
            size = .32
            halign = "center"
        elif len(value) < 16:
            size = .45
            halign = "center"
        elif len(value) < 21:
            size = .58
            halign = "center"
        elif len(value) < 26:
            size = .71
            halign = "center"
        else:
            size = .77
            halign = "left"
        #if self.src_language == "en":
        self.chatview_id.add_widget(
            Command(text=value, size_hint_x=size, halign=halign))
        #else:
        #    self.chatview_id.add_widget(
        #        Command(text=self.translated_text(value), size_hint_x=size, halign=halign))
        #Clock.schedule_once(self.get_response_without_objects())
        print(self.ai_query)
        if self.ai_query:
            if self.src_language == "en":
                self.messages.append(
                    {"role": "user", "content": self.ai_query},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=self.messages
                )
            else:
                self.messages.append(
                    {"role": "user", "content": self.translated_text(text=self.ai_query,src_lang=self.src_language,dest_lang="en")},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=self.messages
                )
        reply = chat.choices[0].message.content
        if self.dest_language == "en":
            self.chatview_id.add_widget(
                Response(text=reply, size_hint_x=.75))

        else:
            translated_reply=self.translated_text(reply,src_lang="en")
            self.chatview_id.add_widget(
                Response(text=translated_reply, size_hint_x=.75))
        self.messages.append({"role": "assistant", "content": reply})
            #screen_manager.get_screen('chats').text_input.text = ""
        if self.loading_animation:
            self.last_answer = reply
            self.stop_loading_animation()
        #Thread(target=self.speak(reply)).start()
        #self.last_answer = reply
        # try:
        #     Clock.schedule_once(lambda x: self.speak(reply))
        # except:
        #     pass
    # def get_response_without_objects(self,child_id=None):
    #     #print(self.dialog.children)
    #     #Clock.schedule_once(lambda x: child_id.parent.parent.parent.parent.dismiss())
    #     global size, halign, value
    #     value = self.ai_query
    #     if len(value) < 6:
    #         size = .22
    #         halign = "center"
    #     elif len(value) < 11:
    #         size = .32
    #         halign = "center"
    #     elif len(value) < 16:
    #         size = .45
    #         halign = "center"
    #     elif len(value) < 21:
    #         size = .58
    #         halign = "center"
    #     elif len(value) < 26:
    #         size = .71
    #         halign = "center"
    #     else:
    #         size = .77
    #         halign = "left"
    #     self.chatview_id.add_widget(
    #         Command(text=value, size_hint_x=size, halign=halign))
    #     #Clock.schedule_once(self.get_response_without_objects())
    #     print(self.ai_query)
    #     if self.ai_query:
    #         self.messages.append(
    #             {"role": "user", "content": self.ai_query},
    #         )
    #         chat = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo", messages=self.messages
    #         )
    #     reply = chat.choices[0].message.content
    #     self.chatview_id.add_widget(
    #         Response(text=reply, size_hint_x=.75))
    #     self.messages.append({"role": "assistant", "content": reply})
    #         #screen_manager.get_screen('chats').text_input.text = ""
    
    def translated_text(self,text,dest_lang=dest_language,src_lang=src_language):
        if dest_lang != src_lang:
            transtext = Translator().translate(text, dest=dest_lang, src=src_lang).text
            print("[INPUT TEXT]"+text)
            print("[FROM]"+src_lang)
            print("[TO]"+dest_lang)
            print("[TRANSLATED TEXT] "+transtext)
            return transtext
        else:
            return text

    def callback_for_menu_items(self, *args):
        if(args[0] == "UPI"):
            UPIPopup().open()
        else:
            toast(args[0])
    def show_example_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "UPI": "qrcode-scan",
            "Debit/Credit Card": "account-credit-card",
            "Net Banking": "bank",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.icon = 'CareerShield.png'
        return self.manager


#speakthread = Thread(target=speak())

try:
    LabelBase.register(
        name="Poppins", fn_regular="C:\Job-Security\JordanChatBot-main\Poppins\Poppins-BoldItalic.ttf")
    LabelBase.register(
        name="BPoppins", fn_regular="C:\Job-Security\JordanChatBot-main\Poppins\Poppins-BoldItalic.ttf")
    LabelBase.register(
       name="Tamil", fn_regular=r"C:\FarmHand-Edifice\FarmHand-App\fonts\NotoSansDevanagari-VariableFont_wdth,wght.ttf")
    CareerShieldApp().run()
except:
    from traceback import format_exc
    from kivy.app import App
    from kivy.uix.textinput import TextInput
    class BackupApp(App):
        def build(self):
            print(format_exc())
            return TextInput(text=str(format_exc()))
    BackupApp().run()    