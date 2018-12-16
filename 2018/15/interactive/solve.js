// Rendering

function turnTitle(turnNumber) {
    const title = document.createElement('span');
    title.style.position = 'absolute';
    title.style.fontSize = 'xx-large';
    title.style.fontFamily = 'monospace';
    title.textContent = 'Turns completed: ' + turnNumber;
    return title;
}

function blockTile(y,x) {
    const tile = document.createElement('span');
    tile.classList.add('tile');
    tile.classList.add('block' + ((3*y*y+x*x)%5));
    return tile;
}

function spaceTile(y,x) {
    const tile = document.createElement('span');
    tile.classList.add('tile');
    tile.classList.add('space' + ((1+4*y+3*x)%5));
    return tile;
}

function unitTile(y,x,unitType,hp) {
    const tile = document.createElement('span');
    tile.classList.add('tile');
    tile.classList.add('space' + ((1+4*y+3*x)%5));
    const hpBar = document.createElement('span');
    hpBar.classList.add('hp');
    tile.appendChild(hpBar);
    const green = document.createElement('span');
    green.classList.add('green');
    green.style.width = (hp/2) + '%';
    hpBar.appendChild(green);
    const unit = document.createElement('span')
    unit.classList.add('unit');
    unit.classList.add(unitType);
    tile.appendChild(unit);
    return tile;
}

function newLine() {
    const div = document.createElement('div');
    return div;
}

function renderWorld(turn, worldData, area) {
    const container = document.getElementById('container');
    container.innerHTML = '';
    container.append(turnTitle(turn));
    for (let y = 0; y < area.length; ++y) {
        const line = area[y];
        for (let x = 0; x < line.length; ++x) {
            const column = line[x];
            if (column == 'G' || column == 'E') {
                const {hp} = worldData[key(column, y, x)];
                container.append(unitTile(y,x,column,hp));
            } else if (column === '#') {
                container.append(blockTile(y,x));
            } else if (column === '.') {
                container.append(spaceTile(y,x));
            }
        }
        container.append(newLine());
    }
}

function renderStats(value) {
    const content = 'Full rounds completed: ' + value.time + '. Sum of remaining hit points: ' + value.hpSum + '. Puzzle answer: ' + (value.hpSum * value.time);
    const container = document.getElementById('container');
    container.append(document.createTextNode(content));
}

function renderElfDied(value) {
    const content = 'Unfortunately, an Elf died and the Gnomes won!';
    const container = document.getElementById('container');
    container.append(document.createTextNode(content));
}

// Input

function parseInput(input, elfAtk) {
    const worldData = {}
    const area = input.split("\n");

    let entityId = 1;
    for (let y = 0; y < area.length; ++y) {
        const line = area[y];
        for (let x = 0; x < line.length; ++x) {
            const c = line[x];
            if (c === 'G' || c === 'E') {
                worldData[key(c, y, x)] = {
                    entityId,
                    hp: 200,
                    atk: (c === 'E' ? elfAtk : 3),
                };
                entityId += 1;
            } else if (c !== '#' && c !== '.') {
                console.log('Invalid character', c)
            }
        }
    }
    return {worldData, area}
}

// Algorithm

function key(unit_type, y, x) {
    return unit_type + ',' + y + ',' + x;
}


function point(y,x) {
    return y + ',' + x;
}

function search(area, unit) {
    const {unitType, y, x} = unit;
    const enemyType = (unitType === 'E') ? 'G' : 'E';
    const queue = [{y, x, distance: 0, firstStep: null}];
    const visited = new Set([point(y, x)]);
    const possibleMoves = [];
    let maxMoveDistance = 1e10;
    while (queue.length > 0) {
        const {y, x, distance, firstStep} = queue.shift();
        if (distance > maxMoveDistance) {
            break;
        }
        for (const [dy, dx] of [[-1, 0], [0, -1], [0, 1], [1, 0]]) {
            const ny = y+dy;
            const nx = x+dx;
            if (visited.has(point(ny,nx))) {
                continue;
            }
            visited.add(point(ny, nx));
            if (area[ny][nx] === '.') {
                queue.push({y: ny, x: nx, distance: distance+1, firstStep: (firstStep ? firstStep : {y: ny, x: nx})});
            } else if (area[ny][nx] === enemyType) {
                if (firstStep === null) {
                    return {action: 'fight'}
                } else {
                    maxMoveDistance = distance;
                    possibleMoves.push({y, x, distance, firstStep});
                }
            }
        }
    }
    if (possibleMoves.length > 0) {
        if (possibleMoves.length > 1) {
            possibleMoves.sort((a, b) => {
                if (a.y !== b.y) {
                    return a.y-b.y;
                }
                return a.x-b.x;
            });
        }
        return {action: 'move', target: {y: possibleMoves[0].firstStep.y, x: possibleMoves[0].firstStep.x}};
    }
    return {action: 'pass'};
}

function findTargets(area, {unitType, y, x}) {
    const enemyType = (unitType === 'E') ? 'G' : 'E';
    const targets = [];
    for (const [dy, dx] of [[-1, 0], [0, -1], [0, 1], [1, 0]]) {
        const ny = y+dy;
        const nx = x+dx;
        if (area[ny][nx] === enemyType) {
            const target = {unitType: enemyType, y: ny, x :nx};
            targets.push(target)
        }
    }
    return targets;
}

function setTile(area, y, x, c) {
    area[y] = area[y].substring(0, x) + c + area[y].substring(x+1);
}

function tryFight(area, {unitType, y, x}, worldData) {
    const targets = findTargets(area, {unitType, y, x});
    if (targets.length === 0) {
        // Valid if no targets after move
        return {fight: false};
    }
    let lowHp = 201;
    let lowHpTarget = null;
    for (const target of targets) {
        const targetData = worldData[key(target.unitType, target.y, target.x)];
        if (targetData.hp < lowHp) {
            lowHp = targetData.hp;
            lowHpTarget = target;
        }
    }

    const attackerData = worldData[key(unitType, y, x)];
    const targetData = worldData[key(lowHpTarget.unitType, lowHpTarget.y, lowHpTarget.x)];
    targetData.hp -= attackerData.atk;

    if (targetData.hp <= 0) {
        setTile(area, lowHpTarget.y, lowHpTarget.x, '.');
        delete worldData[key(lowHpTarget.unitType, lowHpTarget.y, lowHpTarget.x)];
        return {fight: true, casualty: lowHpTarget.unitType};
    }
    return {fight: true}
}

function noEnemyAlive(unitType, worldData) {
    return Object.keys(worldData)
        .every((key) => key.split(",")[0] === unitType);
}

function* handleFrame(t, worldData, area) {
    const units = [];
    for (let y = 0; y < area.length; ++y) {
        const line = area[y];
        for (let x = 0; x < line.length; ++x) {
            const unitType = line[x];
            if (unitType === 'G' || unitType === 'E') {
                const {entityId} = worldData[key(unitType, y, x)];
                units.push({entityId, unitType, y, x})
            }
        }
    }
    console.log('Frame', t);
    console.log('Elves alive:', units.filter(unit => unit.unitType === 'E').length);
    console.log('Gnomes alive:', units.filter(unit => unit.unitType === 'G').length);

    for (const {entityId, unitType, y, x} of units) {
        if (!worldData[key(unitType, y, x)]) {
            // Dead unit
            continue;
        } else if (worldData[key(unitType, y, x)].entityId !== entityId) {
            // Other unit moved here
            continue;
        }
        if (noEnemyAlive(unitType, worldData)) {
            const hpSum = Object.values(worldData).map((data) => data.hp).reduce((a, b) => a + b, 0);
            yield {action: 'combatStop', time: t, hpSum: hpSum};
            return;
        }

        const {action, target} = search(area, {unitType, y, x});
        if (action === 'move') {
            setTile(area, y, x, '.');
            setTile(area, target.y, target.x, unitType);
            worldData[key(unitType, target.y, target.x)] = worldData[key(unitType, y, x)];
            delete worldData[key(unitType, y, x)];
            yield {action: 'move', unitType};
            const {fight, casualty} = tryFight(area, {unitType, y: target.y, x: target.x}, worldData);
            if (fight) {
                yield {action: 'fight', unitType, casualty};
            }
        } else if (action === 'fight') {
            const {fight, casualty} = tryFight(area, {unitType, y, x}, worldData);
            if (fight) {
                yield {action: 'fight', unitType, casualty};
            }
        } else {
            yield {action: 'pass', unitType};
        }
        yield {action: 'unit turn over'};
    }
}

function* handleSimulation(state, elfCanDie) {
    state.running = true;
    while (true) {
        if (state.running === false) {
            yield {action: 'stopped'};
        } else {
            outer:
            while (true) {
                const round = handleFrame(state.time, state.worldData, state.area);
                while (true) {
                    const {value, done} = round.next();
                    if (done) {
                        break;
                    }
                    if (value.action === 'combatStop') {
                        state.running = false;
                        yield value;
                        break outer;
                    }
                    if (!elfCanDie && value.action === 'fight' && value.casualty === 'E') {
                        state.running = false;
                        yield {action: 'elfDied'};
                        break outer;
                    }
                    yield value;
                }
                state.time += 1;
                yield {action: 'full turn over'};
            }
        }
    }
}

let interval = 16;
function initSimulation(input, elfAtk, elfCanDie, onFinishCallback) {
    const state = parseInput(input, elfAtk);
    state.time = 0;
    renderWorld(state.time, state.worldData, state.area);
    // Debug state with global
    window.state = state;

    const simulator = handleSimulation(state, elfCanDie);
    let currentResolve = null;
    let actionMatch = null;
    let lastAction = null;
    let doRenderDetails = true;
    let doRenderTurnEnd = true;
    const stateRecord = [{
        action: 'initial',
        state: JSON.stringify(state)}];
    function iterate() {
        while (true) {
            const {value, done} = simulator.next();
            if (done) {
                throw new Error('Simulator should never be done');
            }
            if (!value || !value.action) {
                throw new Error('Invalid next state');
            }
            if (value.action === 'stopped') {
                // Nothing to be done unless state is reverted.
                onFinishCallback();
                clearInterval(timerId);
                timerId = null;
                if (currentResolve !== null) {
                    currentResolve(false);
                    currentResolve = null;
                    actionMatch = null;
                }
                return;
            }
            lastAction = value.action;

            if (value.action === 'full turn over') {
                stateRecord.push({action: value.action,
                    state: JSON.stringify(state)});
                if (doRenderTurnEnd) {
                    renderWorld(state.time, state.worldData, state.area);
                    if (currentResolve === null) {
                        return;
                    }
                }
            }
            if ((value.action === 'move' || value.action === 'fight')) {
                if (doRenderDetails) {
                    renderWorld(state.time, state.worldData, state.area);
                    if (currentResolve === null) {
                        return;
                    }
                }
            }
            if (value.action === 'combatStop' || value.action === 'elfDied') {
                renderWorld(state.time, state.worldData, state.area);
                if (value.action === 'combatStop') {
                    renderStats(value);
                } else {
                    renderElfDied(value);
                }
                onFinishCallback();
                clearInterval(timerId);
                timerId = null;
                if (currentResolve === null) {
                    return;
                }
            }
            if (currentResolve !== null && actionMatch(value.action)) {
                clearInterval(timerId);
                timerId = null;
                currentResolve(false);
                currentResolve = null;
                actionMatch = null;
                return;
            }
        }
    }

    let timerId = null;
    return {
        pause() {
            if (currentResolve !== null) {
                throw new Error('Already resolving');
            }
            doRenderDetails = true;
            doRenderTurnEnd = false;
            return new Promise((resolve, reject) => {
                if (timerId !== null) {
                    actionMatch = () => true;
                    currentResolve = resolve;
                } else {
                    timerId = setInterval(iterate, interval);
                    resolve(true);
                }
            });
        },
        stop() {
            if (currentResolve !== null) {
                throw new Error('Already pausing');
            }
            return new Promise((resolve, reject) => {
                if (timerId !== null) {
                    actionMatch = (a) => true;
                    currentResolve = resolve;
                } else {
                    resolve();
                }
            });
        },
        until(action) {
            if (timerId) {
                throw new Error('Invalid state');
            }
            actionMatch = (a) => a === action;
            if (action === 'full turn over') {
                doRenderDetails = false;
                doRenderTurnEnd = true;
            } else if (action === 'combatStop') {
                doRenderDetails = false;
                doRenderTurnEnd = false;
                actionMatch = (a) => a === action || a === 'elfDied';
            } else {
                doRenderDetails = true;
                doRenderTurnEnd = false;
            }
            timerId = setInterval(iterate, interval);
            return new Promise((resolve, reject) => {
                currentResolve = resolve;
            });
        },
        async revertTurn() {
            if (timerId) {
                throw new Error('Invalid state');
            }
            let promise;
            if (lastAction === 'full turn over' || !state.running) {
                promise = new Promise((resolve) => {
                    resolve();
                });
            } else {
                doRenderDetails = false;
                doRenderTurnEnd = false;
                timerId = setInterval(iterate, interval);
                promise = new Promise((resolve, reject) => {
                    actionMatch = (a) => a === 'full turn over';
                    currentResolve = resolve;
                });
            }
            await promise;
            if (lastAction === 'full turn over' && stateRecord.length > 1) {
                stateRecord.pop();
            }
            while (stateRecord.length > 0) {
                const previousState = stateRecord.pop();
                if (previousState.action === 'full turn over' || previousState.action === 'initial') {
                    stateRecord.push(previousState);
                    const prevousStateParsed = JSON.parse(previousState.state);
                    state.worldData = prevousStateParsed.worldData;
                    state.area = prevousStateParsed.area;
                    state.time = prevousStateParsed.time;
                    state.running = true;
                    lastAction = previousState.action;
                    renderWorld(state.time, state.worldData, state.area);
                    break;
                }
            }
        }
    }
}

const mapInput = document.getElementById('map');
const elfAtkInput = document.getElementById('elfAtk');
const elfCanDieInput = document.getElementById('elfCanDie');
const stopBtn = document.getElementById('stop');
const playBtn = document.getElementById('play');
const unitTurnBtn = document.getElementById('unit_turn');
const fullTurnBtn = document.getElementById('full_turn');
const allTurnsBtn = document.getElementById('all_turns');
const backFullTurnBtn = document.getElementById('back_full_turn');

let simulation = null;
function setRunningInputs(running) {
    stopBtn.disabled = false;
    backFullTurnBtn.disabled = running;
    allTurnsBtn.disabled = running;
    fullTurnBtn.disabled = running;
    unitTurnBtn.disabled = running;
    if (running) {
        enableInputs(!running);
    }
}
function enableInputs(enabled) {
    mapInput.disabled = !enabled;
    elfAtkInput.disabled = !enabled
    elfCanDieInput.disabled = !enabled;
}
function createSimulation() {
    setRunningInputs(true);
    if (simulation) {
        return;
    }
    const input = mapInput.value;
    const elfAtk = elfAtkInput.value;
    const elfCanDie = elfCanDieInput.checked;
    simulation = initSimulation(input, elfAtk, elfCanDie, () => {
        setRunningInputs(false);
        stopBtn.disabled = true;
        playBtn.textContent = 'Play';
    });
}
stopBtn.addEventListener('click', async (ev) => {
    ev.preventDefault();
    if (confirm("Are you sure you want to clear simulator?")) {
        stopBtn.disabled = true;
        await simulation.stop()
        simulation = null;
        enableInputs(true);
        playBtn.textContent = 'Play';
        renderInitialMap();
    }
});
playBtn.addEventListener('click', async (ev) => {
    ev.preventDefault();
    createSimulation();

    const isRunning = await simulation.pause();
    if (isRunning) {
        playBtn.textContent = 'Pause'
        setRunningInputs(true);
    } else {
        playBtn.textContent = 'Play'
        setRunningInputs(false);
    }
    playBtn.disabled = false;
    stopBtn.disabled = false;
});

function forwarder(action) {
    return async (ev) => {
        ev.preventDefault();
        createSimulation();
        playBtn.disabled = true;

        await simulation.until(action);
        setRunningInputs(false);
        playBtn.disabled = false;
    };
}

unitTurnBtn.addEventListener('click', forwarder('unit turn over'));
fullTurnBtn.addEventListener('click', forwarder('full turn over'));
allTurnsBtn.addEventListener('click', forwarder('combatStop'));

backFullTurnBtn.addEventListener('click', async (ev) => {
    ev.preventDefault();
    createSimulation();
    playBtn.disabled = true;

    await simulation.revertTurn();
    setRunningInputs(false);
    playBtn.disabled = false;
});

function renderInitialMap() {
    const input = mapInput.value;
    const elfAtk = elfAtkInput.value;
    const {worldData, area} = parseInput(input, elfAtk);
    renderWorld(0, worldData, area);
};
renderInitialMap();