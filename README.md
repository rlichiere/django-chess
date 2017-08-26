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



###### todo

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


