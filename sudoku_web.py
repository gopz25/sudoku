from flask import Flask, render_template_string, request, jsonify
from sudoku_solver import validate_sudoku, solve_sudoku, count_unsolved

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sudoku Beautifier</title>
  <style>
    body { background: linear-gradient(120deg, #0f253e, #1e4d7b); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #fff; margin: 0; }
    h1 { text-align: center; margin-top: 1rem; font-size: 2rem; }
    .container { max-width: 980px; margin: 1rem auto 3rem; background: rgba(0,0,0,0.35); border-radius: 16px; padding: 1.2rem; box-shadow: 0 16px 34px rgba(0,0,0,0.4); }
    .grid { display: grid; grid-template-columns: repeat(9, 1fr); grid-gap: 5px; margin-bottom: 1rem; }
    .grid input { width: 100%; aspect-ratio: 1 / 1; border: 2px solid #3b5f8d; background: rgba(255,255,255,0.12); color: #fff; font-size: 1.1rem; text-align: center; border-radius: 6px; }
    .grid input:focus { outline: 2px solid #ffd54f; background: rgba(255,255,255,0.25); }
    .grid div { border: 2px solid transparent; }
    .grid div:nth-child(3n) { border-right: 2px solid #3174b7; }
    .grid div:nth-child(n+19):nth-child(-n+27), .grid div:nth-child(n+46):nth-child(-n+54) { border-bottom: 2px solid #3174b7; }
    .grid div:nth-child(9n+1) { border-left: 2px solid #3174b7; }
    .grid div:nth-child(-n+9) { border-top: 2px solid #3174b7; }
    .controls { text-align: center; margin-bottom: 1rem; }
    button { margin: 0 .3rem; padding: .7rem 1.2rem; font-weight: bold; border: none; border-radius: 10px; cursor: pointer; color:#0f253e; background:#ffd54f; transition: filter .2s ease; }
    button:hover { filter: brightness(1.08); }
    .secondary { background: #fff; color: #0f253e; }
    #status { color: #e5f2ff; margin-top: 1rem; text-align: center; font-weight:600; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Sudoku Solver UI</h1>
    <div class="grid" id="board"></div>
    <div class="controls">
      <button id="solve">Solve</button>
      <button id="clear" class="secondary">Clear</button>
      <button id="random" class="secondary">Load Example</button>
    </div>
    <div id="status">Enter puzzle values and click Solve.</div>
  </div>

  <script>
    const board = document.getElementById('board');
    const status = document.getElementById('status');
    const initial = [
      [3,0,0,0,0,0,0,0,0],
      [0,0,0,0,3,8,0,0,9],
      [0,7,0,2,6,0,0,0,5],
      [0,5,0,0,0,0,0,3,1],
      [8,0,3,0,9,0,7,0,6],
      [2,6,0,0,0,0,0,9,0],
      [5,0,0,0,2,6,0,8,0],
      [6,0,0,1,5,0,0,0,0],
      [0,0,0,0,0,0,0,0,3]
    ];

    const cells=[];
    for(let i=0;i<81;i++){ const cell=document.createElement('input'); cell.type='text'; cell.maxLength='1'; cell.pattern='[1-9]';
      cell.addEventListener('input',()=>{ cell.value=cell.value.replace(/[^1-9]/g,''); });
      board.appendChild(cell); cells.push(cell); }

    function readBoard(){ return Array.from({length:9},(_,r)=>Array.from({length:9},(_,c)=>{
      const val = cells[r*9+c].value.trim();
      return val ? parseInt(val,10) : 0;
    })); }

    function writeBoard(mat){ mat.forEach((row,r)=>row.forEach((v,c)=>{ cells[r*9+c].value=v===0?'':v; })); }

    document.getElementById('clear').onclick=()=>{ cells.forEach(c=>c.value=''); status.textContent='Cleared.'; };
    document.getElementById('random').onclick=()=>{ writeBoard(initial); status.textContent='Example loaded.'; };

    document.getElementById('solve').onclick=async()=>{
      const grid=readBoard();
      const resp = await fetch('/api/solve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({grid})});
      const data = await resp.json();
      if(data.ok){ writeBoard(data.solution); status.textContent='Solved ✅'; }
      else { status.textContent = 'Error: '+data.error; }
    };

    writeBoard(initial);
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/solve', methods=['POST'])
def api_solve():
    body = request.get_json(force=True)
    grid = body.get('grid')
    if not isinstance(grid, list) or len(grid) != 9 or any(len(row) != 9 for row in grid if isinstance(row, list)):
        return jsonify(ok=False, error='Grid must be 9x9'), 400

    try:
        if not validate_sudoku(grid):
            return jsonify(ok=False, error='Invalid Sudoku: duplicates found'), 400

        solving = [row[:] for row in grid]
        if not solve_sudoku(solving):
            return jsonify(ok=False, error='Unable to solve this Sudoku'), 400

        return jsonify(ok=True, solution=solving, unsolved_initial=count_unsolved(grid), unsolved_final=count_unsolved(solving))
    except Exception as ex:
        return jsonify(ok=False, error=str(ex)), 500

if __name__ == '__main__':
    app.run(debug=True)
