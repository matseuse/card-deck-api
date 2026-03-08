from flask import Flask, request, jsonify
import random

app = Flask(__name__)
      
# Card Dec
PROPERTIES = [
    {
        "name": "Gamblers Feet",
        "notes": "Generate a number between 1 and 6. That is the amount of steps you take. Then roll again and repeat.",
        "duration": 20,
        "cost": "Flip if a coin if it's heads this has no effect and the curse is discarded",
        "weight": 1,
     },
     {
        "name": "Impenetrable Fog",
        "notes": "At each junction you walk past you must assign at least 1 number to each direction and roll a dice to decide which way you go.",
        "duration": 20,
        "cost": "Flip if a cion if it's tails this curse has no effect and is discarded",
        "weight": 1,
     },
    {
        "name": "Drained Brain",
        "notes": "The hides choose 3 questions in 3 categories that cannot be asked for the rest of the run",
        "duration": 0,
        "cost": "Discard your hand",
     },
    {
        "name": "Mediocre Travel Agent",
        "notes": "Go to a location the hider chooses within 400m of you. The seekers cannot currently be on transit. Go there and spend at least 5 minutes there before asking another question. Send at least 3 photos enjoying your holiday and procure an object as a souvenir. If this souvenir is lost before the end of the round the hider gets a 30 minute time bonus before asking another question.",
        "duration": 0,
        "cost": "Their holiday destination must be further from the hiders than thir current location",
        "weight": 1,
     },
     {
        "name": "Egg Partner",
        "notes": "Buy an egg. If you break it before the end of the round the hider gets a 45 minute bonus. Do this before asking another question. This question cannot be played during the endgame.",
        "duration": 0,
        "cost": "Discard 2 Cards",
        "weight": 1,
      },
      {
        "name": "Overflowing Chalice",
        "notes": "For the next 3 questions the hider may draw (not keep) an additional card.",
        "duration": 0,
        "cost": "Discard a Card",
        "weight": 1,
      },
      {
        "name": "Impressionable Consumer",
        "notes": "Before asking another question the seekers must enter a location or buy a product that they saw an advert for all in the real world and must be at least 30m from it's location.",
        "duration": 0,
        "cost": "The seekers' next question is free.",
        "weight": 1,
      },
      {
        "name": "Hidden Hangman",
        "notes": "Before asking another question or boarding transport the seekers must beat the hiders in a game of hangman. The hiders choose a 5 letter word and the game ends after the correct word is guessed or 7 incorrect letter guesses. The seekers cannot challenge the hider for 10 minutes after a loss. After 2 losses the seekers must wait 10 minutes and then the curse is cleared.",
        "duration": 0,
        "cost": "Discard 2 cards.",
        "weight": 1,
      },
      {
        "name": "Hide-And-Seek-Ception",
        "notes": "One seeker must hide 100m away and not in direct eyeshot in any direction. The other seekers must find them without help before asking another question.",
        "duration": 0,
        "cost": "The seeekers must be of transport at least 150m away from a station",
        "weight": 1,
      },
      {
        "name": "Gilded Inquiry",
        "notes": "The hiders secretly choose one question. If the seekers ask that question after this curse is played the question is automatically vetoed and the hider draws and keeps 3 extra cards.",
        "duration": 0,
        "cost": "The seekers' next question is free.",
        "weight": 1,
      },
      {
        "name": "Prosperous Home",
        "notes": "The hiders expand the radius of their hiding zone by 50%",
        "duration": 0,
        "cost": "Discard at least 20 minutes of time bonuses.",
        "weight": 1,
      },
      {
        "name": "5-Minute King",
        "notes": "Remove (mark as played) all the 5-minute bonuses from the deck for the rest of the round.",
        "duration": 0,
        "cost": "Discard two 5-minute bonuses.",
        "weight": 1,
      },
      {
        "name": "Soothsayer",
        "notes": "For the rest of the round the hiders may predict the next question straigt after the previous question is asked. If the hiders are right they earn triple rewards if they are wrong they earn no reward.",
        "duration": 0,
        "cost": "Discard a curse.",
        "weight": 1,
      },
      {
        "name": "Jammed Door",
        "notes": "Whenever the seekers want to pass through a doorway into a building, business, train, or other vehicle, they must first roll 2 dice. If they do not get a 7 or higher, they cannot enter that space (including through other doorways). Any given doorway can be re-attempted after 5 minutes.",
        "duration": 60,
        "cost": "Discard a Card",
        "weight": 1,
      },
      {
        "name": "Archaeologist",
        "notes": "The hiders send the seekers a photo of a building or structure whose age you can verify to within a century (don't send the seekers the age). The seekers must find a building or structure (whose age they can also verify) from the same century or earlier before asking another question. (Check with the hiders for if you've been successfull)",
        "duration": 0,
        "cost": "A standard photo of a building or structure",
        "weight": 1,
      },
      {
        "name": "Shrew Critic",
        "notes": "Without using the internet, the seekers must find a location that has at least a 4.3 star average rating on Google Maps before asking another question. If their guess was wrong, they must wait 10 minutes before guessing another location.",
        "duration": 0,
        "cost": "Seekers must be currently off transit within 150 metres of a location that has at least a 4.3 star average rating on Google Maps.",
        "weight": 1,
      },
      {
        "name": "Mind Meld",
        "notes": "On the count of three, any two seekers say any word at the same time. Assuming they're not the same word, they must wait two minutes, and both seekers say a new word that they believe to be the midpoint between the last two words. You may not say any words that have already been said or do anything at all to indicate what word you will say next. Seekers may not ask another question until they both say the same word.",
        "duration": 0,
        "cost": "Seekers must be currently off transit within 150 metres of a location that has at least a 4.3 star average rating on Google Maps.",
        "weight": 1,
      },
      {
        "name": "The Void",
        "notes": "For the next three questions that the seekers ask, roll a die. If you roll a 1, 2, 3, or 4, that question is automatically vetoed.",
        "duration": 0,
        "cost": "Discard a veto.",
        "weight": 1,
      },
      {
        "name": "The Cairn",
        "notes": "The hiders have one attempt to sack as many rocks on top of each other as they can in a freestanding tower. Each rock may only touch one other rock. Once you have added a rock to the tower, it may not be removed. Before adding another rock, the tower must stand for at least five seconds. If at any point, any rock other than the base rock touches the ground, your tower has fallen. Once the hiders' tower falls, the hiders tell the seekers how many rocks high their tower was when it last stood for five seconds. The seekers must then construct a rock tower of the same number of rocks, under the same parameters, before asking another question. If their tower fails, they must restart. The rocks must be found in nature, and both teams must disperse the rocks after building.",
        "duration": 0,
        "cost": "Build a rock tower.",
        "weight": 1,
      },
      
      {
        "name": "The Express Route",
        "notes": "Seekers cannot disembark any transit for the next 30 minutes, unless they've reached the end of a line.",
        "duration": 0,
        "cost": "Discard at least 15 minutes worth of time bonuses.",
        "weight": 1,
      },
      {
        "name": "The Zipped Lip",
        "notes": "Seekers can only communicate to one another through gestures and closed-mouth sounds for the next 30 minutes. They can speak to other people but cannot speak or write any message intended or another seeker.",
        "duration": 10,
        "cost": "Discard a power up (not a curse or time bonus)",
        "weight": 1,
      },
       {
        "name": "Bird Guide",
        "notes": "The hiders have one chance to film a bird for as long as possible, up to 5 minutes straight. If, at any point, the bird leaves the frame, your timer is stopped. The seekers must then film a bird for the same amount of time or longer before asking another question",
        "duration": 0,
        "cost": "Film a Bird",
        "weight": 1,
        },
       {
        "name": "The Plagued Word",
        "notes": "Asking a question creates a 2 kilometre radius where questions cannot be asked until this curse expires. ",
        "duration": 40,
        "cost": "Seekers must be at least 10km away from the hiders",
        "weight": 1,
        },
       {
        "name": "Tiny Home",
        "notes": "All time bonus cards held at the end of this round are worth 50% extra.",
        "duration": 0,
        "cost": "The radius of the hiding zone is halved. This curse cannot be played during the endgame.",
        "weight": 1,
      },
      {
        "name": "The Rewind",
        "notes": "You must ask your next question from the exact place you asked your last question.",
        "duration": 0,
        "cost": "The last question must have been asked during the end game.",
        "weight": 1,
      },
       {
        "name": "The Passenger Princess",
        "notes": "The hider selects one seeker to be the passenger princess. The other seeker is the driver. The passenger princess is not permitted to carry their own belongings, do any research, hold any maps, or discuss the game in any way. They may be involved in clearing curses if instructed to do so.",
        "duration": 20,
        "cost": "Discard 2 cards",
        "weight": 1,
      },
       {
        "name": "The Unguided Tourist",
        "notes": "The hiders send the seekers an unzoomed Google Street View image from a street within 500 feet of where they are now. The shot has to be parallel to the horizon and include at least one human-built structure other than a road. Without using the internet for research, they must find what the hiders sent them in real life before they can use transportation or ask another question. They must send a picture to the hider for verification",
        "duration": 0,
        "cost": "Seekers must be outside.",
        "weight": 1,
      },
      {
        "name": "The Queue",
        "notes": "Seekers may not ask another question until they've waited in line for at least two minutes. They may wait in different lines, but they cannot wait in the same line more than once. They may not let people cut in front of them in line, and lines must have at least two people when they enter them.",
        "duration": 0,
        "cost": "You must currently be in line somewhere",
        "weight": 1,
      },
      {
        "name": "12 minute time bonus",
        "notes": "",
        "duration": 12,
        "cost": "",
        "weight": 2,
      },
      {
        "name": "8 minute time bonus",
        "notes": "",
        "duration": 8,
        "cost": "",
        "weight": 3,
      },
      {
        "name": "6 minute time bonus",
        "notes": "",
        "duration": 6,
        "cost": "",
        "weight": 10,
      },
      {
        "name": "4 minute time bonus",
        "notes": "",
        "duration": 4,
        "cost": "",
        "weight": 1,
      },
      {
        "name": "8 minute time bonus",
        "notes": "",
        "duration": 8,
        "cost": "",
        "weight": 3,
      },
      {
        "name": "6 minute time bonus",
        "notes": "",
        "duration": 6,
        "cost": "",
        "weight": 10,
      },
      {
        "name": "2 minute time bonus",
        "notes": "",
        "duration": 2,
        "cost": "",
        "weight": 25,
      },
      {
        "name": "Veto",
        "notes": "The vetoed question cannot be re asked",
        "duration": 0,
        "cost": "",
        "weight": 4,
      },
      {
        "name": "Randomize",
        "notes": "Assign a number to each un asked question in the category of the asked question answer the randomly selected question instead.",
        "duration": 0,
        "cost": "",
        "weight": 4,
      },
      {
        "name": "Duplicate",
        "notes": "",
        "duration": 0,
        "cost": "",
        "weight": 2,
      },
      {
        "name": "Discard 1 Draw 2",
        "notes": "",
        "duration": 0,
        "cost": "",
        "weight": 4,
      },
      {
        "name": "Discard 2 Draw 3",
        "notes": "",
        "duration": 0,
        "cost": "",
        "weight": 4,
      },
      {
        "name": "Time Trap",
        "notes": "A time trap is placed on a station and builds a time bonus equal too a quarter of the length of time it has been there up to 20 minutes.",
        "duration": 0,
        "cost": "",
        "weight": 3
      },
      {
        "name": "Draw 1 Expand Maximum Hand Size by 1",
        "notes": "",
        "duration": 0,
        "cost": "",
        "weight": 2
      },
      {
        "name": "Move",
        "notes": "The hiders have 10 minutes too rehide in which the seekers are frozen",
        "duration": 10,
        "cost": "",
        "weight": 1
      },
]

deck = []
draw_index = 0
current_seed = None

def reset_game(seed):
    global deck, draw_index, current_seed
    random.seed(seed)
    deck = weighted_shuffle(PROPERTIES[:])
    draw_index = 0
    current_seed = seed
@app.route("/")
def home():
    return "Server is running. Use /draw or /reset for API calls."

@app.route("/draw", methods=["POST"])
def draw ():
    global draw_index, current_seed
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON provided"}), 400

    seed = data.get("seed")
    count = data.get("count", 1)
    
    if seed != current_seed:
        reset_game(seed)

    if draw_index >= len(deck):
        return jsonify({"status": "empty"})

    end_index = min(draw_index + count, len(deck))
    selected_cards = deck[draw_index:end_index]
    draw_index = end_index

    print(f"DEBUG: Sending to Sheet: {selected_cards}") # Add this
    return jsonify({
    "status": "ok",
    "cards": selected_cards,
    "remaining": len(deck) - draw_index
    })

    return jsonify({
        "status": "ok",
        "cards": selected_cards,
        "remaining": len(deck) - draw_index
    }) 
    
def reset_game(seed):
    global deck, draw_index, current_seed
    random.seed(seed)

    multiplied_deck = []
    for item in PROPERTIES:
        weight = int(item.get("weight", 1))
        for _ in range(weight):
            multiplied_deck.append(item.copy())
    random.shuffle(multiplied_deck)
    deck = multiplied_deck
    draw_index = 0
    current_seed = seed     

@app.route("/discard", methods=["POST"])
def discard():
    global deck, draw_index
    if draw_index > 0:
        deck.pop(draw_index - 1)
        draw_index -= 1
        return jsonify({"status": "discarded", "remaining": len(deck) - draw_index})
    return jsonify({"status": "error", "message": "No cards to discard"})                                 

@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json()
    seed = data.get("seed") if data else None 
    reset_game(seed)
    return jsonify({"status": "reset"})

def weighted_shuffle(items):
    weighted = []

    for item in items:
        w = item.get("weight", 1)
        r = random.random()
        key = r ** (1.0/max(w,0.001))
        weighted.append((key,item))

    weighted.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in weighted]  

@app.route("/add_to_deck", methods={"POST"})
def add_to_deck():
    global deck, draw_index
    data = request.get_json()
    card_name = data.get("name")
    template = next((p for p in PROPERTIES if p["name"] == card_name), None)
    if not template:
        return jsonify({"status": "error", "message": "Card not found in PROPERTIES"}),
    if draw_index >= len(deck):
        deck.append(template.copy())
    else:
        inster_at = random.randint(draw_index, len(deck))
        deck.insert(insert_at, template.copy())
    return jsonify({
        "status": "added",
        "card": card_name,
        "remaining": len(deck) - draw_index
    })            

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)