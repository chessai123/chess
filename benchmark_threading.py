"""
Benchmark script to test multithreaded evaluation performance.
Tests performance on Python 3.14 free-threaded build.
Can find optimal depth based on time threshold.
"""

import chess
import time
import sys
from typing import Dict, Optional, List
import os

# Try to import multithreaded version - check which one exists
try:
    import evaluation_optimized as multithreaded
    implementation_name = "evaluation_optimized"
except ImportError:
    try:
        import evaluation_threaded as multithreaded
        implementation_name = "evaluation_threaded"
    except ImportError:
        print("Error: No multithreaded implementation found!")
        print("Expected: evaluation_threaded.py or evaluation_optimized.py")
        sys.exit(1)


def benchmark_position(board: chess.Board, depth: int, name: str) -> Dict:
    """
    Benchmark a specific position with multithreaded implementation.
    
    Args:
        board: Chess position to evaluate
        depth: Search depth
        name: Name of the test position
    
    Returns:
        Dictionary with benchmark results
    """
    results = {
        'name': name,
        'fen': board.fen(),
        'depth': depth,
        'legal_moves': len(list(board.legal_moves))
    }
    
    print(f"\n{'='*60}")
    print(f"Position: {name}")
    print(f"FEN: {board.fen()}")
    print(f"Legal moves: {results['legal_moves']}")
    print(f"Search depth: {depth}")
    print(f"{'='*60}")
    
    # Save original depth
    original_depth_mt = multithreaded.TREE_DEPTH
    
    try:
        # Set depth
        multithreaded.TREE_DEPTH = depth
        
        # Multithreaded benchmark (auto workers)
        print("\n[1/2] Running multithreaded evaluation (auto workers)...")
        board_copy = board.copy()
        start = time.perf_counter()
        result_mt = multithreaded.make_move(board_copy, max_workers=None)
        mt_time = time.perf_counter() - start
        mt_move = result_mt.peek()
        
        results['multithreaded_auto'] = {
            'time': mt_time,
            'move': str(mt_move),
            'workers': 'auto'
        }
        print(f"  Time: {mt_time:.3f}s")
        print(f"  Best move: {mt_move}")
        
        # Multithreaded benchmark (max workers)
        print("\n[2/2] Running multithreaded evaluation (max workers)...")
        max_workers = os.cpu_count() or 4
        board_copy = board.copy()
        start = time.perf_counter()
        result_mt_max = multithreaded.make_move(
            board_copy, max_workers=max_workers
        )
        mt_max_time = time.perf_counter() - start
        mt_max_move = result_mt_max.peek()
        
        results['multithreaded_max'] = {
            'time': mt_max_time,
            'move': str(mt_max_move),
            'workers': max_workers
        }
        print(f"  Time: {mt_max_time:.3f}s")
        print(f"  Best move: {mt_max_move}")
        print(f"  Workers: {max_workers}")
        
        # Summary
        print(f"\n{'='*60}")
        print("RESULTS:")
        print(f"  Multithreaded (auto): {mt_time:.3f}s")
        print(f"  Multithreaded (max): {mt_max_time:.3f}s")
        if mt_time > mt_max_time:
            improvement = ((mt_time - mt_max_time) / mt_time) * 100
            print(f"  Max workers is {improvement:.1f}% faster")
        elif mt_max_time > mt_time:
            improvement = ((mt_max_time - mt_time) / mt_max_time) * 100
            print(f"  Auto workers is {improvement:.1f}% faster")
        else:
            print(f"  Both configurations perform equally")
        print(f"{'='*60}")
        
    finally:
        # Restore original depth
        multithreaded.TREE_DEPTH = original_depth_mt
    
    return results


def find_optimal_depth(
    board: chess.Board,
    max_time: float = 1.0,
    max_workers: Optional[int] = None,
    start_depth: int = 1,
    max_depth: int = 10
) -> Dict:
    """
    Find the optimal search depth that stays under the time threshold.
    
    Args:
        board: Chess position to evaluate
        max_time: Maximum time in seconds
        max_workers: Number of worker threads (None = auto)
        start_depth: Starting depth to test
        max_depth: Maximum depth to test
    
    Returns:
        Dictionary with optimal depth and timing information
    """
    print(f"\n{'='*60}")
    print(f"FINDING OPTIMAL DEPTH")
    print(f"Time threshold: {max_time:.3f}s")
    print(f"Position: {board.fen()}")
    print(f"Legal moves: {len(list(board.legal_moves))}")
    print(f"{'='*60}")
    
    original_depth = multithreaded.TREE_DEPTH
    optimal_depth = start_depth
    last_time = 0
    
    try:
        for depth in range(start_depth, max_depth + 1):
            multithreaded.TREE_DEPTH = depth
            
            print(f"\n[Depth {depth}] Testing...")
            board_copy = board.copy()
            start = time.perf_counter()
            result = multithreaded.make_move(board_copy, max_workers=max_workers)
            elapsed = time.perf_counter() - start
            move = result.peek()
            
            print(f"  Time: {elapsed:.3f}s")
            print(f"  Move: {move}")
            
            if elapsed <= max_time:
                optimal_depth = depth
                last_time = elapsed
                print(f"  ✓ Under threshold")
            else:
                print(f"  ✗ Exceeded threshold by {elapsed - max_time:.3f}s")
                break
        
        print(f"\n{'='*60}")
        print(f"OPTIMAL DEPTH: {optimal_depth}")
        print(f"Time at optimal depth: {last_time:.3f}s")
        print(f"Time budget remaining: {max_time - last_time:.3f}s")
        print(f"{'='*60}")
        
    finally:
        multithreaded.TREE_DEPTH = original_depth
    
    return {
        'optimal_depth': optimal_depth,
        'time': last_time,
        'max_time': max_time,
        'workers': max_workers
    }


def main():
    """Run benchmarks on various positions"""
    print("="*60)
    print("CHESS ENGINE THREADING BENCHMARK")
    print("Python 3.14 Free-Threading Performance Test")
    print("="*60)
    
    # Show which implementation we're testing
    print(f"\nMultithreaded implementation: {implementation_name}")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"CPU count: {os.cpu_count()}")
    
    # Check if running free-threaded build
    try:
        import sysconfig
        is_free_threaded = sysconfig.get_config_var('Py_GIL_DISABLED')
        if is_free_threaded:
            print("✓ Running Python 3.14 FREE-THREADED build (no GIL)")
        else:
            print("⚠ Running standard Python build (with GIL)")
            print("  For best results, use: uv run --python 3.14t")
    except Exception as e:
        print(f"⚠ Could not determine threading mode: {e}")
    
    # Check command line arguments for mode
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "find-depth":
            # Find optimal depth mode
            max_time = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
            fen = sys.argv[3] if len(sys.argv) > 3 else chess.STARTING_FEN
            
            board = chess.Board(fen)
            result = find_optimal_depth(
                board,
                max_time=max_time,
                max_workers=None
            )
            print(f"\n✓ Use TREE_DEPTH = {result['optimal_depth']} "
                  f"for ~{result['time']:.3f}s per move")
            return result
        
        elif mode == "depth-range":
            # Test a range of depths
            min_d = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            max_d = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            fen = sys.argv[4] if len(sys.argv) > 4 else chess.STARTING_FEN
            
            print(f"\nTesting depths {min_d} to {max_d}")
            board = chess.Board(fen)
            
            for depth in range(min_d, max_d + 1):
                result = benchmark_position(board, depth, f"Depth {depth}")
                print()
            
            return
    
    # Default: Standard benchmark mode
    
    # Test positions with categories
    test_positions = [
        {
            'name': 'Starting Position',
            'category': 'opening',
            'fen': chess.STARTING_FEN,
            'depth': 3
        },
        {
            'name': 'Middlegame',
            'category': 'middlegame',
            'fen': 'r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4',
            'depth': 3
        },
        {
            'name': 'Complex Position',
            'category': 'middlegame',
            'fen': 'r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 0 8',
            'depth': 3
        },
        {
            'name': 'Endgame',
            'category': 'endgame',
            'fen': '8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 w - - 99 50',
            'depth': 4
        },
    ]
    
    # Filter positions if specified via command line
    # Usage: python benchmark_threading.py positions opening
    # Usage: python benchmark_threading.py positions middlegame,endgame
    if len(sys.argv) > 1 and sys.argv[1] == "positions":
        if len(sys.argv) > 2:
            categories = sys.argv[2].lower().split(',')
            test_positions = [
                p for p in test_positions
                if p['category'] in categories
            ]
            print(f"\n→ Testing only: {', '.join(categories)}")
        else:
            # Show available categories
            cats = sorted(set(p['category'] for p in test_positions))
            print(f"\nAvailable position categories: {', '.join(cats)}")
            print("\nUsage: python benchmark_threading.py positions <category>")
            print("  category: opening, middlegame, endgame")
            print("  or combine: middlegame,endgame")
            return
    
    if not test_positions:
        print("No positions match the specified categories")
        return
    
    all_results = []
    
    # Run benchmarks
    for test in test_positions:
        board = chess.Board(test['fen'])
        result = benchmark_position(board, test['depth'], test['name'])
        all_results.append(result)
        time.sleep(0.5)  # Brief pause between tests
    
    # Final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"\n{'Position':<20} {'Depth':<6} {'Auto (s)':<12} "
          f"{'Max (s)':<12}")
    print("-"*60)
    
    for r in all_results:
        auto_time = r['multithreaded_auto']['time']
        max_time = r['multithreaded_max']['time']
        name = r['name']
        depth = r['depth']
        print(f"{name:<20} {depth:<6} {auto_time:<12.3f} "
              f"{max_time:<12.3f}")
    
    # Calculate average times
    avg_auto = sum(r['multithreaded_auto']['time'] 
                   for r in all_results) / len(all_results)
    avg_max = sum(r['multithreaded_max']['time'] 
                  for r in all_results) / len(all_results)
    print("-"*60)
    print(f"{'Average Time:':<20} {'':<6} {avg_auto:<12.3f} "
          f"{avg_max:<12.3f}")
    print("="*60)
    
    # Recommendations
    print("\nRECOMMENDATIONS:")
    print(f"✓ Implementation: {implementation_name}.py")
    print(f"  Average time (auto workers): {avg_auto:.3f}s per position")
    print(f"  Average time (max workers): {avg_max:.3f}s per position")
    
    if avg_auto < avg_max:
        improvement = ((avg_max - avg_auto) / avg_max) * 100
        print(f"\n  → Auto worker selection is {improvement:.1f}% faster")
        print("    Recommendation: Use max_workers=None (auto)")
    elif avg_max < avg_auto:
        improvement = ((avg_auto - avg_max) / avg_auto) * 100
        print(f"\n  → Max workers is {improvement:.1f}% faster")
        print(f"    Recommendation: Use max_workers={os.cpu_count()}")
    else:
        print("\n  → Both configurations perform equally")
    
    return all_results


def print_usage():
    """Print usage information"""
    print("\nUSAGE:")
    print("  # Standard benchmark (all positions)")
    print("  python benchmark_threading.py")
    print()
    print("  # Test specific position types")
    print("  python benchmark_threading.py positions opening")
    print("  python benchmark_threading.py positions middlegame")
    print("  python benchmark_threading.py positions endgame")
    print("  python benchmark_threading.py positions middlegame,endgame")
    print()
    print("  # Find optimal depth for time threshold")
    print("  python benchmark_threading.py find-depth <max_seconds> [fen]")
    print("  Example: python benchmark_threading.py find-depth 1.0")
    print()
    print("  # Test a range of depths on one position")
    print("  python benchmark_threading.py depth-range <min> <max> [fen]")
    print("  Example: python benchmark_threading.py depth-range 1 5")
    print()
    print("POSITION CATEGORIES:")
    print("  opening     - Starting positions")
    print("  middlegame  - Complex tactical positions")
    print("  endgame     - Endgame positions")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        print_usage()
    else:
        main()
