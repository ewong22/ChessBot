import chess
from game_tree import Node, minimax


# Create a new chess board
board = chess.Board()
# Ask for 1 or 2 player
game_mode = int(input("Enter 1 for single player or 2 for two player"))

if game_mode == 2:
    while not board.is_checkmate() and not board.is_stalemate():
        # Print the chess board
        print(board, "\n")

        # Get the move from the user
        move = input("Enter your move: ")

        # Try to apply the move
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in board.legal_moves:
                board.push(chess_move)
            else:
                print("This move is not legal.")
        except:
            print("Invalid input. Please enter a move in UCI format (e.g., e2e4).")

    # Print the final board state
    print(board)

    # Check the game outcome
    if board.is_checkmate():
        print("Checkmate!")
        print("Winner: " + ("White" if board.turn else "Black"))
    else:
        print("Stalemate!")

elif game_mode == 1:
    choose_side = int(input("Type 0 for White and 1 for Black"))
    if choose_side == 0: 
        turn = True
    while not board.is_checkmate() and not board.is_stalemate():
        # Print the chess board
        print(board, "\n")
        if turn == True:
            while (turn):
                # Get the move from the user
                move = input("Enter your move: ")

                # Try to apply the move
                try:
                    chess_move = chess.Move.from_uci(move)
                    if chess_move in board.legal_moves:
                        board.push(chess_move)
                        turn = False
                    else:
                        print("This move is not legal.")
                except:
                    print("Invalid input. Please enter a move in UCI format (e.g., e2e4).")

        else:
            game = Node(board)
            evaluation, best_move = minimax(game, 5, float('-inf'), float('inf'), False)
            board.push(best_move)
            print("Bot's move: ", best_move)
            turn = True



    # Print the final board state
    print(board)

    # Check the game outcome
    if board.is_checkmate():
        print("Checkmate!")
        print("Winner: " + ("White" if board.turn else "Black"))
    else:
        print("Stalemate!")







    



