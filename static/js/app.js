document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('game-board');
    const resetButton = document.getElementById('reset-button');
    let currentPlayer = 'X';

    // Crear celdas del tablero
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = row;
            cell.dataset.col = col;
            board.appendChild(cell);
        }
    }

    // Manejar clics en el tablero
    board.addEventListener('click', async (event) => {
        const cell = event.target;
        if (!cell.classList.contains('cell') || cell.classList.contains('taken')) return;

        const row = cell.dataset.row;
        const col = cell.dataset.col;
        console.log(row,col) //flag

        const response = await fetch('/make_move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row, col, player: currentPlayer })
        });

        const result = await response.json();

        if (result.status === 'invalid') return;
        cell.textContent = currentPlayer;
        cell.classList.add('taken');

        if (result.status === 'end') {
            alert(result.winner === 'Tie' ? '¡Es un empate!' : `¡Ganó ${result.winner}!`);
        } else if (result.ai_move) {
            const aiCell = document.querySelector(
                `.cell[data-row="${result.ai_move.row}"][data-col="${result.ai_move.col}"]`
            );
            aiCell.textContent = 'O';
            aiCell.classList.add('taken');
            if (result.winner) {
                alert(`¡Ganó ${result.winner}!`);
            }
        }
    });

    // Reiniciar juego
    resetButton.addEventListener('click', async () => {
        await fetch('/reset', { method: 'POST' });
        document.querySelectorAll('.cell').forEach(cell => {
            cell.textContent = '';
            cell.classList.remove('taken');
        });
        currentPlayer = 'X';
    });
});
