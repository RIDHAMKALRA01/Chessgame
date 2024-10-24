import pygame
import chess
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = WIDTH // DIMENSION
FPS = 15
PIECE_FONT_SIZE = 80  # Increased font size
IMAGES = {}
selected_square = None  # The selected square
valid_moves = []  # List to track valid moves for a selected piece

# Timer variables
white_time = 300  # 5 minutes for white
black_time = 300  # 5 minutes for black
white_timer_running = True  # Start white's timer first
black_timer_running = False
last_move_time = time.time()

# Piece Unicode characters
PIECE_UNICODE = {
    'wP': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔',
    'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚'
}

# Load images for chess pieces
def load_images():
    try:
        font = pygame.font.SysFont('Segoe UI Symbol', PIECE_FONT_SIZE)
    except:
        font = pygame.font.SysFont('Arial', PIECE_FONT_SIZE)
    
    for piece in PIECE_UNICODE.keys():
        image = font.render(PIECE_UNICODE[piece], True, pygame.Color("black"))
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

# Function to draw the chessboard
def draw_board(screen):
    colors = [pygame.Color(238, 238, 210), pygame.Color(118, 150, 86)]  # Light and dark squares
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Function to highlight possible moves for a selected piece
def highlight_squares(screen, board):
    if selected_square is not None:
        # Highlight selected square
        row, col = divmod(selected_square, DIMENSION)
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # Transparency
        s.fill(pygame.Color("blue"))
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

        # Highlight possible moves
        for move in valid_moves:
            row, col = divmod(move.to_square, DIMENSION)
            s.fill(pygame.Color("green"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

# Function to draw pieces on the board
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.piece_at(r * DIMENSION + c)
            if piece:
                piece_str = piece.symbol()
                piece_color = 'w' if piece_str.isupper() else 'b'
                piece_name = piece_color + piece_str.upper()
                screen.blit(IMAGES[piece_name], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Convert mouse position to board coordinates
def get_board_pos(mouse_pos):
    x, y = mouse_pos
    col = x // SQ_SIZE
    row = y // SQ_SIZE
    return row, col

# Handle mouse clicks and piece selection
def handle_mouse_click(board, pos):
    global selected_square, valid_moves, white_timer_running, black_timer_running
    row, col = pos
    square = row * DIMENSION + col

    if selected_square is None:
        piece = board.piece_at(square)
        if piece and (piece.color == board.turn):
            selected_square = square
            valid_moves = [move for move in board.legal_moves if move.from_square == selected_square]
    else:
        move = chess.Move(from_square=selected_square, to_square=square)
        if move in board.legal_moves:
            board.push(move)
            # Switch timer
            if board.turn:  # If it was white's turn
                white_timer_running = True
                black_timer_running = False
            else:  # If it was black's turn
                black_timer_running = True
                white_timer_running = False

            # Reset selected square and valid moves
            selected_square = None
            valid_moves = []

# Function to draw the timer on the right side
def draw_timer(screen):
    global white_time, black_time
    font = pygame.font.SysFont('Arial', 40)
    
    # Draw white timer
    white_time_text = font.render(f"White: {int(white_time // 60):02}:{int(white_time % 60):02}", True, pygame.Color("black"))
    screen.blit(white_time_text, (WIDTH - 200, HEIGHT // 2 - 40))

    # Draw black timer
    black_time_text = font.render(f"Black: {int(black_time // 60):02}:{int(black_time % 60):02}", True, pygame.Color("black"))
    screen.blit(black_time_text, (WIDTH - 200, HEIGHT // 2 + 20))

# Function to update the timer
def update_timer():
    global white_time, black_time, white_timer_running, black_timer_running, last_move_time
    current_time = time.time()
    elapsed_time = current_time - last_move_time

    # Update only the running timer
    if white_timer_running:
        white_time -= elapsed_time
    if black_timer_running:
        black_time -= elapsed_time

    last_move_time = current_time

# Function to handle chess logic and updates
def play_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Game')
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))

    # Initialize board and load images
    board = chess.Board()
    load_images()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_mouse_click(board, get_board_pos(mouse_pos))

        update_timer()  # Update timers

        # Check for timer expiration
        if white_time <= 0 and black_time > 0:
            print("Black wins on time!")
            running = False
        elif black_time <= 0 and white_time > 0:
            print("White wins on time!")
            running = False
        elif white_time <= 0 and black_time <= 0:
            print("Draw on time!")
            running = False

        draw_board(screen)
        highlight_squares(screen, board)  # Highlight selected squares and moves
        draw_pieces(screen, board)
        draw_timer(screen)  # Draw the timer on the right side

        if board.is_checkmate():
            print("Checkmate!")
            running = False
        elif board.is_stalemate():
            print("Stalemate!")
            running = False
        elif board.is_insufficient_material():
            print("Draw due to insufficient material!")
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    play_game()
