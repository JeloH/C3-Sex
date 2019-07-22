# Copyright 2017 Bo Shao. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import os
import re
import sys
import tensorflow as tf

from settings import PROJECT_ROOT
from ACA.chatbot.botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def bot_ui():
    """ 
        En las variables dir se ubican principalmente los datasets que se van a usar 
        para los entrenamientos y las reglas. 
        corp_dir -> Corpus de data para entrenar el chatbot.
        knbs_dir -> Corpus de entrenamiento con Jokes y Stories.
        res_dir -> Directorio resultado donde se guardan los resultados (Entrenamientos).
        rules_dir -> Directorio donde están ubicadas las reglas.
    """
    corp_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Corpus')
    knbs_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Variety')
    res_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Result')
    rules_dir = os.path.join(PROJECT_ROOT, 'ACA', 'Data', 'Rules')

    with tf.Session() as sess:
        predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                                 result_dir=res_dir, aiml_dir=rules_dir,
                                 result_file='basic')
        # This command UI has a single chat session only
        session_id = predictor.session_data.add_session()

        # print("Welcome to Chat with ChatLearner!")
        # print("Type exit and press enter to end the conversation.")
        # Waiting from standard input.
        sys.stdout.write("> ")
        sys.stdout.flush()
        question = sys.stdin.readline()
        while question:
            if question.strip() == 'exit':
                print("Bye Bye ~")
                break

            print(re.sub(r'_nl_|_np_', '\n', predictor.predict(session_id, question)).strip())
            print("> ", end="")
            sys.stdout.flush()
            question = sys.stdin.readline()

if __name__ == "__main__":
    bot_ui()
