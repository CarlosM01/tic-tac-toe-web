from flask import Flask, jsonify, request, render_template
from game_logic import GameBoard, MinimaxAI

app = Flask(__name__)

# Inicializar el tablero y la IA
game_board = GameBoard()
ai = MinimaxAI(game_board)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    print(data)
    row, col = int(data['row']), int(data['col'])
    player = data['player']

    if game_board.make_move(row, col, player):
        winner = game_board.check_winner()
        if winner:
            return jsonify({'status': 'end', 'winner': winner})
        
        if player == 'X':
            ai_move = ai.best_move()
            print(ai_move)
            if ai_move:
                ai_row, ai_col = ai_move
                game_board.make_move(ai_row, ai_col, 'O')
                winner = game_board.check_winner()
                return jsonify({
                    'status': 'continue',
                    'ai_move': {'row': ai_row, 'col': ai_col},
                    'winner': winner if winner else None
                })
    
    return jsonify({'status': 'invalid'})

@app.route('/reset', methods=['POST'])
def reset():
    game_board.reset()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
