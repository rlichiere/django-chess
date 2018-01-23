/**
 * Created by rlichiere on 01/01/2018.
 */


// configuration
var opt_number_of_lines, opt_number_of_columns, opt_number_of_cards;

// structural data
var cards = [];
var GAME_STATUS = {
    EMPTY: 'EMPTY',
    WAIT_FIRST_SELECT: 'WAIT_FIRST_SELECT',
    WAIT_SECOND_SELECT: 'WAIT_SECOND_SELECT',
    WAIT_ROLLBACK: 'WAIT_ROLLBACK',
    FINISHED: 'FINISHED'
};
var gameStatus = GAME_STATUS.EMPTY; // playing/finished

// live data
var discoveredCells = [];
var selectedCells = [];
var playerAttempts = 0;

function generateCode() {
    var _newCode = {
        r: parseInt(Math.random() * 5),
        v: parseInt(Math.random() * 5),
        b: parseInt(Math.random() * 5)
    };
    var codeName = _newCode.r + '.' + _newCode.v + '.' + _newCode.b;
    return {name: codeName, code: _newCode};
}

function buildCards() {
    var _cardCouples = [];
    var used_codes = [];
    for (var coupleNum=0; coupleNum < opt_number_of_cards / 2; coupleNum++) {

        var newCodeSet = false;
        while (newCodeSet == false) {
            var newCode = generateCode();
            if (!used_codes[newCode.name]) {
                _cardCouples[_cardCouples.length] = newCode.code;
                _cardCouples[_cardCouples.length] = newCode.code;
                used_codes = newCode.name;
                newCodeSet = true;
            }
        }
    }
    return _cardCouples;
}

function initializeBoard() {
    var _cards = buildCards();
    for (var line_num=0; line_num < opt_number_of_lines; line_num++) {
        cards[line_num] = [];
        for (var col_num=0; col_num < opt_number_of_columns; col_num++) {
            var popIndex = parseInt(Math.random() * _cards.length);
            var card = _cards[popIndex];
            _cards.splice(popIndex, 1);
            cards[line_num][col_num] = card;
        }
    }
}

function hasBeenSelected(col, line) {
    for (var key in selectedCells) {
        if ((selectedCells[key].x == col) && (selectedCells[key].y == line) ) {
            return true;
        }
    }
    return false;
}
function hasBeenDiscovered(col, line) {
    for (var index=0; index < discoveredCells.length; index++) {
        var disc = discoveredCells[index];
        if ((disc.x == col) && disc.y == line) {
            return true;
        }
    }
    return false;
}


function sketchProc(processing) {
    var width = 700;
    var height = 700;

    var X, Y;
    var nX, nY;
    var delay = 3;


    processing.setup = function () {
        processing.size(width, height);
        processing.strokeWeight(1);
        processing.frameRate(60);
        X = processing.width / 2;
        Y = processing.height / 2;
        nX = X;
        nY = Y;

        opt_number_of_cards = document.getElementsByName('number_of_cards')[0].value;
        opt_number_of_lines = document.getElementsByName('number_of_lines')[0].value;
        opt_number_of_columns =  opt_number_of_cards / opt_number_of_lines;

        initializeBoard();
        drawBoard();
    };

    function setPen(r, v, b) {
        processing.stroke(r, v, b);
        processing.strokeWeight(3);
        processing.fill(r, v, b);
    }

    function drawCell(col, line) {
        var cell_width = width / opt_number_of_columns;
        var cell_height = height / opt_number_of_lines;
        var card = cards[line][col];

        if (hasBeenDiscovered(col, line) || hasBeenSelected(col, line)) {
            setPen(card.r * 50, card.v * 50, card.b * 50);
        } else {
            setPen(0, 0, 0);
        }

        var p1_x = col * cell_width;
        var p1_y = line * cell_height;
        var p2_x = col + cell_width;
        var p2_y = line + cell_height;
        processing.rect(p1_x, p1_y, p2_x, p2_y);
    }

    function drawSeparator(mode, index) {
        if (mode == 'vertical') {
            var cell_width = width / opt_number_of_columns;
            var p1_x = index * cell_width;
            processing.line(p1_x, 0, p1_x, width);
        } else if (mode == 'horizontal') {
            var cell_height = height / opt_number_of_lines;
            var p1_y = index * cell_height;
            processing.line(0, p1_y, height, p1_y);
        }
    }

    function drawCells() {
        for (var line_num = 0; line_num < opt_number_of_lines; line_num++) {
            for (var col_num = 0; col_num < opt_number_of_columns; col_num++) {
                drawCell(col_num, line_num);
            }
        }
    }

    function drawSeparators() {
        setPen(255, 255, 255);
        for (var line_num = 1; line_num < opt_number_of_lines; line_num++) {
            drawSeparator('horizontal', line_num);
        }
        for (var col_num = 1; col_num < opt_number_of_columns; col_num++) {
            drawSeparator('vertical', col_num);
        }
    }

    function drawBoard() {
        drawCells();
        drawSeparators();
    }

    processing.draw = function () {
        X += (nX - X) / delay;
        Y += (nY - Y) / delay;
        drawBoard();
    };

    processing.mouseMoved = function () {
        nX = processing.mouseX;
        nY = processing.mouseY;
    };

    processing.mouseClicked = function () {
        if (gameStatus == GAME_STATUS.WAIT_FIRST_SELECT || gameStatus == GAME_STATUS.WAIT_SECOND_SELECT || gameStatus == GAME_STATUS.WAIT_ROLLBACK) {
            // console.log('mouseClicked: x:' + nX + ', y:' + nY);
            revealCell(nX, nY);
        } else if (gameStatus == GAME_STATUS.FINISHED) {
            console.log('Click update button to launch a new game.');
        }
    };

    function revealCell(mouseX, mouseY) {
        var cell_x = -1;
        var cell_y = -1;
        var cell_width = width / opt_number_of_columns;
        var cell_height = height / opt_number_of_lines;
        for (var col=0; col < opt_number_of_columns; col++) {
            for (var line=0; line < opt_number_of_lines; line++) {
                if (((line * cell_height) < mouseY) && (((line+1) * cell_height) > mouseY)) {
                    cell_y = line;
                    break;
                }
            }
            if (((col * cell_width) < mouseX) && (((col+1) * cell_width) > mouseX)) {
                cell_x = col;
            }
            if (cell_x >=0 && cell_y >=0) {
                break;
            }
        }

        if (gameStatus == GAME_STATUS.WAIT_FIRST_SELECT) {
            if (!hasBeenDiscovered(cell_x, cell_y)) {
                playerAttempts += 1;
                selectedCells['first'] = {x: cell_x, y:cell_y};
                gameStatus = GAME_STATUS.WAIT_SECOND_SELECT;
            }
        } else if (gameStatus == GAME_STATUS.WAIT_SECOND_SELECT) {
            if ((selectedCells['first'].x != cell_x) || (selectedCells['first'].y != cell_y)) {
                if (!hasBeenDiscovered(cell_x, cell_y)) {
                    selectedCells['second'] = {x: cell_x, y: cell_y};
                    var sourceColors = cards[selectedCells['first'].y][selectedCells['first'].x];
                    var targetColors = cards[cell_y][cell_x];
                    if (sourceColors.r == targetColors.r && sourceColors.v == targetColors.v && sourceColors.b == targetColors.b) {
                        console.log('Same cell, bravo !');
                        playerAttempts += 1;
                        discoveredCells[discoveredCells.length] = {
                            x: selectedCells['first'].x,
                            y: selectedCells['first'].y
                        };
                        discoveredCells[discoveredCells.length] = {x: cell_x, y: cell_y};
                        if (discoveredCells.length == opt_number_of_cards) {
                            console.log('Finish. Super !');
                            // selectedCells = [];
                            gameStatus = GAME_STATUS.FINISHED;
                            showScore();
                        }
                    } else {
                        console.log('fail.');
                    }
                    if (gameStatus != GAME_STATUS.FINISHED) {
                        gameStatus = GAME_STATUS.WAIT_ROLLBACK;
                    }
                }
            }
        } else if (gameStatus == GAME_STATUS.WAIT_ROLLBACK) {
            selectedCells = [];

            gameStatus = GAME_STATUS.WAIT_FIRST_SELECT;
        }
        refreshGameDataUI();
    }
}

function refreshGameDataUI() {
    var elemPlayerClickCount = document.getElementById('player_click_count');
    elemPlayerClickCount.innerText = '' + playerAttempts;
}

function showScore() {
    var elemPlayerScore = document.getElementById('player_score');
    var player_score = opt_number_of_cards * opt_number_of_cards - playerAttempts;
    elemPlayerScore.innerText = '' + player_score;
    elemPlayerScore.parentElement.setAttribute('style', 'display: block;');
}
function hideScore() {
    var elemPlayerScore = document.getElementById('player_score');
    elemPlayerScore.parentElement.setAttribute('style', 'display: none;');
    elemPlayerScore.innerText = '';
}

var canvas = document.getElementById("mycanvas");
var p = new Processing(canvas, sketchProc);



// Game Logic
function initializeGame() {
    // kill Processing if exists
    try {
        p.exit();
    } catch(e) {}
    hideScore();

    discoveredCells = [];
    selectedCells = [];

    p = new Processing(canvas, sketchProc);

    playerAttempts = 0;
    gameStatus = GAME_STATUS.WAIT_FIRST_SELECT;
}

function reloadGame() {
    initializeGame();
}

function onOptionsChanged () {
    reloadGame();
}


