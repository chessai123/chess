#!/usr/bin/env python3
"""
Quick comparison of all available implementations.
Shows side-by-side performance on a single position.
"""

import chess
import time
import sys
import os


def test_implementation(name, make_move_func, board, depth):
    """Test a single implementation"""
    import evaluation
    original_depth = evaluation.TREE_DEPTH
    evaluation.TREE_DEPTH = depth
    
    try:
        board_copy = board.copy()
        start = time.perf_counter()
        result = make_move_func(board_copy)
        elapsed = time.perf_counter() - start
        move = result.peek()
        return elapsed, str(move)
    finally:
        evaluation.TREE_DEPTH = original_depth


def main():
    print("="*60)
    print("QUICK PERFORMANCE COMPARISON")
    print("="*60)
    
    # Check Python version
    print(f"\nPython: {sys.version.split()[0]}")
    print(f"CPUs: {os.cpu_count()}")
    
    try:
        import sysconfig
        if sysconfig.get_config_var('Py_GIL_DISABLED'):
            print("Build: FREE-THREADED (no GIL) ✓")
        else:
            print("Build: Standard (with GIL)")
    except:
        pass
    
    # Test position
    board = chess.Board()
    depth = 3
    
    print(f"\nPosition: Starting position")
    print(f"Depth: {depth}")
    print(f"Legal moves: {len(list(board.legal_moves))}")
    print("\n" + "="*60)
    
    results = []
    
    # Test single-threaded
    print("\n[1] Testing: evaluation.py (single-threaded)")
    try:
        import evaluation
        time_st, move_st = test_implementation(
            "Single-threaded",
            evaluation.make_move,
            board,
            depth
        )
        results.append(("Single-threaded", time_st, move_st, 1.0))
        print(f"    Time: {time_st:.3f}s")
        print(f"    Move: {move_st}")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Test threaded
    print("\n[2] Testing: evaluation_threaded.py (threaded)")
    try:
        import evaluation_threaded
        
        # Set depth on the threaded module
        evaluation_threaded.TREE_DEPTH = depth
        
        board_copy = board.copy()
        start = time.perf_counter()
        result = evaluation_threaded.make_move(board_copy, max_workers=None)
        time_mt = time.perf_counter() - start
        move_mt = str(result.peek())
        
        speedup = time_st / time_mt if time_mt > 0 else 0
        results.append(("Threaded (auto)", time_mt, move_mt, speedup))
        print(f"    Time: {time_mt:.3f}s")
        print(f"    Move: {move_mt}")
        print(f"    Speedup: {speedup:.2f}x")
    except ImportError:
        print("    Not available (file not found)")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Test optimized
    print("\n[3] Testing: evaluation_optimized.py (optimized)")
    try:
        import evaluation_optimized
        
        # Set depth on the optimized module
        evaluation_optimized.TREE_DEPTH = depth
        
        board_copy = board.copy()
        start = time.perf_counter()
        result = evaluation_optimized.make_move(board_copy, max_workers=None)
        time_opt = time.perf_counter() - start
        move_opt = str(result.peek())
        
        speedup = time_st / time_opt if time_opt > 0 else 0
        results.append(("Optimized (auto)", time_opt, move_opt, speedup))
        print(f"    Time: {time_opt:.3f}s")
        print(f"    Move: {move_opt}")
        print(f"    Speedup: {speedup:.2f}x")
    except ImportError:
        print("    Not available (file not found)")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\n{'Implementation':<25} {'Time (s)':<12} {'Speedup':<10}")
    print("-"*60)
    
    for name, elapsed, move, speedup in results:
        print(f"{name:<25} {elapsed:<12.3f} {speedup:<10.2f}x")
    
    print("="*60)
    
    # Recommendation
    if len(results) > 1:
        best = min(results[1:], key=lambda x: x[1])
        print(f"\n✓ Best performer: {best[0]}")
        print(f"  {best[3]:.2f}x faster than single-threaded")
        
        if best[3] < 1.5:
            print("\n⚠ Limited speedup is expected for pure Python!")
            print("  See WHY_SLOW_THREADING.md for explanation.")
            print("  Consider multiprocessing for 4-8x speedup.")


if __name__ == "__main__":
    main()
