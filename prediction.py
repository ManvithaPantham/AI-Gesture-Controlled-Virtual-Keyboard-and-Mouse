class PredictionEngine:

    def __init__(self):

        self.words = [
            "hello", "help", "helmet", "hi", "house",
            "gesture", "keyboard", "python", "project",
            "computer", "camera", "mouse", "monitor",
            "screen", "engineering", "college",
            "student", "artificial", "intelligence",
            "machine", "learning", "vision", "opencv",
            "mediapipe", "typing", "virtual",
            "application", "software", "developer",
            "resume", "internship", "company",
            "windows", "technology", "science",
            "chatgpt", "coding", "programming",
            "algorithm", "system", "future"
        ]

    # ----------------------------------

    def predict(self, text):

        if len(text.strip()) == 0:
            return []

        current = text.split()[-1].lower()

        suggestions = []

        for word in self.words:

            if word.startswith(current):

                suggestions.append(word)

            if len(suggestions) == 3:
                break

        return suggestions