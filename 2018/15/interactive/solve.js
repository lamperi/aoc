function key(unit_type, y, x) {
    return unit_type + ',' + y + ',' + x;
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

function renderWorld(worldData, area) {
    const container = document.getElementById('container');
    container.innerHTML = '';
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
            // YIELD MOVE
            yield {action: 'move', unitType};
            const {fight, casualty} = tryFight(area, {unitType, y: target.y, x: target.x}, worldData);
            // YIELD FIGHT
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
    }
}

function* handleSimulation(worldData, area, elfCanDie) {
    let time = 0;
    while (time < 2000) {
        const round = handleFrame(time, worldData, area);
        while (true) {
            const {value, done} = round.next();
            if (done) {
                break;
            }
            yield value;
            if (value.action === 'combatStop') {
                return;
            }
            if (!elfCanDie && value.action === 'fight' && value.casualty === 'E') {
                yield {action: 'elfDied'};
                return;
            }
        }
        time += 1;
    }
}

let interval = 16;
function startSimulation(input, elfAtk, elfCanDie) {
    const {worldData, area} = parseInput(input, elfAtk);
    renderWorld(worldData, area);
    window.worldData = worldData;

    const simulator = handleSimulation(worldData, area, elfCanDie);
    let currentResolve = null;
    let onFinishCallback = null;
    function iterate() {
        const {value, done} = simulator.next();
        if (done) {
            onFinishCallback();
            clearInterval(timerId);
            timerId = null;
            return;
        }
        
        renderWorld(worldData, area);
        if (value && value.action === 'combatStop') {
            renderStats(value);
        }
        if (value && value.action === 'elfDied') {
            renderElfDied(value);
        }
        if (currentResolve !== null) {
            clearInterval(timerId);
            timerId = null;
            currentResolve();
            currentResolve = null;
        }
    }

    let timerId = setInterval(iterate, interval);
    return {
        pause() {
            if (currentResolve !== null) {
                throw new Error('Already pausing');
            }
            return new Promise((resolve, reject) => {   
                if (timerId !== null) {
                    currentResolve = resolve;
                } else {
                    timerId = setInterval(iterate, interval);
                    resolve();
                }
            });
        },
        stop() {
            if (currentResolve !== null) {
                throw new Error('Already pausing');
            }
            return new Promise((resolve, reject) => {   
                if (timerId !== null) {
                    currentResolve = resolve;
                } else {
                    resolve();
                }
            });
        },
        onFinish(cb) {
            onFinishCallback = cb;
        }
    }
}

const mapInput = document.getElementById('map');
const elfAtkInput = document.getElementById('elfAtk');
const elfCanDieInput = document.getElementById('elfCanDie');
const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const stopBtn = document.getElementById('stop');
let simulation = null;
startBtn.addEventListener('click', (ev) => {
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    stopBtn.disabled = false;
    mapInput.disabled = true;
    elfAtkInput.disabled = true;
    elfCanDieInput.disabled = true;

    const input = mapInput.value;
    const elfAtk = elfAtkInput.value;    
    const elfCanDie = elfCanDieInput.checked;
    simulation = startSimulation(input, elfAtk, elfCanDie);
    simulation.onFinish(() => {
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = true;

        mapInput.disabled = false;
        elfAtkInput.disabled = false;
        elfCanDieInput.disabled = false;
    });    
    ev.preventDefault();
});
pauseBtn.addEventListener('click', (ev) => {
    pauseBtn.disabled = true;
    simulation.pause().then(() => {
        pauseBtn.disabled = false;
        stopBtn.disabled = false;
    });
    ev.preventDefault();
});
stopBtn.addEventListener('click', (ev) => {
    pauseBtn.disabled = true;
    stopBtn.disabled = true;
    simulation.stop().then(() => {
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = true;

        mapInput.disabled = false;
        elfAtkInput.disabled = false;
        elfCanDieInput.disabled = false;
    });
    ev.preventDefault();
});

(function renderInitialMap() {
    const input = mapInput.value;
    const elfAtk = elfAtkInput.value;
    const {worldData, area} = parseInput(input, elfAtk);
    renderWorld(worldData, area);
})();
