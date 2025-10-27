"""
Optimized multithreaded evaluation for Python 3.14+ free-threaded builds.
This version reduces Python object overhead for better parallelization.
"""

import config
import fenparser
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional
import chess


TREE_DEPTH = 3
PLAYER_NUM = 1


def make_move(
    board: chess.Board,
    max_workers: Optional[int] = None,
    depth: Optional[int] = None
) -> chess.Board:
    """
    Evaluate the best move using optimized parallel minimax.
    
    Args:
        board: Chess board position
        max_workers: Number of worker threads (None = auto)
        depth: Search depth (None = use TREE_DEPTH global)
    
    Returns:
        Board with best move applied
    """
    search_depth = depth if depth is not None else TREE_DEPTH
    move = find_best_move(board, search_depth, PLAYER_NUM, max_workers)
    board.push(move)
    return board


def calculate_score_for_piece(piece: str, lowercase: bool, row: int, col: int) -> int:
    """Calculate the score for a piece (optimized to reduce lookups)"""
    piece_upper = piece.upper()
    pst_pos = (config.board_length * row) + col
    
    # Get values once
    piece_val = config.piece[piece_upper]
    pst_val = config.pst[piece_upper][-(pst_pos + 1)]  # Reversed index
    
    if lowercase:
        return piece_val + pst_val
    else:
        return -(piece_val + pst_val)


def evaluate_board_score(board: chess.Board) -> int:
    """Calculate board score (cached FEN parsing)"""
    fen = fenparser.FenParser(board.fen()).parse()
    score = 0
    
    # Unrolled loop for better performance
    for row in range(8):
        row_data = fen[row]
        for col in range(8):
            piece = row_data[col]
            if piece == ' ':
                continue
            
            is_lowercase = piece.islower()
            piece_upper = piece.upper()
            pst_pos = (config.board_length * row) + col
            
            piece_val = config.piece.get(piece_upper, 0)
            pst_val = config.pst.get(piece_upper, [0] * 64)[-(pst_pos + 1)]
            
            if is_lowercase:
                score += piece_val + pst_val
            else:
                score -= piece_val + pst_val
    
    return score


def minimax_recursive(
    board: chess.Board,
    depth: int,
    player: int,
    alpha: int,
    beta: int
) -> int:
    """
    Optimized minimax without creating Node objects.
    Reduces Python object overhead significantly.
    """
    if depth == 0:
        return evaluate_board_score(board)
    
    legal_moves = list(board.legal_moves)
    
    if not legal_moves:
        # Game over
        if board.is_checkmate():
            return -999999 if player > 0 else 999999
        return 0  # Stalemate
    
    if player > 0:  # Maximizer
        max_eval = alpha
        for move in legal_moves:
            board.push(move)
            eval_score = minimax_recursive(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            if eval_score > max_eval:
                max_eval = eval_score
            alpha = max(alpha, eval_score)
            
            if beta <= alpha:
                break  # Beta cutoff
        
        return max_eval
    else:  # Minimizer
        min_eval = beta
        for move in legal_moves:
            board.push(move)
            eval_score = minimax_recursive(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            if eval_score < min_eval:
                min_eval = eval_score
            beta = min(beta, eval_score)
            
            if beta <= alpha:
                break  # Alpha cutoff
        
        return min_eval


def evaluate_single_move(
    board_fen: str,
    move_uci: str,
    depth: int,
    player: int
) -> Tuple[int, str]:
    """
    Evaluate a single move independently (for parallel execution).
    Uses FEN string to avoid sharing board objects.
    """
    # Create fresh board from FEN (no shared state)
    board = chess.Board(board_fen)
    move = chess.Move.from_uci(move_uci)
    
    # Make the move
    board.push(move)
    
    # Evaluate the resulting position
    score = minimax_recursive(
        board,
        depth - 1,
        -player,
        -sys.maxsize,
        sys.maxsize
    )
    
    return (score, move_uci)


def find_best_move(
    board: chess.Board,
    depth: int,
    player: int,
    max_workers: Optional[int] = None
) -> chess.Move:
    """
    Find best move using parallel evaluation.
    Optimized to reduce Python object overhead.
    """
    legal_moves = list(board.legal_moves)
    
    if not legal_moves:
        return None
    
    if len(legal_moves) == 1:
        return legal_moves[0]
    
    # For very few moves or shallow depth, use single-threaded
    if len(legal_moves) <= 3 or depth <= 1:
        best_score = -sys.maxsize if player > 0 else sys.maxsize
        best_move = legal_moves[0]
        
        for move in legal_moves:
            board.push(move)
            score = minimax_recursive(board, depth - 1, -player, -sys.maxsize, sys.maxsize)
            board.pop()
            
            if (player > 0 and score > best_score) or (player < 0 and score < best_score):
                best_score = score
                best_move = move
        
        return best_move
    
    # Parallel evaluation - use FEN strings to avoid shared objects
    board_fen = board.fen()
    move_ucis = [move.uci() for move in legal_moves]
    
    # Limit workers to number of moves or CPU count
    import os
    cpu_count = os.cpu_count() or 4
    if max_workers is None:
        max_workers = min(len(legal_moves), cpu_count)
    
    best_score = -sys.maxsize if player > 0 else sys.maxsize
    best_move_uci = move_ucis[0]
    
    # Use ThreadPoolExecutor for parallel evaluation
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all move evaluations
        futures = {
            executor.submit(evaluate_single_move, board_fen, move_uci, depth, player): move_uci
            for move_uci in move_ucis
        }
        
        # Collect results
        for future in as_completed(futures):
            try:
                score, move_uci = future.result()
                
                if player > 0:  # Maximizer
                    if score > best_score:
                        best_score = score
                        best_move_uci = move_uci
                else:  # Minimizer
                    if score < best_score:
                        best_score = score
                        best_move_uci = move_uci
            except Exception as exc:
                print(f"Move evaluation failed: {exc}", file=sys.stderr)
    
    return chess.Move.from_uci(best_move_uci)


# Single-threaded version for comparison
def make_move_single_threaded(board: chess.Board) -> chess.Board:
    """Single-threaded version using optimized minimax"""
    best_score = -sys.maxsize
    best_move = None
    
    for move in board.legal_moves:
        board.push(move)
        score = minimax_recursive(board, TREE_DEPTH - 1, -PLAYER_NUM, -sys.maxsize, sys.maxsize)
        board.pop()
        
        if score > best_score:
            best_score = score
            best_move = move
    
    if best_move:
        board.push(best_move)
    
    return board


if __name__ == "__main__":
    import time
    
    # Quick benchmark
    board = chess.Board()
    
    print("Testing optimized implementation...")
    print(f"Position: {board.fen()}")
    
    # Multithreaded
    start = time.perf_counter()
    result = make_move(board.copy(), max_workers=None)
    mt_time = time.perf_counter() - start
    print(f"Multithreaded: {mt_time:.3f}s - Move: {result.peek()}")
    
    # Single-threaded
    start = time.perf_counter()
    result_st = make_move_single_threaded(board.copy())
    st_time = time.perf_counter() - start
    print(f"Single-threaded: {st_time:.3f}s - Move: {result_st.peek()}")
    
    speedup = st_time / mt_time
    print(f"Speedup: {speedup:.2f}x")
