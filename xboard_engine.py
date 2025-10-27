#!/usr/bin/env python3
"""
XBoard/CECP Protocol Handler for AlfaGeir Chess Engine

This module implements the Chess Engine Communication Protocol (XBoard/WinBoard)
allowing the AlfaGeir engine to communicate with XBoard-compatible GUIs.

Phase 1: Basic Protocol Implementation
- Unbuffered I/O handling
- Core commands: xboard, protover, new, quit, force, go
- Move input/output in coordinate notation
- Basic game loop and state management

Phase 3: Time Management
- Time controls via level, time, otim commands
- Move now command (?)
- Time-based search termination

Phase 4: Polish
- Thinking output (post/nopost)
- Result reporting
- Draw handling
- Improved error handling
"""

import sys
import time
import chess
import evaluation


class XBoardEngine:
    """XBoard protocol handler for AlfaGeir chess engine"""
    
    def __init__(self):
        """Initialize the engine state"""
        self.board = chess.Board()
        self.force_mode = False  # If True, engine doesn't think
        self.engine_color = chess.BLACK  # Color engine is playing
        self.search_depth = evaluation.TREE_DEPTH
        self.xboard_mode = False
        self.debug = False  # Enable debug output
        
        # Time management (Phase 3)
        self.my_time = None  # My remaining time in centiseconds
        self.opp_time = None  # Opponent's remaining time in centiseconds
        self.moves_per_session = 0  # Moves per time control (0 = all moves)
        self.base_time = 0  # Base time in minutes
        self.increment = 0  # Increment per move in seconds
        self.move_now = False  # Flag to interrupt search
        
        # Thinking output (Phase 4)
        self.post_mode = False  # Show thinking
        self.result_sent = False  # Track if result was sent
        
    def log(self, message):
        """Log debug messages (only visible when debug is True)"""
        if self.debug:
            print(f"# DEBUG: {message}", flush=True)
    
    def send_command(self, command):
        """Send a command to the GUI (with proper flushing)"""
        print(command, flush=True)
    
    def handle_xboard(self):
        """Enter xboard mode"""
        self.xboard_mode = True
        self.log("Entered XBoard mode")
    
    def handle_protover(self, version):
        """Handle protocol version negotiation"""
        if version == "2":
            # Announce our features
            features = [
                "ping=1",
                "setboard=1",
                "playother=0",
                "san=0",
                "usermove=1",
                "time=1",
                "draw=0",
                "sigint=0",
                "sigterm=0",
                "reuse=1",
                "analyze=0",
                "myname=\"AlfaGeir\"",
                "variants=\"normal\"",
                "colors=0",
                "ics=0",
                "name=0",
                "pause=0",
                "done=1"
            ]
            
            for feature in features:
                self.send_command(f"feature {feature}")
        
        self.log(f"Protocol version {version} negotiated")
    
    def handle_new(self):
        """Start a new game"""
        self.board = chess.Board()
        self.force_mode = False
        self.engine_color = chess.BLACK  # Engine plays black by default
        self.result_sent = False
        self.move_now = False
        # Don't reset time controls - they persist across games
        self.log("New game started, engine plays BLACK")
    
    def handle_quit(self):
        """Exit the engine"""
        self.log("Quitting engine")
        # Flush output before exiting
        sys.stdout.flush()
        sys.stderr.flush()
        # Use a clean exit that closes streams properly
        raise SystemExit(0)
    
    def handle_force(self):
        """Enter force mode (stop engine from thinking)"""
        self.force_mode = True
        self.log("Entered force mode")
    
    def handle_go(self):
        """Start playing for the current side to move"""
        self.force_mode = False
        self.engine_color = self.board.turn
        self.log(f"Engine starts playing {self.engine_color}")
        # Make a move immediately
        self.make_engine_move()
    
    def handle_usermove(self, move_str):
        """Handle a move from the opponent"""
        try:
            # Parse move in coordinate notation (e.g., "e2e4" or "e7e8q" for promotion)
            move = chess.Move.from_uci(move_str)
            
            # Check if move is legal
            if move not in self.board.legal_moves:
                self.send_command(f"Illegal move: {move_str}")
                return
            
            # Make the move
            self.board.push(move)
            self.log(f"Opponent played: {move_str}")
            
            # If not in force mode, think and respond
            if not self.force_mode:
                self.make_engine_move()
        
        except ValueError:
            self.send_command(f"Error (invalid move format): {move_str}")
    
    def handle_setboard(self, fen):
        """Set the board position from FEN string"""
        try:
            self.board = chess.Board(fen)
            self.log(f"Board set to FEN: {fen}")
        except ValueError:
            self.send_command(f"Error (invalid FEN): {fen}")
    
    def handle_ping(self, number):
        """Respond to ping with pong"""
        self.send_command(f"pong {number}")
    
    def handle_time(self, centiseconds):
        """Set engine's remaining time (in centiseconds)"""
        try:
            self.my_time = int(centiseconds)
            self.log(f"My time: {self.my_time} centiseconds")
        except ValueError:
            self.log(f"Invalid time value: {centiseconds}")
    
    def handle_otim(self, centiseconds):
        """Set opponent's remaining time (in centiseconds)"""
        try:
            self.opp_time = int(centiseconds)
            self.log(f"Opponent time: {self.opp_time} centiseconds")
        except ValueError:
            self.log(f"Invalid otim value: {centiseconds}")
    
    def handle_level(self, moves, base_time, increment):
        """Set time controls
        Format: level MOVES BASE INC
        MOVES = moves per session (0 = all moves)
        BASE = base time (minutes or minutes:seconds)
        INC = increment in seconds
        """
        try:
            self.moves_per_session = int(moves)
            
            # Parse base time (could be "5" or "2:30")
            if ':' in base_time:
                parts = base_time.split(':')
                minutes = int(parts[0])
                seconds = int(parts[1])
                self.base_time = minutes + seconds / 60.0
            else:
                self.base_time = float(base_time)
            
            self.increment = float(increment)
            
            self.log(f"Time control: {self.moves_per_session} moves, "
                    f"{self.base_time} min base, {self.increment}s inc")
        except (ValueError, IndexError):
            self.log(f"Invalid level command: {moves} {base_time} {increment}")
    
    def handle_st(self, seconds):
        """Set time per move in seconds"""
        try:
            time_per_move = float(seconds)
            self.log(f"Time per move: {time_per_move} seconds")
            # Could adjust search based on this
        except ValueError:
            self.log(f"Invalid st value: {seconds}")
    
    def handle_sd(self, depth):
        """Set search depth"""
        try:
            self.search_depth = int(depth)
            self.log(f"Search depth set to: {self.search_depth}")
        except ValueError:
            self.log(f"Invalid sd value: {depth}")
    
    def handle_move_now(self):
        """Interrupt search and move immediately"""
        self.move_now = True
        self.log("Move now requested")
    
    def handle_post(self):
        """Enable thinking output"""
        self.post_mode = True
        self.log("Thinking output enabled")
    
    def handle_nopost(self):
        """Disable thinking output"""
        self.post_mode = False
        self.log("Thinking output disabled")
    
    def handle_result(self, result, reason):
        """Game result notification"""
        self.log(f"Game ended: {result} ({reason})")
        self.result_sent = True
    
    def handle_draw(self):
        """Handle draw offer (we'll decline for now)"""
        self.log("Draw offer received (declining)")
        # Could implement draw acceptance logic here
    
    def send_result(self):
        """Check and send game result if game is over"""
        if self.board.is_game_over() and not self.result_sent:
            result = self.board.result()
            
            if self.board.is_checkmate():
                self.send_command(f"# Checkmate! Result: {result}")
            elif self.board.is_stalemate():
                self.send_command(f"# Stalemate! Result: {result}")
            elif self.board.is_insufficient_material():
                self.send_command(f"# Insufficient material! Result: {result}")
            elif self.board.is_fifty_moves():
                self.send_command(f"# Fifty move rule! Result: {result}")
            elif self.board.is_repetition():
                self.send_command(f"# Threefold repetition! Result: {result}")
            else:
                self.send_command(f"# Game over! Result: {result}")
            
            self.result_sent = True
    
    def get_time_for_move(self):
        """Calculate time allocation for this move (simple strategy)"""
        if self.my_time is None:
            return None  # No time limit
        
        # Simple time management: use 1/40th of remaining time
        # (assuming ~40 moves to go if not in time control)
        time_centiseconds = self.my_time / 40
        
        # Add increment
        if self.increment > 0:
            time_centiseconds += self.increment * 100
        # Convert to seconds
        return time_centiseconds / 100.0

    def make_engine_move(self):
        """Make the engine calculate and play a move"""
        # Reset move now flag
        self.move_now = False
        
        # Check for game over
        if self.board.is_game_over():
            self.send_result()
            return
        
        # Check if it's engine's turn
        if self.board.turn != self.engine_color:
            self.log("Not engine's turn")
            return
        
        move_time = self.get_time_for_move()
        if move_time:
            self.log(f"Engine thinking (depth {self.search_depth}, "
                    f"{move_time:.2f}s)...")
        else:
            self.log(f"Engine thinking (depth {self.search_depth})...")
        
        start_time = time.time()
        
        # Use the existing minimax evaluation
        try:
            tree = evaluation.Node(
                self.search_depth,
                evaluation.PLAYER_NUM,
                0,
                self.board
            )
            
            # Show thinking if post mode is on
            if self.post_mode:
                self.send_command(f"# Searching to depth {self.search_depth}")
            
            move_result = evaluation.min_max(
                self.search_depth,
                tree,
                evaluation.PLAYER_NUM,
                -sys.maxsize,
                sys.maxsize
            )
            best_move = move_result[1]
            score = move_result[0]
            
            elapsed = time.time() - start_time
            
            if best_move is None:
                self.log("No legal moves available")
                self.send_result()
                return
            
            # Show thinking output
            if self.post_mode:
                # Format: ply score time nodes pv
                nodes = 0  # We don't track nodes currently
                centiseconds = int(elapsed * 100)
                self.send_command(
                    f"{self.search_depth} {score} {centiseconds} {nodes} "
                    f"{best_move.uci()}"
                )
            
            # Make the move
            self.board.push(best_move)
            
            # Send move in coordinate notation
            move_str = best_move.uci()
            self.send_command(f"move {move_str}")
            self.log(f"Engine played: {move_str} (score: {score}, "
                    f"time: {elapsed:.2f}s)")
            
            # Check if game ended after our move
            self.send_result()
        
        except Exception as e:
            self.log(f"Error during move calculation: {e}")
            import traceback
            traceback.print_exc()
            self.send_command(f"move {move_str}")
            self.log(f"Engine played: {move_str}")
            
        except Exception as e:
            self.log(f"Error during move calculation: {e}")
    
    def parse_command(self, line):
        """Parse and execute a single command"""
        parts = line.strip().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]
        
        # Command dispatch
        if command == "xboard":
            self.handle_xboard()
        
        elif command == "protover":
            version = args[0] if args else "1"
            self.handle_protover(version)
        
        elif command == "new":
            self.handle_new()
        
        elif command == "quit":
            self.handle_quit()
        
        elif command == "force":
            self.handle_force()
        
        elif command == "go":
            self.handle_go()
        
        elif command == "usermove":
            if args:
                self.handle_usermove(args[0])
        
        elif command == "setboard":
            if args:
                fen = " ".join(args)
                self.handle_setboard(fen)
        
        elif command == "ping":
            if args:
                self.handle_ping(args[0])
        
        # Time management commands (Phase 3)
        elif command == "time":
            if args:
                self.handle_time(args[0])
        
        elif command == "otim":
            if args:
                self.handle_otim(args[0])
        
        elif command == "level":
            if len(args) >= 3:
                self.handle_level(args[0], args[1], args[2])
        
        elif command == "st":
            if args:
                self.handle_st(args[0])
        
        elif command == "sd":
            if args:
                self.handle_sd(args[0])
        
        elif command == "?":
            self.handle_move_now()
        
        # Thinking output commands (Phase 4)
        elif command == "post":
            self.handle_post()
        
        elif command == "nopost":
            self.handle_nopost()
        
        elif command == "result":
            if len(args) >= 2:
                result = args[0]
                reason = " ".join(args[1:])
                self.handle_result(result, reason)
        
        elif command == "draw":
            self.handle_draw()
        
        elif command == "playother":
            # Switch sides
            self.force_mode = False
            self.engine_color = not self.board.turn
            self.log(f"Engine now plays {self.engine_color}")
        
        elif command == "white":
            # Set engine to play white (if in force mode)
            if self.force_mode:
                self.engine_color = chess.WHITE
                self.log("Engine set to play WHITE")
        
        elif command == "black":
            # Set engine to play black (if in force mode)
            if self.force_mode:
                self.engine_color = chess.BLACK
                self.log("Engine set to play BLACK")
        
        # Moves without "usermove" prefix (for backward compatibility)
        elif len(command) >= 4 and len(command) <= 5:
            # Might be a move like "e2e4" or "e7e8q"
            try:
                move = chess.Move.from_uci(command)
                if move in self.board.legal_moves:
                    self.handle_usermove(command)
                else:
                    self.log(f"Unknown command or illegal move: {command}")
            except (ValueError, chess.InvalidMoveError):
                self.log(f"Unknown command: {command}")
        
        else:
            # Unknown command - silently ignore as per protocol
            self.log(f"Unknown command: {command}")
    
    def run(self):
        """Main engine loop - read commands from stdin and respond"""
        self.log("AlfaGeir Chess Engine started")
        self.log("Waiting for commands...")
        
        # Main command loop
        try:
            while True:
                line = sys.stdin.readline()
                if not line:  # EOF
                    break
                line = line.strip()
                if line:
                    self.log(f"Received: {line}")
                    self.parse_command(line)
        
        except (KeyboardInterrupt, SystemExit):
            self.log("Engine shutting down")
        
        except Exception as e:
            self.log(f"Fatal error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Ensure streams are flushed on exit
            sys.stdout.flush()
            sys.stderr.flush()


def main():
    """Entry point for XBoard engine"""
    engine = XBoardEngine()
    engine.run()


if __name__ == "__main__":
    main()
