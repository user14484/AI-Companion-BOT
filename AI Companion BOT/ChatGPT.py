import openai
import mtranslate
import logging

class ChatGPT:
    logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
    def __init__(self, api_key):
        openai.api_key = api_key

    def getAnswer(self, message, lang="ru", max_tokens=4000, temperature=0.5, engine_model="text-davinci-003"):
        try:
            # Считаем количество токенов
            num_tokens = len(list(message))
            # Если количество токенов превышает допустимое количество, то возращаем сообщение с ошибкой
            if(num_tokens > max_tokens):
                return mtranslate.translate("❌ You have exceeded the limit on the number of tokens. Please shorten your message.", lang, "auto")

            result = ""

            # Отправляем контекст на серверы OpenAI и получаем ответ
            response = openai.Completion.create(
                engine=engine_model,
                prompt=message,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
            result = response["choices"][0]["text"].strip()
                

            # Если бот вернул пустой ответ
            if(not result):
                result = "❌ Sorry, the bot didn't return the result.";

            # Возращаем полученный и переводим его на нужный нам язык текст
            return mtranslate.translate(result, lang, "auto")
        except Exception as e:
            logging.critical(f"{e}")
            return mtranslate.translate("❌ An unknown error has occurred, try again!", lang, "auto")

