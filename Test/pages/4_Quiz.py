import streamlit as st
import random

# Seitenkonfiguration
st.set_page_config(page_title="Wissensquiz", page_icon="🧠")

# Quiz-Daten
quiz_data = [
   {
       "frage": "Was ist die Hauptstadt von Deutschland?",
       "optionen": ["Berlin", "München", "Hamburg", "Frankfurt"],
       "antwort": "Berlin"
   },
   {
       "frage": "Welches Element hat das chemische Symbol 'O'?",
       "optionen": ["Gold", "Sauerstoff", "Osmium", "Silber"],
       "antwort": "Sauerstoff"
   },
   {
       "frage": "Wie viele Planeten hat unser Sonnensystem?",
       "optionen": ["7", "8", "9", "10"],
       "antwort": "8"
   },
   {
       "frage": "Welches ist das größte Säugetier der Welt?",
       "optionen": ["Afrikanischer Elefant", "Giraffe", "Blauwal", "Gorilla"],
       "antwort": "Blauwal"
   },
   {
       "frage": "In welchem Jahr fiel die Berliner Mauer?",
       "optionen": ["1987", "1989", "1991", "1993"],
       "antwort": "1989"
   }
]

def main():
   st.title("📚 Wissensquiz")
   st.write("Teste dein Allgemeinwissen mit diesem Quiz!")

   # Session State für Score und aktuelle Frage initialisieren
   if 'score' not in st.session_state:
       st.session_state.score = 0
   if 'current_question' not in st.session_state:
       st.session_state.current_question = 0
   if 'answers' not in st.session_state:
       st.session_state.answers = []
   if 'quiz_started' not in st.session_state:
       st.session_state.quiz_started = False
   if 'quiz_finished' not in st.session_state:
       st.session_state.quiz_finished = False
   if 'questions' not in st.session_state:
       # Kopiere die Fragen und mische sie
       st.session_state.questions = random.sample(quiz_data, len(quiz_data))

   # Quiz starten
   if not st.session_state.quiz_started and not st.session_state.quiz_finished:
       col1, col2, col3 = st.columns([1, 2, 1])
       with col2:
           if st.button("Quiz starten", use_container_width=True):
               st.session_state.quiz_started = True
               st.rerun()

   # Quiz durchführen
   if st.session_state.quiz_started and not st.session_state.quiz_finished:
       display_question()

   # Ergebnisse anzeigen
   if st.session_state.quiz_finished:
       display_results()

       if st.button("Quiz neu starten"):
           reset_quiz()
           st.rerun()

def display_question():
   current_q = st.session_state.current_question
   total_q = len(st.session_state.questions)

   # Fortschrittsbalken
   st.progress(current_q / total_q)
   st.write(f"Frage {current_q + 1} von {total_q}")

   # Aktuelle Frage anzeigen
   question = st.session_state.questions[current_q]
   st.subheader(question["frage"])

   # Antwortoptionen als Radio-Buttons
   user_answer = st.radio(
       "Wähle deine Antwort:",
       question["optionen"],
       key=f"q_{current_q}"
   )

   # Weiter-Button
   if st.button("Antwort bestätigen"):
       # Antwort überprüfen und speichern
       correct = user_answer == question["antwort"]
       if correct:
           st.session_state.score += 1

       st.session_state.answers.append({
           "frage": question["frage"],
           "user_antwort": user_answer,
           "korrekte_antwort": question["antwort"],
           "korrekt": correct
       })

       # Nächste Frage oder Quiz beenden
       if current_q < total_q - 1:
           st.session_state.current_question += 1
       else:
           st.session_state.quiz_finished = True

       st.rerun()

def display_results():
   total_questions = len(st.session_state.questions)
   score = st.session_state.score
   percentage = (score / total_questions) * 100

   st.title("Quiz abgeschlossen!")

   # Prozent-Score mit Fortschrittsbalken
   st.subheader(f"Dein Ergebnis: {score}/{total_questions} ({percentage:.1f}%)")
   st.progress(percentage/100)

   # Bewertung basierend auf Prozentsatz
   if percentage >= 80:
       st.success("Ausgezeichnet! Du hast ein hervorragendes Wissen gezeigt.")
   elif percentage >= 60:
       st.info("Gut gemacht! Du hast solide Kenntnisse.")
   elif percentage >= 40:
       st.warning("Du hast grundlegende Kenntnisse. Es gibt Raum für Verbesserungen.")
   else:
       st.error("Da ist noch Luft nach oben. Weiter lernen!")

   # Antworten überprüfen
   st.subheader("Deine Antworten")
   for i, answer in enumerate(st.session_state.answers):
       with st.expander(f"Frage {i+1}: {answer['frage']}"):
           if answer['korrekt']:
               st.success(f"Deine Antwort: {answer['user_antwort']} ✓")
           else:
               st.error(f"Deine Antwort: {answer['user_antwort']} ✗")
               st.info(f"Richtige Antwort: {answer['korrekte_antwort']}")

def reset_quiz():
   st.session_state.score = 0
   st.session_state.current_question = 0
   st.session_state.answers = []
   st.session_state.quiz_started = False
   st.session_state.quiz_finished = False
   st.session_state.questions = random.sample(quiz_data, len(quiz_data))

if __name__ == "__main__":
   main()