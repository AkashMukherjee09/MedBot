from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
from chatterbot import ChatBot
from flask import Flask, render_template, request

app = Flask(__name__)

bot=ChatBot('MedBot',
            database='./MedBot.sqlite3',
            logic_adapters = [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.65,
                    'default_response': 'Sorry this information is not available. We will get back to you in 1 day.'
                }
            ],
            statement_comparison_function=levenshtein_distance,
            read_only=True
            )


bot.set_trainer(ChatterBotCorpusTrainer)
bot.train(
    "chatterbot.corpus.custom"
)


@app.route("/")
def chat():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    bot_response=str(bot.get_response(userText))
    bot_response=bot_response.replace(". ",".\n ")
    bot_response=bot_response.replace(" - ","\n")
    print(bot_response)
    if bot_response=="Sorry this information is not available.\n We will get back to you in 1 day.":
        '''con = sqlite3.connect('unanswered.db')
        con.execute('CREATE TABLE IF NOT EXISTS NEWQ(QUESTION CHAR(100));')
        con.execute('INSERT INTO NEWQ (QUESTION) VALUES(?)', (userText,))
        cursor = con.execute('SELECT * FROM NEWQ')
        for row in cursor:
            print(row[0])
        '''
        newFile=open('Chat/unanswered.txt','a')
        newFile.write(userText+'\n')
        print("file created")
        newFile.close()
    return bot_response


if __name__ == "__main__":
    app.run()
