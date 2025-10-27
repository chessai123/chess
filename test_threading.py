#!/usr/bin/env python3
"""
Quick test to verify the multithreaded implementation works correctly.
"""

import sys
import chess


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import evaluation
        print("  ✓ evaluation.py imported")
    except ImportError as e:
        print(f"  ✗ Failed to import evaluation.py: {e}")
        return False
    
    try:
        import evaluation_threaded
        print("  ✓ evaluation_threaded.py imported")
    except ImportError as e:
        print(f"  ✗ Failed to import evaluation_threaded.py: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test that both implementations produce valid moves"""
    print("\nTesting basic functionality...")
    
    import evaluation
    import evaluation_threaded
    
    board = chess.Board()
    print(f"  Starting position: {board.fen()}")
    
    # Test single-threaded
    try:
        board_st = board.copy()
        original_depth = evaluation.TREE_DEPTH
        evaluation.TREE_DEPTH = 2  # Shallow for quick test
        result_st = evaluation.make_move(board_st)
        evaluation.TREE_DEPTH = original_depth
        move_st = result_st.peek()
        print(f"  ✓ Single-threaded: {move_st}")
    except Exception as e:
        print(f"  ✗ Single-threaded failed: {e}")
        return False
    
    # Test multithreaded
    try:
        board_mt = board.copy()
        original_depth = evaluation_threaded.TREE_DEPTH
        evaluation_threaded.TREE_DEPTH = 2  # Shallow for quick test
        result_mt = evaluation_threaded.make_move(board_mt, max_workers=2)
        evaluation_threaded.TREE_DEPTH = original_depth
        move_mt = result_mt.peek()
        print(f"  ✓ Multithreaded: {move_mt}")
    except Exception as e:
        print(f"  ✗ Multithreaded failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_free_threading():
    """Check if running free-threaded Python"""
    print("\nChecking Python configuration...")
    print(f"  Python version: {sys.version.split()[0]}")
    
    try:
        import sysconfig
        is_free_threaded = sysconfig.get_config_var('Py_GIL_DISABLED')
        if is_free_threaded:
            print("  ✓ Running FREE-THREADED build (no GIL)")
            print("    Multithreading will provide significant speedup!")
            return True
        else:
            print("  ⚠ Running STANDARD build (with GIL)")
            print("    Multithreading speedup will be limited")
            print("    For best performance, use: uv run --python 3.14t")
            return False
    except Exception as e:
        print(f"  ⚠ Could not determine threading mode: {e}")
        return False


def test_chess_library():
    """Test chess library functionality"""
    print("\nTesting chess library...")
    try:
        board = chess.Board()
        moves = list(board.legal_moves)
        print(f"  ✓ chess library working ({len(moves)} legal moves)")
        return True
    except Exception as e:
        print(f"  ✗ chess library error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("MULTITHREADED EVALUATION - QUICK TEST")
    print("="*60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_chess_library()
    all_passed &= test_basic_functionality()
    is_free_threaded = test_free_threading()
    
    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nNext steps:")
        print("1. Run full benchmarks: python benchmark_threading.py")
        if not is_free_threaded:
            print("2. For best performance, use: uv run --python 3.14t")
        print("3. Integrate into xboard_engine.py")
        print("4. Read THREADING_GUIDE.md for details")
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60)
        print("\nTroubleshooting:")
        print("1. Install dependencies: uv pip install chess")
        print("2. Check Python version: python --version")
        print("3. See THREADING_GUIDE.md for help")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
