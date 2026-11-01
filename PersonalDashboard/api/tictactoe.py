import random
def check_win(cards: list[dict]) -> str:
    board = [c["data"] if c["data"] in ["X", "O"] else "" for c in sorted(cards, key=lambda x: int(x["id"]))]
    
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            if board[combo[0]] == "O":
                return "player"
            elif board[combo[0]] == "X":
                return "computer"
                
    if "0" not in [c["data"] for c in cards]:
        return "tie"
        
    return "none"

def computer_decide(cards: list[dict]) -> dict:
    sorted_cards = sorted(cards, key=lambda x: int(x["id"]))
    board = [c["data"] if c["data"] in ["X", "O"] else "" for c in sorted_cards]
    empty_spots = [i for i in range(9) if board[i] == ""]
    if not empty_spots:
        return {}

    if random.random() < 0.3: # Minimax impossible chanigng to 70% impossible
        idx = random.choice(empty_spots)
        return {"id": str(idx), "data": "X"}

    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    def get_winner(b):
        for combo in wins:
            if b[combo[0]] == b[combo[1]] == b[combo[2]] != "":
                return b[combo[0]]
        if "" not in b: return "Tie"
        return None

    def minimax(b, depth, is_maximizing):
        result = get_winner(b)
        if result == "X": return 10 - depth
        if result == "O": return depth - 10
        if result == "Tie": return 0

        if is_maximizing:
            best = -float("inf")
            for i in range(9):
                if b[i] == "":
                    b[i] = "X"
                    score = minimax(b, depth + 1, False)
                    b[i] = ""
                    best = max(score, best)
            return best
        else:
            best = float("inf")
            for i in range(9):
                if b[i] == "":
                    b[i] = "O"
                    score = minimax(b, depth + 1, True)
                    b[i] = ""
                    best = min(score, best)
            return best

    best_score = -float("inf")
    best_move_idx = None
    
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move_idx = i
    if best_move_idx is not None:
        return {
            "id": str(best_move_idx),
            "data": "X"
        }
    
    return {}
