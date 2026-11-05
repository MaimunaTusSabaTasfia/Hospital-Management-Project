(function () {
  'use strict';

  const uname = localStorage.getItem('loggedNurse');
  const load = (k) => {
    try { return JSON.parse(localStorage.getItem(k) || '[]'); }
    catch (e) { console.error('load error', e); return []; }
  };
  const save = (k, v) => localStorage.setItem(k, JSON.stringify(v));

  if (!uname) { alert('Please login first.'); window.location.href = 'nurse.html'; return; }

  let nurses = load('nurses');
  const userIndex = nurses.findIndex(n => n.username === uname);
  if (userIndex === -1) { alert('Account not found.'); window.location.href = 'nurse.html'; return; }

  const user = nurses[userIndex];

  document.getElementById('welcome').textContent = `Welcome, ${user.name}!`;

  document.getElementById('nurseDetails').innerHTML = `
    <p><strong>Name:</strong> ${user.name}</p>
    <p><strong>Qualification:</strong> ${user.qualification}</p>
    <p><strong>Experience:</strong> ${user.experience}</p>
    <p><strong>Working Days:</strong> ${user.workingDays}</p>
    <p><strong>Status:</strong> ${user.status}</p>
    <p><strong>Username:</strong> ${user.username || 'N/A'}</p>
  `;

  // Achievements chart
  try {
    const ctx = document.getElementById('achievementsChart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Month 1', 'Month 2', 'Month 3'],
        datasets: [{
          label: 'Achievements',
          data: user.achievements || [0,0,0]
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (e) {
    console.warn('Chart error', e);
  }

  // Problems form
  const problemForm = document.getElementById('problemForm');
  const problemText = document.getElementById('problemText');

  problemForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const txt = problemText.value.trim();
    if (!txt) return;
    const entry = { text: txt, date: new Date().toLocaleString() };
    if (!nurses[userIndex].problems) nurses[userIndex].problems = [];
    nurses[userIndex].problems.push(entry);
    save('nurses', nurses);
    problemText.value = '';
    renderProblems();
  });

  function renderProblems() {
    const ul = document.getElementById('problemsList');
    const list = (nurses[userIndex].problems || []);
    if (!list.length) {
      ul.innerHTML = '<li>No reports yet.</li>';
      return;
    }
    ul.innerHTML = list.map(p => `<li>${p.text} <small>(${p.date})</small></li>`).join('');
  }
  renderProblems();

  window.logout = function () {
    localStorage.removeItem('loggedNurse');
    window.location.href = 'nurse.html';
  };

})();