import chess 

class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []

    def add_child(self, move):
        new_board = self.board.copy()
        new_board.push(move)
        return Node(new_board, move, self)



def evaluate_node(node):
    if node.board.is_game_over():
        if node.board.is_checkmate():
            # If it's a checkmate, the player who is not to move won
            # We return a very high or very low score depending on the winner
            if node.board.turn == chess.WHITE:
                return float('-inf')  # Black won
            else:
                return float('inf')  # White won
        else:
            # It's a draw
            return 0
    board = node.board
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.symbol().upper()]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    mobility_score = 0
    if board.turn == chess.WHITE:
        mobility_score = len(list(board.legal_moves))
        board.turn = chess.BLACK
        mobility_score -= len(list(board.legal_moves))
        board.turn = chess.WHITE
    else:
        mobility_score = -len(list(board.legal_moves))
        board.turn = chess.WHITE
        mobility_score += len(list(board.legal_moves))
        board.turn = chess.BLACK
    score += mobility_score * 0.1

    # king safety
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    white_king_safety = -len(list(board.attackers(chess.BLACK, white_king_square))) * 0.5
    black_king_safety = -len(list(board.attackers(chess.WHITE, black_king_square))) * 0.5
    score += white_king_safety - black_king_safety

    return score


def minimax(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.board.is_game_over():
        return evaluate_node(node), node.move
    
    moves = list(node.board.legal_moves)
    moves.sort(key=lambda move: node.board.is_capture(move) or node.board.gives_check(move), reverse=True)

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        
        for move in moves:
            child = node.add_child(move)
            eval, _ = minimax(child, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            child = node.add_child(move)
            eval, _ = minimax(child, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
