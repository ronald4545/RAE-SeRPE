import pacman.pacman as pacman
import cPickle as pickle
import codecs
import random

game = None
layout = None

def init(state, dummy):
    print 'State = {}'.format(state)
    global game, layout
    rules = pacman.ClassicGameRules()
    rules.quiet = False
    gameDisplay = pacman.graphicsDisplay.PacmanGraphics()
    beQuiet = True
    catchExceptions = False
    noKeyboard = True
    ghostType = pacman.loadAgent('RandomGhost', noKeyboard)
    ghosts = [ghostType(i + 1) for i in range(1)]
    layout = pacman.layout.getLayout('mediumClassic')
    game = rules.newGame(
        layout, 'ReflexAgent', ghosts,
        gameDisplay, beQuiet, catchExceptions)
    gameDisplay.initialize(game.state.data)
    return True


def render(state):
    global game
    newState = state.data
    newState._agentMoved = 0
    game.display.update(newState)
    newState = state.data
    newState._agentMoved = 1
    game.display.update(newState)
    return True


def is_accessible(state, x, y):
    walls = state.game.state.getWalls()
    if walls[x][y] == True:
        return False
    else:
        ghosts = state.game.state.getGhostPositions()
        for ghost in ghosts:
            if ghost[0] == x and ghost[1] == y:
                return False
        return True


def go_up(state, dummy):
    # print 'go_up, state = {}'.format(state)
    return _go_direction(state, 'North')


def go_down(state, dummy):
    # print 'go_down, state = {}'.format(state)
    return _go_direction(state, 'South')


def go_left(state, dummy):
    # print 'go_left, state = {}'.format(state)
    return _go_direction(state, 'West')


def go_right(state, dummy):
    # print 'go_right, state = {}'.format(state)
    return _go_direction(state, 'East')


def _go_direction(state, direction):
    global game
    if game is None:
        init(state, None)
        state['state_vars']['value'][('GameState',)] = codecs.encode(pickle.dumps(game.state), "base64").decode()
    game_state = pickle.loads(codecs.decode(state['state_vars']['value'][('GameState',)].encode(), "base64"))
    # if direction not in game_state.getLegalActions():
    #     print 'direction = {}, getLegalActions = {}'.format(direction, game_state.getLegalActions())
    #     return False
    game_state = game_state.generateSuccessor(0, direction)
    render(game_state)
    state['state_vars']['value'][('score',)] = game_state.getScore()
    if game_state.getScore() < 0:
        return False
    elif game_state.getScore() > 100:
        state['state_vars']['value'][('score',)] = 'win'
    # if state['state_vars']['value'][('score',)] > 5.0:
    #     state['state_vars']['value'][('score',)] = 'win'
    # update ghost
    pacman_x, pacman_y = game_state.getPacmanPosition()
    ghost_x, ghost_y = game_state.getGhostPosition(1)
    ghost_action = random.choice(game_state.getLegalActions(1))
    game_state = game_state.generateSuccessor(1, ghost_action)
    pacman.time.sleep(0.005)
    print 'score = {}'.format(game_state.getScore())
    state['state_vars']['value'][('GameState',)] = codecs.encode(pickle.dumps(game_state), "base64").decode()
    state['state_vars']['value'][('North',)] = 'true' if 'North' in game_state.getLegalActions() else 'false'
    state['state_vars']['value'][('East',)] = 'true' if 'East' in game_state.getLegalActions() else 'false'
    state['state_vars']['value'][('West',)] = 'true' if 'West' in game_state.getLegalActions() else 'false'
    state['state_vars']['value'][('South',)] = 'true' if 'South' in game_state.getLegalActions() else 'false'
    return True

def is_done(state, dummy):
    global game
    if game is None:
        init(state, None)
        state['state_vars']['value'][('GameState',)] = codecs.encode(pickle.dumps(game.state), "base64").decode()
    game_state = pickle.loads(codecs.decode(state['state_vars']['value'][('GameState',)].encode(), "base64"))
    return game_state.getScore() >= 0
