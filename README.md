# django-chess


## Release Note

### 0.0.1
[ui] basic stuff
* grid
* pieces

### 0.0.2
[gamelogic]
* implementation of all pieces standard moves
* added special moves : Pawn+2, Enpassant, Promotion

[ui]
* colors on selected/moved pieces
* logs
* turn side information
* debug details

### 0.0.3
[gamelogic]
* avoid move when inducing check on own king
* surrender button (required to finish a game when checkmate)
* rook

[ui]
* lifter in logs panel
* own king check information






## Incoming


## Todo

### Urgent
[gamelogic]
* finish casting :
 * casting should be avoid when path is in check

[ui]
* information for all avoid move cases

### MidTerm
[gamelogic]

[ui]

### LongTerm
[gamelogic]
* user lobby
* give user capacity to :
  1. create games
  1. edit/delete its own games
  1. select a side in an opened game
  1. start the game when all sides have a player
* lock game (and refresh) when user do not plays current side turn

[ui]
* bootstrap
* nice colors (button)


## Refactoring

### Shield :
* x,y/c,l coordinates

### Layerize :
* think about a kind of BoardDataAccessor to facilite/centralize access to board data :
    - standard format to pass request parameters (by-coords/by-piece, etc)
    -
* think about a real game_data object to improve access to sql data :
    - get : return cache data, otherwise sql data (and store in cache)
    - set : stores data in sql and cache







## PersistentData Game Model :

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




## Limitations
* no rook
* no check/checkmate arbitration (checkmate must be manually played to be appliyed)

## known bugs
### GRAVE (not contournable)

### MAJOR (contournable manually)

### MINOR
* promotion available when checkmate


## fast ideas


### finish implementing properly class DataPieceMove
* must manage all data produced (by a move) and required (by interfaces)
1. source_piece (real Piece object)
1. target_piece (real Piece object)
1. promotion
1. eat
1. en_passant

### moves
* implement remaining moves :
1. O-O           King and Rook
1. O-O-O         King and Rook

### button
* surrender to give the win
    (actually necessary to finalize a game when checkmate, while waiting its automated detection)

### token change automations
* king checking :
   - checkmate (sinon killed, mais c pas top)

### gamelogic
* ending of game (abandon, king-killed, checkmate, draw)
* checkmate ends game


