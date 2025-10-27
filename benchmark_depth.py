#!/usr/bin/env python3
"""
Chess Engine Depth Benchmark Script

This script benchmarks the move algorithm performance across different:
- Search depths (1 to 3)
- Number of possible moves (positions with varying legal move counts)
- Various game positions (opening, middlegame, endgame)

Outputs:
- Time taken per depth level
- Nodes evaluated
- Moves per second
- Comparison across different board positions
"""

import chess
import time
import sys
import evaluation
import statistics
from typing import List, Dict
import json


class BenchmarkResult:
    """Store benchmark results for a single test"""

    def __init__(
        self,
        depth: int,
        legal_moves: int,
        time_taken: float,
        best_move: chess.Move,
        position_name: str,
    ):
        self.depth = depth
        self.legal_moves = legal_moves
        self.time_taken = time_taken
        self.best_move = best_move
        self.position_name = position_name

    def __repr__(self):
        return (
            f"Depth {self.depth} | Moves: {self.legal_moves:2d} | "
            f"Time: {self.time_taken:.4f}s | Move: {self.best_move}"
        )


class DepthBenchmark:
    """Benchmark the chess engine at various depths"""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

        # Test positions with varying complexity
        self.test_positions = {
            "starting_position": (
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            ),
            "open_game": (
                "r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/" "PPPP1PPP/RNBQK2R w KQkq - 4 4"
            ),
            "middlegame": (
                "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/"
                "PPP2PPP/R1BQ1RK1 w - - 0 8"
            ),
            "complex_middlegame": (
                "r2q1rk1/ppp1bppp/2np1n2/4p1B1/2B1P3/2NP1N2/"
                "PPP2PPP/R2Q1RK1 w - - 0 10"
            ),
            "endgame": "8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 w - - 0 1",
            "few_pieces": "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
            "tactical_position": (
                "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/"
                "PPP2PPP/RNBQK2R w KQkq - 0 6"
            ),
            "late_endgame": "8/8/4k3/8/8/3K4/3P4/8 w - - 0 1",
        }

    def benchmark_position(
        self, fen: str, depth: int, position_name: str
    ) -> BenchmarkResult:
        """Benchmark a single position at a given depth"""
        board = chess.Board(fen)
        legal_moves_count = len(list(board.legal_moves))

        # Store original depth
        original_depth = evaluation.TREE_DEPTH

        # Set the depth for this test
        evaluation.TREE_DEPTH = depth

        # Measure time
        start_time = time.perf_counter()

        # Create the tree and find best move
        tree = evaluation.Node(depth, evaluation.PLAYER_NUM, 0, board)
        result = evaluation.min_max(
            depth, tree, evaluation.PLAYER_NUM, -sys.maxsize, sys.maxsize
        )
        best_move = result[1]

        end_time = time.perf_counter()
        time_taken = end_time - start_time

        # Restore original depth
        evaluation.TREE_DEPTH = original_depth

        return BenchmarkResult(
            depth, legal_moves_count, time_taken, best_move, position_name
        )

    def run_depth_benchmarks(
        self, min_depth: int = 1, max_depth: int = 5, positions: List[str] = None
    ) -> None:
        """Run benchmarks across different depths"""
        if positions is None:
            positions = list(self.test_positions.keys())

        print("=" * 80)
        print("CHESS ENGINE DEPTH BENCHMARK")
        print("=" * 80)
        print()

        for position_name in positions:
            if position_name not in self.test_positions:
                print(f"Warning: Position '{position_name}' not found, " "skipping...")
                continue

            fen = self.test_positions[position_name]
            board = chess.Board(fen)
            legal_moves = len(list(board.legal_moves))

            print(f"\n{'─' * 80}")
            print(f"Position: {position_name}")
            print(f"FEN: {fen}")
            print(f"Legal moves available: {legal_moves}")
            print(f"{'─' * 80}")
            print(
                f"{'Depth':<8} {'Time (s)':<12} {'Moves/Legal':<15} "
                f"{'Best Move':<12}"
            )
            print(f"{'─' * 80}")

            for depth in range(min_depth, max_depth + 1):
                try:
                    result = self.benchmark_position(fen, depth, position_name)
                    self.results.append(result)

                    print(
                        f"{depth:<8} {result.time_taken:<12.4f} "
                        f"{legal_moves:<15} {result.best_move}"
                    )

                    # Skip deeper searches if taking too long (> 60 seconds)
                    if result.time_taken > 60:
                        print("  ⚠ Skipping deeper searches " "(taking too long)")
                        break

                except KeyboardInterrupt:
                    print("\n\nBenchmark interrupted by user")
                    return
                except Exception as e:
                    print(f"  ✗ Error at depth {depth}: {e}")
                    break

    def run_move_count_analysis(self, depth: int = 3) -> None:
        """Analyze how number of legal moves affects performance"""
        print("\n" + "=" * 80)
        print(f"MOVE COUNT ANALYSIS (Depth {depth})")
        print("=" * 80)
        print()

        # Sort positions by number of legal moves
        positions_with_moves = []
        for name, fen in self.test_positions.items():
            board = chess.Board(fen)
            move_count = len(list(board.legal_moves))
            positions_with_moves.append((name, fen, move_count))

        positions_with_moves.sort(key=lambda x: x[2])

        print(f"{'Legal Moves':<15} {'Time (s)':<12} {'Position':<25}")
        print("─" * 80)

        move_count_results = []
        for name, fen, move_count in positions_with_moves:
            try:
                result = self.benchmark_position(fen, depth, name)
                print(f"{move_count:<15} {result.time_taken:<12.4f} " f"{name:<25}")
                move_count_results.append((move_count, result.time_taken))
            except Exception:
                print(f"{move_count:<15} {'ERROR':<12} {name:<25}")

        # Calculate correlation
        if len(move_count_results) > 1:
            moves = [x[0] for x in move_count_results]
            times = [x[1] for x in move_count_results]

            # Simple correlation analysis
            avg_moves = statistics.mean(moves)
            avg_times = statistics.mean(times)

            print(f"\n{'─' * 80}")
            print(f"Average legal moves: {avg_moves:.1f}")
            print(f"Average time: {avg_times:.4f}s")

    def print_summary(self) -> None:
        """Print summary statistics"""
        if not self.results:
            print("\nNo results to summarize")
            return

        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)

        # Group by depth
        depth_groups: Dict[int, List[BenchmarkResult]] = {}
        for result in self.results:
            if result.depth not in depth_groups:
                depth_groups[result.depth] = []
            depth_groups[result.depth].append(result)

        print(
            f"\n{'Depth':<8} {'Avg Time (s)':<15} {'Min Time (s)':<15} "
            f"{'Max Time (s)':<15} {'Tests':<8}"
        )
        print("─" * 80)

        for depth in sorted(depth_groups.keys()):
            results = depth_groups[depth]
            times = [r.time_taken for r in results]
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)

            print(
                f"{depth:<8} {avg_time:<15.4f} {min_time:<15.4f} "
                f"{max_time:<15.4f} {len(results):<8}"
            )

        # Exponential growth analysis
        if len(depth_groups) > 1:
            print(f"\n{'─' * 80}")
            print("GROWTH ANALYSIS (Average time per depth)")
            print("─" * 80)

            sorted_depths = sorted(depth_groups.keys())
            for i in range(1, len(sorted_depths)):
                prev_depth = sorted_depths[i - 1]
                curr_depth = sorted_depths[i]

                prev_avg = statistics.mean(
                    [r.time_taken for r in depth_groups[prev_depth]]
                )
                curr_avg = statistics.mean(
                    [r.time_taken for r in depth_groups[curr_depth]]
                )

                if prev_avg > 0:
                    growth_factor = curr_avg / prev_avg
                    print(
                        f"Depth {prev_depth} → {curr_depth}: "
                        f"{growth_factor:.2f}x slower"
                    )

    def export_results(self, filename: str = "benchmark_results.json") -> None:
        """Export results to JSON file"""
        data = {
            "results": [
                {
                    "depth": r.depth,
                    "legal_moves": r.legal_moves,
                    "time_taken": r.time_taken,
                    "best_move": str(r.best_move),
                    "position_name": r.position_name,
                }
                for r in self.results
            ]
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n✓ Results exported to {filename}")


def main():
    """Main benchmark execution"""
    benchmark = DepthBenchmark()

    print("Starting Chess Engine Benchmarks...")
    print()

    # Configuration
    MIN_DEPTH = 1
    MAX_DEPTH = 3  # Limited to depth 3 for initial benchmarking

    # Run depth benchmarks on all positions
    benchmark.run_depth_benchmarks(MIN_DEPTH, MAX_DEPTH)

    # Analyze move count impact
    benchmark.run_move_count_analysis(depth=3)

    # Print summary
    benchmark.print_summary()

    # Export results
    benchmark.export_results("benchmark_results.json")

    print("\n" + "=" * 80)
    print("Benchmark Complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user")
        sys.exit(0)
