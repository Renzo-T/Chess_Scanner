
import cv2
from ChessLocalization import localization
from ChessLocalization import dice
from GPCam import gpcam
import os
from stockfish import Stockfish
import numpy as np
# import keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def main():
    scriptDir = os.path.dirname(__file__)
    img_path = os.path.join(scriptDir, 'images/full.png')
    # frame = cv2.imread(img_path)

    frame = gpcam()
    board = localization(frame)
    # board = cv2.rotate(board, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # frame_path = os.path.join(scriptDir, 'images/full.png')
    # cv2.imwrite(frame_path, frame)
    while(1):
        cv2.imshow('frame',board)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            quit()
        elif k == ord('r'):
            # frame = cv2.imread(img_path)
            frame = gpcam()
            board = localization(frame)
        elif k == ord('c'):
            break

    # img = dice(board)
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "dataset",
        validation_split = 0.2,
        subset= "training",
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "dataset",
        validation_split = 0.2,
        subset = "validation"
    )

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation = 'relu'),
        tf.keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    train_labels_words = ['bBishop', 'bKing', 'bKnight', 'bPawn', 'bQueen', 'bRook', 'nothing', 'wBishop','wKing','wKnight', 'wPawn', 'wQueen', 'wRook']
    train_labels = [0,1,2,3,4,5,6,7,8,10,11,12]
    model.fit(train_ds, train_labels, epochs=10)

    p_model = tf.keras.Sequential([model,tf.keras.layers.Softmax()])

    dims = board.shape
    y = dims[0]//8
    x = dims[0]//8

    pred = [["" for x in range(8)] for y in range(8)]
    curX = 0
    curY = 0
    for i in range(8):
        for j in range(8): 
            # print(str(i) + " " + str(j))
            # cv2.imshow(str(i*8+j+1), board[curY:curY+y, curX:curX+x])
            predictions = p_model.predict(board[curY:curY+y, curX:curX+x])
            out = train_labels_words[np.argmax(predictions[0])]
            curX += x
        curX = 0
        curY += y

    pred = np.rot90(pred)
    pred = np.rot90(pred)   

    for i in range(8):
        for j in range(8):
            pred[i,j] = switch(pred[i,j])

    fen = ""
    for i in range(8):
        ct = 0
        for j in range(8):
            if not isInt(pred[i,j]):
                fen = fen + pred[i,j]
            else:
                if isInt(fen[-1]):
                    num = int(fen[-1])
                    fen = fen.substring(0, fen.length() - 1)
                    fen = fen + str(num+1)
                fen = fen + "1"
        if i != 7:
            fen += "/"
        
    turn = input("B/W to move?: ")
    if turn == "W":
        fen = fen + " w KQkq - 0 1"
    else:
        fen = fen + " b KQkq - 0 1"
        
    cw_dir = os.path.dirname(__file__)
    sf_path = "stockfish_20090216_x64_bmi2"
    abs_path = os.path.join(cw_dir,sf_path)


    stockfish = Stockfish(abs_path);
    stockfish.set_fen_position(fen)
    print(fen)
    print(stockfish.get_board_visual())
    print(stockfish.get_best_move())


    


                

def switch(piece):
    switcher = {
        'bBishop': "b",
        'bKing': "k",
        'bKnight': "n",
        'bPawn': "p",
        'bQueen': "q",
        'bRook': "r", 
        'nothing': 1, 
        'wBishop': "B",
        'wKing': "K",
        'wKnight': "N", 
        'wPawn': "P", 
        'wQueen': "Q", 
        'wRook': "R"
    }
    return switcher.get(piece, "Invalid")
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()