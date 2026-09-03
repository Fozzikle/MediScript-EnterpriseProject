import genanki
import uuid

# Define the model
model_id = int(str(uuid.uuid4().int)[:9])
my_model = genanki.Model(
  model_id,
  'HSC Chemistry Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Tags'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br><i>Tags: {{Tags}}</i>',
    },
  ]
)

# Define the deck
deck_id = int(str(uuid.uuid4().int)[:9])
my_deck = genanki.Deck(
  deck_id,
  'HSC Chemistry: Modules 5–8 (In-Depth Flashcards)'
)

# Add sample notes
cards = [
  {
    "question": "What is the difference between static and dynamic equilibrium?",
    "answer": "Static: no movement of particles. Dynamic: forward and reverse reactions continue at equal rates with no net change in concentrations.",
    "tags": "Module5::StaticDynamicEquilibrium::CH12-12"
  },
  {
    "question": "How does temperature affect the equilibrium of an exothermic reaction?",
    "answer": "Increased temperature shifts equilibrium to the left (towards reactants), according to Le Chatelier’s principle.",
    "tags": "Module5::LeChateliersPrinciple::CH12-12"
  },
  {
    "question": "Write the general Keq expression for aA + bB ⇌ cC + dD.",
    "answer": "Keq = ([C]^c [D]^d) / ([A]^a [B]^b)",
    "tags": "Module5::EquilibriumConstant::CH12-12"
  },
  {
    "question": "How did Aboriginal and Torres Strait Islander Peoples use solubility equilibria?",
    "answer": "They leached toxins from cycad fruit in water—an application of solubility equilibrium to shift toxic compounds out of food.",
    "tags": "Module5::SolutionEquilibria::CH12-12"
  },
  {
    "question": "Compare Arrhenius and Brønsted–Lowry acid/base definitions.",
    "answer": "Arrhenius: acids release H+, bases release OH−. Brønsted–Lowry: acids donate protons, bases accept protons.",
    "tags": "Module6::AcidBaseTheories::CH12-13"
  },
]

for card in cards:
  note = genanki.Note(
    model=my_model,
    fields=[card["question"], card["answer"], card["tags"]],
    tags=card["tags"].split("::")
  )
  my_deck.add_note(note)

# Export to APKG
genanki.Package(my_deck).write_to_file("HSC_Chemistry_Modules_5-8.apkg")
print("Anki deck created: HSC_Chemistry_Modules_5-8.apkg")
