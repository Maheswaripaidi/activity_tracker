from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def summarize_text(sentences, top_n=3):
    if not sentences:
        return "No activity to summarize."

    #  Step 1: Clean sentences (remove noise)
    clean_sentences = [
        s for s in sentences
        if "Mouse click" not in s and "Keyboard activity" not in s
    ]

    if not clean_sentences:
        return "No meaningful activity found."

    #  Step 2: TF-IDF scoring
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(clean_sentences)

    scores = np.sum(X.toarray(), axis=1)

    # Rank sentences
    ranked = [
        sentence for _, sentence in sorted(
            zip(scores, clean_sentences), reverse=True
        )
    ]

    important_sentences = ranked[:top_n]

    #  Step 3: Extract meaning
    apps = []
    typing = []
    idle = []

    for line in important_sentences:
        if "Opened" in line:
            apps.append(line.replace("Opened ", "").strip())

        elif "typed" in line:
            typing.append(line.split("User typed:")[-1].strip())

        elif "idle" in line:
            idle.append(line)

    #  Step 4: Build human-like paragraph
    summary = "The user started a session "

    # Applications
    if apps:
        unique_apps = list(set(apps))
        summary += "and interacted with applications such as "
        summary += ", ".join(unique_apps[:3]) + ". "

    # Typing
    if typing:
        summary += "During the session, the user entered text including "
        summary += ", ".join(typing[:2]) + ". "

    # Idle
    if idle:
        summary += "There was also a period of inactivity observed. "

    # Final statement
    summary += "Overall, the session involved user interaction and navigation across applications."

    return " Activity Summary:\n\n" + summary