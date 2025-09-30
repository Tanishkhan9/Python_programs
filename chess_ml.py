#!/usr/bin/env python3
"""
Simple supervised chess policy net (PyTorch).
Usage:
  - Put some PGN games into "games.pgn" or change filename.
  - python chess_ml.py --train
  - python chess_ml.py --play

This is a minimal baseline intended for learning/experimentation.
"""

import argparse
import math
import random
from pathlib import Path

import chess
import chess.pgn
import numpy as np
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# ---------- helpers: board encoding and move indexing ----------

# We'll use a 8x8x12 binary stack: 6 piece types × 2 colors
piece_to_plane = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN: 4,
    chess.KING: 5
}

def board_to_tensor(board: chess.Board):
    """
    Convert a python-chess Board to a (12,8,8) numpy array.
    Planes 0-5 white pawn...king, 6-11 black pawn...king
    """
    arr = np.zeros((12, 8, 8), dtype=np.float32)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        plane = piece_to_plane[piece.piece_type] + (0 if piece.color == chess.WHITE else 6)
        r = 7 - (square // 8)  # rank to row (so white perspective bottom)
        c = square % 8
        arr[plane, r, c] = 1.0
    return arr

# move indexing: from_square (0..63) * 64 + to_square (0..63) => 0..4095
def move_to_index(move: chess.Move):
    return move.from_square * 64 + move.to_square

def index_to_move(idx: int):
    from_sq = idx // 64
    to_sq = idx % 64
    return chess.Move(from_sq, to_sq)

# ---------- Dataset ----------

class ChessDataset(Dataset):
    def __init__(self, pgn_path: str, max_games: int = None, max_positions_per_game: int = None):
        self.samples = []  # list of (board_tensor, move_index)
        pgn_path = Path(pgn_path)
        if not pgn_path.exists():
            raise FileNotFoundError(f"{pgn_path} not found")
        with open(pgn_path, 'r', encoding='utf-8', errors='ignore') as f:
            game_count = 0
            while True:
                if max_games is not None and game_count >= max_games:
                    break
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                game_count += 1
                board = game.board()
                pos_count = 0
                for move in game.mainline_moves():
                    if max_positions_per_game is not None and pos_count >= max_positions_per_game:
                        break
                    # Save the current board position and the move to play
                    board_tensor = board_to_tensor(board)
                    # Only consider "simple" moves (ignore promotions to other pieces? we encode promotion by to-square only -> loses info)
                    # To keep it simple, we will only include moves that are not promotions or handle promotions by mapping to to_square (less ideal).
                    move_idx = move_to_index(move)
                    self.samples.append((board_tensor, move_idx))
                    board.push(move)
                    pos_count += 1

        print(f"Loaded dataset: {len(self.samples)} positions from {pgn_path}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        board_tensor, move_idx = self.samples[idx]
        # return tensor and long label
        return torch.tensor(board_tensor), torch.tensor(move_idx, dtype=torch.long)

# ---------- Model ----------

class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        # small conv net
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 1024)
        self.fc2 = nn.Linear(1024, 4096)  # 64*64 possible moves

    def forward(self, x):
        # x: (B,12,8,8)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)  # raw logits for 4096 moves
        return x

# ---------- training & utilities ----------

def collate_fn(batch):
    boards = torch.stack([item[0] for item in batch])
    labels = torch.stack([item[1] for item in batch])
    return boards, labels

def train(model, dataset, epochs=5, batch_size=64, lr=1e-3, device='cpu'):
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    model.to(device)
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        pbar = tqdm(loader, desc=f"Epoch {epoch}/{epochs}")
        for boards, labels in pbar:
            boards = boards.to(device)
            labels = labels.to(device)
            logits = model(boards)
            loss = criterion(logits, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * boards.size(0)
            pbar.set_postfix(loss=loss.item())
        avg_loss = total_loss / len(dataset)
        print(f"Epoch {epoch} finished. Avg loss: {avg_loss:.4f}")

# ---------- play using model ----------

def legal_move_mask(board: chess.Board):
    """
    Return boolean mask of length 4096 where legal moves are True.
    """
    mask = np.zeros(4096, dtype=np.bool_)
    for mv in board.legal_moves:
        idx = move_to_index(mv)
        mask[idx] = True
    return mask

def choose_move(model, board: chess.Board, device='cpu'):
    model.eval()
    with torch.no_grad():
        b_tensor = torch.tensor(board_to_tensor(board)).unsqueeze(0).to(device)  # (1,12,8,8)
        logits = model(b_tensor).cpu().numpy().squeeze(0)  # (4096,)
        mask = legal_move_mask(board)
        masked_logits = np.where(mask, logits, -1e9)
        if not mask.any():
            return None
        best_idx = int(np.argmax(masked_logits))
        return index_to_move(best_idx)

# ---------- simple play loop: model vs. random or model vs. model ----------

def play_game(model_white, model_black, max_moves=200, device='cpu', verbose=True):
    board = chess.Board()
    move_count = 0
    while not board.is_game_over() and move_count < max_moves:
        if board.turn == chess.WHITE:
            model = model_white
        else:
            model = model_black
        mv = choose_move(model, board, device=device)
        if mv is None:
            break
        board.push(mv)
        move_count += 1
        if verbose:
            print(f"{move_count:03d}. {board.san(board.peek())}   ({'white' if board.turn==chess.BLACK else 'black'})")
    if verbose:
        print("Game over:", board.result(), board.outcome())
    return board

# ---------- main ----------

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pgn', type=str, default='games.pgn', help='PGN file with training games')
    p.add_argument('--train', action='store_true')
    p.add_argument('--play', action='store_true')
    p.add_argument('--epochs', type=int, default=3)
    p.add_argument('--batch', type=int, default=128)
    p.add_argument('--device', type=str, default='cpu')
    args = p.parse_args()

    device = args.device
    model = PolicyNet()

    model_path = Path('policy_net.pt')

    if args.train:
        print("Loading dataset...")
        ds = ChessDataset(args.pgn, max_games=5000, max_positions_per_game=200)  # tune these for your machine
        print("Training model...")
        train(model, ds, epochs=args.epochs, batch_size=args.batch, device=device)
        torch.save(model.state_dict(), model_path)
        print(f"Saved model to {model_path}")

    if args.play:
        if model_path.exists():
            model.load_state_dict(torch.load(model_path, map_location=device))
            print("Loaded model from", model_path)
        else:
            print("No saved model found; using randomly initialized model (weak).")

        # play model vs random move agent
        class RandomAgent:
            def __init__(self):
                pass
            def choose(self, board):
                moves = list(board.legal_moves)
                return random.choice(moves) if moves else None

        # wrap model as object with choose method
        class ModelAgent:
            def __init__(self, model, device='cpu'):
                self.model = model
                self.device = device
            def choose(self, board):
                return choose_move(self.model, board, device=self.device)

        # Example: model as white, random as black
        model_agent = ModelAgent(model, device=device)
        # We'll adapt play_game to accept choose methods:
        board = chess.Board()
        move_num = 0
        while not board.is_game_over() and move_num < 200:
            if board.turn == chess.WHITE:
                mv = model_agent.choose(board)
            else:
                mv = random.choice(list(board.legal_moves))
            if mv is None:
                break
            board.push(mv)
            move_num += 1
            print(f"{move_num:03d}. {board.san(board.peek())}")

        print("Result:", board.result(), "Outcome:", board.outcome())

if __name__ == '__main__':
    main()