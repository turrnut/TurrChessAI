# P0
# N1
# B2
# R3
# Q4
# K5
# O6
# todo : go back a move
import chess
import pandas
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import json
import numpy as np
import random
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import ModelCheckpoint


board = chess.Board()

# Define the mapping from index to chess piece type
index_to_piece = {
    0: 'P',  # Pawn
    1: 'N',  # Knight
    2: 'B',  # Bishop
    3: 'R',  # Rook
    4: 'Q',  # Queen
    5: 'K',  # King
    6: 'O',  # Special case for Castling
}

def predict_next_piece(model, moves):
    board.reset()
    for move in moves:
        board.push_san(move)

    move_indices = [board.piece_at(move.from_square).piece_type - 1 for move in board.legal_moves if board.piece_at(move.from_square)]

    # Pad the sequence to match the expected input length of 348
    padded_input = pad_sequences([move_indices], maxlen=348, padding='post')
    
    prediction = model.predict(padded_input)
    sorted_pieces = np.argsort(prediction[0])[::-1]

    possible = []

    for piece_index in sorted_pieces:
        piece_type = index_to_piece[piece_index]
        for move in board.legal_moves:
            if board.piece_at(move.from_square) and board.piece_at(move.from_square).symbol().upper() == piece_type:
                possible.append(board.san(move))

    if len(possible) == 0:
        return None
    return random.Random().choice(seq=possible)

def pvp():
    board = chess.Board()
    moves = []
    print("Enter \'quit\' to exit")
    print("Enter \'display\' to display board")
    while not board.is_game_over():
        print("========================")
        try:
            move = input("Move: ")
            if move.lower() == "quit":
                print("Game terminated")
                break
            elif move.lower() == "display":
                print(board)
                continue

            if move in [board.san(m) for m in board.legal_moves]:
                moves.append(move)
                board.push_san(move)
            else:
                print("Illegal Move, try again.")
                continue
        except ValueError:
            print("Invalid move format or illegal move, please try again.")
    print("Game over", board.result())

def vcomputer(model):
    board = chess.Board()
    moves = []
    print("Enter \'quit\' to exit")
    print("Enter \'display\' to display board")
    while not board.is_game_over():
        print("========================")
        # try:
        move = input("Move: ")
        if move.lower() == "quit":
            print("Game terminated")
            break
        elif move.lower() == "display":
            print(board)
            continue

        if move in [board.san(m) for m in board.legal_moves]:
            moves.append(move)
            board.push_san(move)
            ai_move = predict_next_piece(model, moves)
            if ai_move == None:
                break
            moves.append(ai_move)
            board.push_san(ai_move)
            print(f"{move} AI did:", ai_move)
        else:
            print("Illegal Move, try again.")
            continue
        # except ValueError as e:
        #     print(e)
        #     print("Invalid move format or illegal move, please try again.")
    print("Game over", board.result())

def mainloop():
    model = load_model('chess.h5')
    print("===Welcome to TurrChess!===")
    while True:
        print("1 - player vs player\n2 - player vs computer\n3 - exit")
        option = input()
        if option =="" or option not in "123":
            print("input invalid")
            continue
        elif option == "1":
            pvp()
            print("=======================")
        elif option == "2":
            vcomputer(model)
            print("=======================")
        elif option == "3":
            break
        else:
            print("input invalid")
            continue

mainloop()
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
# # TRAINING

# MODEL_PATH = 'chess.h5'

# # Step 1: Load and prepare the data
# with open('data\chess\Trainable.json', 'r') as file:
#     training_data = json.load(file)

# # Convert training data to numpy arrays for use with Keras
# X = [np.array(sequence[0]) for sequence in training_data]
# y = [np.array(sequence[1]) for sequence in training_data]

# # Padding sequences to ensure they are all the same length
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# max_sequence_len = max(len(x) for x in X)
# X_padded = pad_sequences(X, maxlen=max_sequence_len, padding='post')

# # Step 2: Define the model
# model = Sequential([
#     Embedding(input_dim=7, output_dim=10, input_length=max_sequence_len),  # Embedding layer
#     LSTM(64),  # LSTM layer with 64 units
#     Dense(7, activation='softmax')  # Output layer with softmax
# ])
# model = load_model('chess.h5')

# # Compile the model
# model.compile(optimizer=Adam(learning_rate=0.01), loss='categorical_crossentropy', metrics=['accuracy'])

# # Set up the ModelCheckpoint callback to save the model after each epoch
# checkpoint_callback = ModelCheckpoint(
#     filepath='chess.h5',
#     save_freq='epoch',  # 'save_freq' set to 'epoch' saves the model after each epoch
#     save_best_only=False,  # Set to True to save only the best model according to the validation loss
#     save_weights_only=False,  # Set to True to save only the weights
#     verbose=1  # Verbosity mode, 1 means that it will print messages when saving the model
# )

# # Step 3: Train the model
# model.fit(X_padded, np.array(y), epochs=50, batch_size=32, callbacks=[checkpoint_callback])


# print("Model training complete and saved.")
