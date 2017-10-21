# django-chess


## Release Note

### 0.0.1
[ui] basic stuff
* grid
* pieces

### 0.0.2
[game logic]
* implementation of all pieces standard moves
* added special moves : Pawn+2, Enpassant, Promotion

[ui]
* colors on selected/moved pieces
* logs
* turn side information
* debug details

### 0.0.3
[game logic]
* avoid move inducing check on own king
* added checkmate/surrender button (required to finish a game when checkmate)
* added complete rook move
* user management
 * authentication form and views filtering
 * user participation management
 * winning_games management
* color_set customization

[ui]
* lifter in logs panel
* own king check information
* lobby : opened, running and closed games, game creation
* filter menu buttons depending on user profile :
 * viewer : nothing
 * player : surrender/checkmate
 * game creator : Reset current round, Reset game
* refresh page for waiting player and viewers

### 0.0.4
[game logic]
* user registration :
 * players are able to registrate
 * players are able to change their password

[ui]
* registration form
* improvements in lobby, game and profile pages
* show kingcheck

### 0.0.5
[game logic]
* elo management (https://fr.wikipedia.org/wiki/Classement_Elo)
* save/load game management (manual and auto)

[ui]
* game page shows players material
* history of ranked games
* added filter games history : ranked/unranked/all
* user theme management
* major improvements everywhere :
 * layouts
 * forms
 * cleaned colors

### 0.0.6
[game logic]

[ui]

## Incoming

### feature_custom_piece_set
[game_logic]
* user custom pieces management
* yamled available_themes, available_pieces and levels

[ui]
* profile : added piece selector
* profile : filter theme and piece set depending on player level
* nav : added Admin link

## Todo

### Urgent
[game logic]
* load game (except for ranked games)
    * give possibility to change player sides
* opened games list : add ranked/unranked option

[ui]
* add elo level icons
* show players elo level in ranked games

### ShortTerm
[game logic]
* give user capacity to :
  1. edit/delete its own games
  1. start the game when all sides have a player

[ui]
* information for all avoid move cases
* link a graphical set to each level (activable by user in its profile)

### MidTerm
[game logic]
* for viewers : add capacity to move in history and log

### LongTerm
[game logic]
* refactor lobby mechanics to a Lobby class :
 * game management : generic status to retrieve opened/running/finished/archived specific status
 * game creation : generic form to manage game specific creation process)
 * user management : generic user participation (1v1, NvN, etc)
* user ranking :
 * Elo calculation
 * player Elo initialization
 * find ranked game (based on Elo)
 * find unranked game (based on Elo, or not)

[ui]
* bootstrap
* nice colors (button)
* Elo statistic pages

## Refactoring

### Shield :
* x,y/c,l coordinates

### Layerize :
* think about a kind of BoardDataAccessor to facilite/centralize access to board data :
    - standard format to pass request parameters (by-coords/by-piece, etc)

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
            },
            'board': {
                [board_data],
            },
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
   'logs': {
      'nnn': {
         'side': 'white/black',
         'official': 'xxx/e2-e4',
         'source': {
            'piece': 'p',
            'x': 'e',
            'y': '2'
         },
         'target': {
            'x': 'e',
            'y': '4'
         }
      }
   },
   'game_options': {
      'name': 'xxx',
      'winning_games': 1/2/n,
      'creator': user_id,
      'ranked': true/false,
      'public': true/false,
      'logging': true/false,
   },
   'participants': {
        'white': {
            '1': user_id,
        },
        'black': {
            '1': user_id,
            '2': user_id,
        }
   },
   'rounds': {
        '1': {
            'result': 'checkmate/draw/withdraw',
            'winner': 'white/black'
        }
   },
   'result': {
        'winner': 'white/black',
        'round_list': 'wbw',
   }
}
```




## Limitations
* no check/checkmate arbitration (checkmate must be manually played to be applied)

## known bugs
### GRAVE (not contournable)
* crash on checkmate when no plyer in other side

### MAJOR (contournable manually)
* Enabled logging overloads game_data
    * should test performance with mysql
    * should test performance with real webserver
    * should remove boards and logs from render2jsondebug

### MINOR

* promotion available when checkmate                    todo : a verifier


## fast ideas


### token change automations
* king checking :
   - checkmate should be automatically detected

### gamelogic
* ending of game (withdraw, draw)

