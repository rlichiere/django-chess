# django-chess

### PersistentData Game Model :

```python
{
   'token': {
      'step': {
         'side': '[white/black]'
         'name': '[waitReadyToStart/waitCellSource/waitCellTarget/pieceMoved/checkmate]'
         'data': {
            'targetCell": {
               'column': 'f',
               'line": '4'
            },
            'sourceCell': {
               'column': 'f',
               'line': '2'
            },
            ['eaten': {
					's': 'w',
					'r': 'P',
					'n': 'p6'
			}]
         }
         ['enpassant': {
            'y': 3,
            'x': 5
         }]
      },
      'logs': {
         '001.': {
            'official': 'e2-e4',
            'side': 'w',
            'source': {
               'x': 'e',
               'y': '2',
               'piece': {
                  's': 'w',
                  'r': 'P',
                  'n': 'P5'
               }
            },
            'target': {
               'x': 'e',
               'y': '4',
               'piece': '-'
            }
         },
         [...]
      }
   },
   'board': {
      '1': {
        'a': {
           's': 'w',
           'r': 'R',
           'n': 'r2'
        },
        [...]
      },
      [...]
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

### token change automations
- king checking :
    - check when taking hand
    - avoid move if ends up with check
    - checkmate (sinon killed, mais c pas top)

### gamelogic
- ending of game (abandon, king-killed, checkmate, draw)
- checkmate ends game


