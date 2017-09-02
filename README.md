# django-chess

### PersistentData Game Model :

```python
{
   'board': {[board.json]},
   'token': {
      'side': '[white/black]'
      'step': {
         'name': '[waitReadyToStart/waitCellSource/waitCellTarget/pieceMoved]'
         'data': {[step_data.json]
      }
   }
}
```

#### waitCellTarget model

```python
'waitCellTarget': {
   'sourceCell': {
      'line': '2',
      'column': 'e'
   }
}
```

#### pieceMoved model

```python
'pieceMoved': {
   'sourceCell': {
      'line': '2',
      'column': 'e'
   }
   'targetCell': {
      'line': '4',
      'column': 'e'
   },
}
```



###### limitations
- no rook
- no check/checkmate arbitration (checkmate must be manually played to be appliyed)

###### known bugs
# GRAVE (not contournable)

# MAJOR (contournable manually)

# MINOR
- promotion available when checkmate


###### todo


### finish implementing properly class DataPieceMove
# must manage all data produced (by a move) and required (by interfaces)
- source_piece (real Piece object)
- target_piece (real Piece object)
- promotion
- eat
- en_passant

### moves
- implement remaining moves :
    - O-O           King and Rook
    - O-O-O         King and Rook
    - en passant    Pawn and Pawn

### token change automations
- king checking :
    - check
    - checkmate (sinon killed, mais c pas top)

### gamelogic
- ending of game (abandon, king-killed, checkmate, draw)
- checkmate ends game


