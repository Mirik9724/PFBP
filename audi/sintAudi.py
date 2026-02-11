import pyttsx3

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for v in voices:
            if "Russian" in v.name or "ru" in v.id.lower():
                self.engine.setProperty('voice', v.id)
                break
        self.engine.setProperty('rate', 180)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    import asyncio

    async def main():
        speaker = Voice()
        speaker.say("Ехали тюлени на мопеде, попивая чай")

    asyncio.run(main())
