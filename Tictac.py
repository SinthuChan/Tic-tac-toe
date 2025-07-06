import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe – Sinthiya vs Aida 💖")
root.configure(bg="#fdf0f0")
root.resizable(False, False)

board = [" "] * 9
buttons = []

player_name = "Sinthiya"
ai_name = "Aida"

score = {player_name: 0, ai_name: 0}

def check_win(brd, player):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(brd[i] == brd[j] == brd[k] == player for i,j,k in wins)

def check_draw(brd):
    return all(cell != " " for cell in brd)

def minimax(brd, is_max):
    if check_win(brd, "O"):
        return 1
    if check_win(brd, "X"):
        return -1
    if check_draw(brd):
        return 0

    if is_max:
        best = -float("inf")
        for i in range(9):
            if brd[i] == " ":
                brd[i] = "O"
                score = minimax(brd, False)
                brd[i] = " "
                best = max(best, score)
        return best
    else:
        best = float("inf")
        for i in range(9):
            if brd[i] == " ":
                brd[i] = "X"
                score = minimax(brd, True)
                brd[i] = " "
                best = min(score, best)
        return best

def ai_move():
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def on_click(index):
    if board[index] == " ":
        board[index] = "X"
        buttons[index]["text"] = "X"
        buttons[index]["fg"] = "#4361ee"
        buttons[index]["state"] = "disabled"

        if check_win(board, "X"):
            score[player_name] += 1
            end_game(f"🎉 {player_name} wins! 💌 Aida is proud of you! 💖")
            return
        elif check_draw(board):
            end_game("🤝 It's a draw!")
            return

        root.after(500, ai_turn)

def ai_turn():
    move = ai_move()
    if move is not None:
        board[move] = "O"
        buttons[move]["text"] = "O"
        buttons[move]["fg"] = "#ff006e"
        buttons[move]["state"] = "disabled"

        if check_win(board, "O"):
            score[ai_name] += 1
            end_game(f"💖 {ai_name} (AI) wins!")
        elif check_draw(board):
            end_game("🤝 It's a draw!")

def end_game(msg):
    for b in buttons:
        b["state"] = "disabled"
    show_fireworks(msg)
    messagebox.showinfo("Game Over", msg)
    update_scoreboard()

def restart_game():
    global board
    board = [" "] * 9
    for b in buttons:
        b["text"] = ""
        b["state"] = "normal"
    update_scoreboard()
    title_label.config(text=f"{player_name} vs {ai_name} 💖", fg="#c9184a")

def show_fireworks(msg):
    # Simple flashing text effect
    def flash(count=0):
        if count % 2 == 0:
            title_label.config(text=msg, fg="#ff006e")
        else:
            title_label.config(text=msg, fg="#c9184a")
        if count < 6:
            root.after(300, flash, count+1)
        else:
            title_label.config(text=f"{player_name} vs {ai_name} 💖", fg="#c9184a")
    flash()

def update_scoreboard():
    score_label.config(text=f"Score — {player_name}: {score[player_name]}  |  {ai_name}: {score[ai_name]}")

# UI Layout
title_label = tk.Label(root, text=f"{player_name} vs {ai_name} 💖", font=("Helvetica", 20, "bold"), bg="#fdf0f0", fg="#c9184a")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

for i in range(9):
    btn = tk.Button(root, text="", font=("Helvetica", 32), width=5, height=2,
                    command=lambda i=i: on_click(i), bg="#fff0f3", relief="groove", borderwidth=3)
    btn.grid(row=(i//3)+1, column=i%3, padx=5, pady=5)
    buttons.append(btn)

score_label = tk.Label(root, text=f"Score — {player_name}: 0  |  {ai_name}: 0", font=("Helvetica", 12), bg="#fdf0f0", fg="#720026")
score_label.grid(row=4, column=0, columnspan=3)

reset_btn = tk.Button(root, text="🔁 Restart Game", font=("Helvetica", 12, "bold"),
                      bg="#ffc8dd", fg="#6a0572", command=restart_game)
reset_btn.grid(row=5, column=0, columnspan=3, pady=10)

credit_label = tk.Label(root, text="Developed by Sinthiya", font=("Helvetica", 10, "italic"), bg="#fdf0f0", fg="#555555")
credit_label.grid(row=6, column=0, columnspan=3, pady=(0,10))

root.mainloop()
      
