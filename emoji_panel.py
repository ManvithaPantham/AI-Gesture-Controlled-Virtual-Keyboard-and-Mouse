class EmojiPanel:

    def __init__(self):

        self.emojis = [
            "😀",
            "😂",
            "😍",
            "😎",
            "👍",
            "❤️",
            "🔥",
            "🎉",
            "🙏",
            "💻"
        ]

    # --------------------------------------

    def get_emojis(self):

        return self.emojis

    # --------------------------------------

    def add_emoji(self, typed_text, emoji):

        return typed_text + emoji