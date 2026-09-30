const SHAPES = ['●', '■', '▲', '◆', '⬡', '★'];
const $ = id => document.getElementById(id);

function showMessage(text = '') { $('message').textContent = text; }
function shuffle(items) { return [...items].sort(() => Math.random() - 0.5); }
function copyText(id) { navigator.clipboard.writeText($(id).value ?? $(id).textContent); }

$('password').addEventListener('input', e => $('counter').textContent = `${e.target.value.length}/6`);

document.querySelectorAll('.tab').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.tab, .panel').forEach(element => element.classList.remove('active'));
  button.classList.add('active');
  $(button.dataset.tab).classList.add('active');
  showMessage('');
}));

$('encodeBtn').addEventListener('click', () => {
  const password = $('password').value;
  if (password.length !== 6) return showMessage('A senha deve ter exatamente 6 caracteres.');

  const unique = [...new Set(password)];
  const mapping = Object.fromEntries(unique.map((character, index) => [character, shuffle(SHAPES)[index]]));
  const code = [...password].map(character => mapping[character]).join('');
  const key = Object.entries(mapping).map(([character, shape]) => `${shape}:${character}`).join(';');

  $('codeOutput').textContent = code;
  $('keyOutput').value = key;
  $('encodeResult').classList.remove('hidden');
  showMessage('');
});

$('decodeBtn').addEventListener('click', () => {
  const code = $('codeInput').value;
  const key = $('keyInput').value;
  if ([...code].length !== 6 || [...code].some(shape => !SHAPES.includes(shape))) return showMessage('O código deve conter exatamente 6 formas válidas.');
  if (!key.trim()) return showMessage('Informe a chave de decodificação.');

  const mapping = {};
  for (const pair of key.split(';')) {
    const [shape, character] = pair.split(':');
    if (!SHAPES.includes(shape) || !character || [...character].length !== 1) return showMessage('Formato de chave inválido.');
    mapping[shape] = character;
  }
  if ([...new Set(code)].some(shape => !mapping[shape])) return showMessage('A chave não corresponde ao código.');

  $('passwordOutput').textContent = [...code].map(shape => mapping[shape]).join('');
  $('decodeResult').classList.remove('hidden');
  showMessage('');
});

document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', () => copyText(button.dataset.copy)));
