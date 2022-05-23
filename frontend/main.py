import json

import pygame
import sys
from api.admin import api_start_game
from api.game import api_get_current_stage_questions
from api.game import api_get_game_leaderboard
from api.game import api_get_questions_amount
from api.game import websocket_all_participants_answered
from api.game import websocket_get_game_current_stage
from api.game import websocket_get_game_participants
from api.game import api_move_to_next_stage
from api.user import api_answer_question, api_join_game, api_create_new_user
from api.utils import get_game_id
from api.utils import is_current_user_admin
from components.text_block import TextBlock
from components.answer_button import AnswerButton
from components.text_input import TextInput
from api.admin import api_create_new_game
from api.user import api_create_new_admin_user
from logic.question_object import Question_Object
from configs.colors import Color


class GameState:
    menu = 0
    game = 1
    game_over = 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.logo = pygame.image.load("./assets/game_logo.png")
        self.question_height = 100
        self.answer_height = 50
        self.surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.mouse_handlers = []
        self.input_handlers = []
        self.objects = []
        self.questions_editor_inputs = []
        self.answer_objects = []
        self.current_question = None
        self.current_stage = 0
        self.score = 0
        self.state = GameState.game
        self.questions = []
        self.websockets = []

        self.show_welcome_screen()

    def update(self):
        for item in self.objects:
            item.update()

        for item in self.answer_objects:
            item.update()

    def draw(self):
        for item in self.objects:
            item.draw(self.surface)

        for item in self.answer_objects:
            item.draw(self.surface)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    event_button_num = None
                    if hasattr(event, "button"):
                        event_button_num = event.button

                    handler(event.type, event.pos, event_button_num)

            elif event.type == pygame.KEYDOWN:
                for handler in self.input_handlers:
                    handler(event)

    def addTextBlock(self, x, y, w, h, text):
        self.objects.append(TextBlock(x, y, w, h, text))

    def addImage(self, x, y, w, h, image):
        image = pygame.transform.scale(image, (w, h))
        self.surface.blit(image, (x, y, w, h))

    def addTextInput(self, x, y, w, h, placeholder=''):
        text_input = TextInput(x, y, w, h, placeholder=placeholder)
        self.objects.append(text_input)
        self.mouse_handlers.append(text_input.handle_mouse_down)
        self.input_handlers.append(text_input.handle_key_down_event)
        return text_input

    def addSimpleButton(self, x, y, w, h, text, onclick_func):
        button = AnswerButton(x, y, w, h, text, onclick_func)
        self.objects.append(button)
        self.mouse_handlers.append(button.handleMouseEvent)

    def addAnswerButton(self, x, y, w, h, text, onclick_func, is_it_correct):
        button = AnswerButton(x, y, w, h, text, onclick_func, is_it_correct)
        self.answer_objects.append(button)
        self.mouse_handlers.append(button.handleMouseEvent)

    def check_if_all_participants_answered_and_move_to_game_over(self, ws, message):
        all_participants_answered = json.loads(message)
        self.addTextBlock(150, 210, 400, 25, "WAITING FOR OTHER PLAYERS")

        if all_participants_answered:
            self.move_to_game_over_screen()

    def move_to_game_over_screen(self):
        for specific_websocket in self.websockets:
            specific_websocket.close()

        self.state = GameState.game_over
        self.cleanScreen()
        self.addTextBlock(
            50,
            70,
            600,
            50,
            f"GAME OVER - USER LEADERBOARD"
        )

        participants = api_get_game_leaderboard()

        for index, participant in enumerate(participants):
            self.addTextBlock(
                50,
                (index + 2) * 70,
                600,
                50,
                f"USER: {participant['username']} - SCORE: {participant['score']}"
            )

    def cleanScreen(self):
        del self.answer_objects[:]
        del self.objects[:]
        del self.mouse_handlers[:]

    def answer_question(self, question, answer):
        self.cleanScreen()
        api_answer_question(question, answer)
        game_id = get_game_id()
        all_participants_answered_websocket = websocket_all_participants_answered(
            game_id,
            self.check_if_all_participants_answered_and_move_to_next_question
        )
        self.websockets.append(all_participants_answered_websocket)

    def check_if_all_participants_answered_and_move_to_next_question(self, ws, message):
        all_participants_answered = json.loads(message)
        self.addTextBlock(150, 210, 400, 25, "WAITING FOR OTHER PLAYERS")

        if all_participants_answered:
            self.move_to_next_question()

    def move_to_next_question(self):
        for specific_websocket in self.websockets:
            specific_websocket.close()

        self.cleanScreen()
        del self.answer_objects[:]
        del self.mouse_handlers[:]

        questions_amount = api_get_questions_amount()
        is_admin = is_current_user_admin()
        self.current_stage += 1

        if is_admin:
            if self.current_stage == 1:
                api_start_game()
            else:
                api_move_to_next_stage()

        if self.current_stage > questions_amount:
            game_id = get_game_id()
            self.cleanScreen()
            all_participants_answered_websocket = websocket_all_participants_answered(
                game_id,
                self.check_if_all_participants_answered_and_move_to_game_over
            )
            self.websockets.append(all_participants_answered_websocket)
            return

        self.current_question = api_get_current_stage_questions()
        self.addTextBlock(50, 70, 700, self.question_height, self.current_question['question'])

        answers = self.current_question['answers']

        for index, answer in enumerate(answers):
            is_it_correct = self.current_question['correct_answer'] == index

            self.addAnswerButton(
                x=50,
                y=self.question_height+80+index*(self.answer_height+10),
                w=700,
                h=self.answer_height,
                text=answer,
                onclick_func=lambda: self.answer_question(
                    self.current_question['question'],
                    3 - index
                ),
                is_it_correct=is_it_correct
            )

    def join_game(self):
        input_objects = self.get_input_objects()
        username = input_objects[0].get_text()
        api_create_new_user(username)

        game_id = input_objects[1].get_text()
        api_join_game(game_id)

        self.move_to_waiting_screen()

    def move_to_join_existing_game_screen(self):
        self.cleanScreen()
        self.addTextBlock(150, 70, 300, 25, "Please enter USERNAME:")
        self.addTextInput(150, 140, 300, 20, "TYPE HERE")
        self.addTextBlock(150, 210, 300, 25, "Please enter GAME-ID:")
        self.addTextInput(150, 280, 300, 20, "TYPE HERE")

        self.addSimpleButton(150, 400, 200, 50, "JOIN GAME NOW", self.join_game)

    def show_game_participants_from_websocket(self, ws, message):
        users_list = json.loads(message)
        for index, participant in enumerate(users_list):
            username = participant['username']
            if index < 3:
                self.addTextBlock(50 + 250*index, 150, 200, 100, f"#{(index+1)}:{username}")
            else:
                self.addTextBlock(50 + 250*index, 350, 200, 100, f"#{(index+1)}:{username}")

    def check_current_stage_and_start_game(self, ws, message):
        current_stage = int(json.loads(message))
        if current_stage == 0:
            return
        else:
            self.start_game()

    def start_game(self):
        for specific_websocket in self.websockets:
            specific_websocket.close()

        self.move_to_next_question()

    def move_to_waiting_screen(self):
        self.cleanScreen()

        game_id = get_game_id()
        self.addTextBlock(50, 70, 720, 50, f"Welcome to Shir's Kahoot game! - {game_id}")

        participants_ws = websocket_get_game_participants(game_id=game_id, on_message_func=self.show_game_participants_from_websocket)
        self.websockets.append(participants_ws)

        is_admin = is_current_user_admin()
        if is_admin:
            self.addSimpleButton(550, 500, 170, 100, "START GAME", self.start_game)
        else:
            stage_websocket = websocket_get_game_current_stage(game_id=game_id, on_message_func=self.check_current_stage_and_start_game)
            self.websockets.append(stage_websocket)

    def add_question_to_editor(self):
        questions_amount = len(self.questions_editor_inputs) + 1
        question_height_const = questions_amount * 200
        question_text = self.addTextInput(150, question_height_const, 350, 20, "TYPE QUESTION HERE")
        first_answer = self.addTextInput(150, question_height_const + 30, 350, 20, "TYPE FIRST ANSWER")
        second_answer = self.addTextInput(150, question_height_const + 60, 350, 20, "TYPE SECOND ANSWER")
        third_answer = self.addTextInput(150, question_height_const + 90, 350, 20, "TYPE THIRD ANSWER")
        fourth_answer = self.addTextInput(150, question_height_const + 120, 350, 20, "TYPE FOURTH ANSWER")
        correct_answer = self.addTextInput(150, question_height_const + 150, 350, 20, "CORRECT ANSWER NUM")

        # Adding specific question instances to questions_editor_inputs list
        self.questions_editor_inputs.append(
            {
                'text': question_text,
                'first_answer': first_answer,
                'second_answer': second_answer,
                'third_answer': third_answer,
                'fourth_answer': fourth_answer,
                'correct_answer': correct_answer,
            }
        )

    def get_input_objects(self):
        return [
            input_object
            for input_object
            in self.objects
            if type(input_object) == TextInput
        ]

    def finish_writing_questions(self):
        input_objects = self.get_input_objects()
        username = input_objects[0].get_text()

        api_create_new_admin_user(username=username)

        for question_input in self.questions_editor_inputs:
            new_question = Question_Object(
                question_input['text'].get_text(),
                (
                    question_input['first_answer'].get_text(),
                    question_input['second_answer'].get_text(),
                    question_input['third_answer'].get_text(),
                    question_input['fourth_answer'].get_text(),
                ),
                int(question_input['correct_answer'].get_text())
            )

            self.questions.append(new_question)

        questions_dict = [
            question.to_dict()
            for question
            in self.questions
        ]

        api_create_new_game(questions=questions_dict)

        del self.questions_editor_inputs[:]

        self.move_to_waiting_screen()

    def move_to_create_new_game_screen(self):
        self.cleanScreen()

        self.addSimpleButton(150, 50, 200, 50, "Add new question", self.add_question_to_editor)
        self.addSimpleButton(450, 50, 200, 50, "Finish & Start", self.finish_writing_questions)
        self.addTextBlock(150, 120, 300, 25, "Please enter USERNAME:")
        self.addTextInput(150, 150, 300, 20, "TYPE HERE")

        self.mouse_handlers.append(self.scroll_down)


    def show_welcome_screen(self):
        self.addTextBlock(150, 70, 300, 25, "Welcome to Triviara!")
        self.addSimpleButton(150, 170, 250, 50, "Join an existing game", self.move_to_join_existing_game_screen)
        self.addSimpleButton(150, 300, 250, 50, "Create new game", self.move_to_create_new_game_screen)

    def is_screen_out_of_upper_bound(self):
        is_item_in_upper_bounds = [
            item.y > 300
            for item
            in self.objects
        ]

        return not any(is_item_in_upper_bounds)

    def is_screen_out_of_lower_bound(self):
        is_item_in_upper_bounds = [
            item.y < 300
            for item
            in self.objects
        ]

        return not any(is_item_in_upper_bounds)

    def scroll_down(self, event_type, mouse_pos, event_button):
        if event_type == pygame.MOUSEBUTTONUP:
            for item in self.objects:
                if event_button == 5 and not self.is_screen_out_of_upper_bound():
                    item.scrollUp(20)

                if event_button == 4 and not self.is_screen_out_of_lower_bound():
                    item.scrollDown(20)

    def run(self):
        while True:
            self.surface.fill(Color.WHITE)
            self.addImage(0, 0, 100, 100, self.logo)
            self.handleEvents()
            self.draw()
            self.update()
            pygame.display.update()
            # self.clock.tick(60)


Game1 = Game()


Game1.run()
