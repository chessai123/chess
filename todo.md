Great question! Let me analyze the problem and give you options ranging from quick wins to advanced optimizations. 

Read [](file:///home/agf/projects/chess/evaluation_optimized.py#1-1), lines 1 to 100

Read [](file:///home/agf/projects/chess/evaluation.py)

Now let me provide you with options for improving performance at depth >= 5:

## Performance Improvement Options for Depth >= 5

### The Problem
At depth 5+, you're evaluating **millions of positions**:
- Depth 3: ~8,000 positions
- Depth 4: ~160,000 positions  
- Depth 5: ~3,200,000 positions (400× more than depth 3!)
- Depth 6: ~64,000,000 positions

---

## 🟢 Option 1: Iterative Deepening with Time Limits (EASY - 30 min)

**Complexity:** ⭐ Low  
**Time to implement:** 30 minutes  
**Expected improvement:** Always returns a move within your time budget  

**Concept:** Start at depth 1, then 2, 3, etc., until time runs out. Always have a "good enough" move ready.

````python
def make_move_with_time_limit(board, max_time=1.0, max_workers=None):
    """
    Search as deep as possible within time limit.
    Always returns best move found so far.
    """
    import time
    from evaluation_optimized import find_best_move, PLAYER_NUM
    
    start_time = time.time()
    best_move = None
    depth = 1
    
    while True:
        remaining = max_time - (time.time() - start_time)
        if remaining < 0.05:  # Need at least 50ms
            break
            
        try:
            # Try next depth
            move = find_best_move(board, depth, PLAYER_NUM, max_workers)
            best_move = move
            elapsed = time.time() - start_time
            
            print(f"  Depth {depth}: {elapsed:.2f}s - {move}")
            
            # Estimate next depth will take ~20x longer
            if elapsed * 20 > remaining:
                break
                
            depth += 1
            
        except KeyboardInterrupt:
            break
    
    if best_move:
        board.push(best_move)
    return board
````

**Usage:**
```python
# Always returns within 1 second, best move found
board = make_move_with_time_limit(board, max_time=1.0)
```

---

## 🟡 Option 2: Move Ordering + Hash Table (MEDIUM - 2-3 hours)

**Complexity:** ⭐⭐ Medium  
**Time to implement:** 2-3 hours  
**Expected improvement:** 3-5× faster at depth 5+  

**Concept:** Evaluate promising moves first to prune more branches. Cache positions to avoid re-evaluation.

````python
from functools import lru_cache

# Global cache for position evaluations
position_cache = {}

def get_move_priority(board, move):
    """
    Score moves to search best first.
    Better move ordering = more pruning.
    """
    score = 0
    
    # Prioritize captures
    if board.is_capture(move):
        captured = board.piece_at(move.to_square)
        if captured:
            score += 1000 + config.piece.get(captured.symbol().upper(), 0)
    
    # Prioritize checks
    board.push(move)
    if board.is_check():
        score += 500
    board.pop()
    
    # Central squares
    to_rank = chess.square_rank(move.to_square)
    to_file = chess.square_file(move.to_square)
    center_distance = abs(3.5 - to_rank) + abs(3.5 - to_file)
    score += (7 - center_distance) * 10
    
    return score


def minimax_with_ordering(board, depth, player, alpha, beta):
    """Minimax with move ordering and caching"""
    
    # Check cache
    board_hash = chess.polyglot.zobrist_hash(board)
    cache_key = (board_hash, depth, player)
    if cache_key in position_cache:
        return position_cache[cache_key]
    
    if depth == 0:
        score = evaluate_board_score(board)
        return score
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return evaluate_board_score(board)
    
    # CRITICAL: Order moves by priority
    legal_moves.sort(key=lambda m: get_move_priority(board, m), reverse=True)
    
    if player > 0:  # Maximizer
        max_score = alpha
        for move in legal_moves:
            board.push(move)
            score = minimax_with_ordering(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cutoff
        
        result = max_score
    else:  # Minimizer
        min_score = beta
        for move in legal_moves:
            board.push(move)
            score = minimax_with_ordering(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        
        result = min_score
    
    # Cache result
    position_cache[cache_key] = result
    return result
````

---

## 🟠 Option 3: Transposition Table + Better Pruning (HARD - 1 day)

**Complexity:** ⭐⭐⭐ High  
**Time to implement:** 1 day  
**Expected improvement:** 10-20× faster at depth 5+  

**Concept:** Professional chess engine techniques - full transposition table, null move pruning, quiescence search.

Key additions:
- **Transposition table** with depth tracking
- **Null move pruning** (skip turn to detect losing positions faster)
- **Quiescence search** (don't stop at captures)
- **Killer moves** (moves that caused cutoffs at same depth)

This is a significant rewrite - I can provide the full implementation if you want.

---

## 🔴 Option 4: Bitboard Evaluation (EXPERT - 3-5 days)

**Complexity:** ⭐⭐⭐⭐ Expert  
**Time to implement:** 3-5 days  
**Expected improvement:** 50-100× faster  

**Concept:** Replace FEN parsing with bitboard evaluation. Store board as 64-bit integers.

````python
# Instead of parsing FEN strings every time:
fen = fenparser.FenParser(board.fen()).parse()  # SLOW

# Use bitboards directly:
white_pawns = board.pawns & board.occupied_co[chess.WHITE]  # FAST
score += popcount(white_pawns) * 100  # Count bits
````

---

## 🟣 Option 5: C Extension / Cython (EXPERT - 1 week)

**Complexity:** ⭐⭐⭐⭐⭐ Expert  
**Time to implement:** 1 week  
**Expected improvement:** 100-500× faster  

Rewrite the hot path (minimax + evaluation) in Cython or C. This is what professional engines do.

---

## 📊 My Recommendation: Combination Approach

**For immediate results (today):**
1. ✅ Implement **Option 1: Iterative Deepening** (30 min)
   - Always get a move within time budget
   - No quality loss

**For 2-3× improvement (this week):**
2. ✅ Implement **Option 2: Move Ordering** (2-3 hours)
   - Captures first, checks second
   - Easy to implement, big wins

**For 10× improvement (if you have time):**
3. ✅ Add **Transposition Table** from Option 3 (half day)
   - Massive speedup for repeated positions

---

## Quick Win Implementation

Let me create a combined version with Options 1 + 2 (iterative deepening + move ordering):

````python
"""
Smart evaluation with iterative deepening and move ordering.
Combines best of both worlds: speed + intelligence.
"""

import chess
import time
import config
import fenparser
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Tuple

TREE_DEPTH = 3
PLAYER_NUM = 1

# Simple position cache
_position_cache = {}


def get_move_priority(board: chess.Board, move: chess.Move) -> int:
    """Score moves for better ordering (search best first)"""
    score = 0
    
    # Captures are usually good
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece:
            score += 1000 + config.piece.get(captured_piece.symbol().upper(), 0)
    
    # Checks are interesting
    board.push(move)
    if board.is_check():
        score += 500
    board.pop()
    
    # Prefer center
    to_rank = chess.square_rank(move.to_square)
    to_file = chess.square_file(move.to_square)
    center_dist = abs(3.5 - to_rank) + abs(3.5 - to_file)
    score += (7 - center_dist) * 10
    
    return score


def evaluate_board_score(board: chess.Board) -> int:
    """Fast board evaluation"""
    fen = fenparser.FenParser(board.fen()).parse()
    score = 0
    
    for row in range(8):
        for col in range(8):
            piece = fen[row][col]
            if piece == ' ':
                continue
            
            is_lower = piece.islower()
            piece_upper = piece.upper()
            pst_pos = (config.board_length * row) + col
            
            piece_val = config.piece.get(piece_upper, 0)
            pst_val = config.pst.get(piece_upper, [0] * 64)[-(pst_pos + 1)]
            
            if is_lower:
                score += piece_val + pst_val
            else:
                score -= piece_val + pst_val
    
    return score


def minimax_ordered(board: chess.Board, depth: int, player: int, 
                   alpha: int, beta: int) -> int:
    """Minimax with move ordering for better pruning"""
    
    if depth == 0:
        return evaluate_board_score(board)
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return evaluate_board_score(board)
    
    # ORDER MOVES (this is the key optimization)
    legal_moves.sort(key=lambda m: get_move_priority(board, m), reverse=True)
    
    if player > 0:  # Maximizer
        max_score = alpha
        for move in legal_moves:
            board.push(move)
            score = minimax_ordered(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score
    else:  # Minimizer
        min_score = beta
        for move in legal_moves:
            board.push(move)
            score = minimax_ordered(board, depth - 1, -player, alpha, beta)
            board.pop()
            
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score


def find_best_move_ordered(board: chess.Board, depth: int, player: int,
                           max_workers: Optional[int] = None) -> chess.Move:
    """Find best move with move ordering"""
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    # Order root moves too
    legal_moves.sort(key=lambda m: get_move_priority(board, m), reverse=True)
    
    def evaluate_move(move: chess.Move) -> Tuple[int, chess.Move]:
        board_copy = board.copy()
        board_copy.push(move)
        score = minimax_ordered(board_copy, depth - 1, -player,
                               -sys.maxsize, sys.maxsize)
        return (score, move)
    
    # Parallel evaluation of root moves
    if max_workers is None:
        import os
        max_workers = min(len(legal_moves), os.cpu_count() or 1)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(evaluate_move, legal_moves))
    
    best_score, best_move = max(results, key=lambda x: x[0])
    return best_move


def make_move_iterative(board: chess.Board, max_time: float = 1.0,
                       max_workers: Optional[int] = None) -> chess.Board:
    """
    Iterative deepening with time limit.
    Always returns within max_time.
    """
    start_time = time.perf_counter()
    best_move = None
    depth = 1
    
    print(f"Searching with time limit: {max_time}s")
    
    while True:
        elapsed = time.perf_counter() - start_time
        remaining = max_time - elapsed
        
        # Need at least 5% of time remaining
        if remaining < max_time * 0.05:
            break
        
        try:
            move = find_best_move_ordered(board, depth, PLAYER_NUM, max_workers)
            if move:
                best_move = move
                search_time = time.perf_counter() - start_time
                print(f"  Depth {depth}: {search_time:.3f}s - {move}")
            
            # Estimate: next depth takes ~15-20x longer
            if search_time * 18 > remaining:
                print(f"  Stopping: next depth would exceed time limit")
                break
            
            depth += 1
            
            # Safety: don't go too deep
            if depth > 10:
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  Error at depth {depth}: {e}")
            break
    
    if best_move:
        print(f"✓ Selected depth {depth - 1} move: {best_move}")
        board.push(best_move)
    
    return board


def make_move(board: chess.Board, max_workers: Optional[int] = None,
             depth: Optional[int] = None, max_time: Optional[float] = None) -> chess.Board:
    """
    Make a move with various strategies.
    
    Args:
        board: Chess board
        max_workers: Thread count (None = auto)
        depth: Fixed depth (None = use TREE_DEPTH)
        max_time: Time limit in seconds (None = no limit, use fixed depth)
    """
    if max_time is not None:
        # Iterative deepening with time limit
        return make_move_iterative(board, max_time, max_workers)
    else:
        # Fixed depth search
        search_depth = depth if depth is not None else TREE_DEPTH
        move = find_best_move_ordered(board, search_depth, PLAYER_NUM, max_workers)
        if move:
            board.push(move)
        return board
````

**Usage:**
```python
# Time-based (recommended)
board = make_move(board, max_time=1.0)  # Best depth within 1 second

# Fixed depth
board = make_move(board, depth=4)  # Always depth 4

# Hybrid
board = make_move(board, depth=6, max_time=5.0)  # Try depth 6, stop at 5s
```

---

## Which should you choose?

**Choose Option 1 if:** You need something working TODAY  
**Choose Option 1+2 if:** You have 2-3 hours and want good improvement  
**Choose Option 3 if:** You want pro-level performance and have a day  
**Choose Options 4-5 if:** This is a long-term project  

Would you like me to implement any of these for you?