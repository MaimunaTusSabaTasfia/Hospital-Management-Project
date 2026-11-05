(function () {
  'use strict';

  const uname = localStorage.getItem('loggedStaff');
  const load = (k) => JSON.parse(localStorage.getItem(k) || '[]');
  const save = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  if (!uname) { alert('Please log in first.'); window.location.href = 'staff.html'; }

  let staff = load('staff');
  let user = staff.find((s) => s.username === uname);

  if (!user) { alert('Account not found.'); window.location.href = 'staff.html'; }

  document.getElementById('welcome').textContent = `Welcome, ${user.name}!`;
  document.getElementById('staffDetails').innerHTML = `
    <p><strong>Name:</strong> ${user.name}</p>
    <p><strong>Qualification:</strong> ${user.qualification}</p>
    <p><strong>Work Part:</strong> ${user.workPart}</p>
    <p><strong>Working Days:</strong> ${user.workingDays}</p>
    <p><strong>Status:</strong> ${user.status}</p>
    <p><strong>Username:</strong> ${user.username}</p>
  `;

  // Chart
  const ctx = document.getElementById('achievementsChart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Month 1', 'Month 2', 'Month 3'],
      datasets: [{
        label: 'Achievements',
        data: user.achievements,
        backgroundColor: ['#42a5f5', '#64b5f6', '#90caf9']
      }]
    }
  });

  // Problem Form
  document.getElementById('problemForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const txt = document.getElementById('problemText').value.trim();
    if (!txt) return;
    user.problems.push({ text: txt, date: new Date().toLocaleString() });
    save('staff', staff);
    document.getElementById('problemText').value = '';
    renderProblems();
  });

  function renderProblems() {
    const ul = document.getElementById('problemsList');
    ul.innerHTML = user.problems.map(p => `<li>${p.text} <small>(${p.date})</small></li>`).join('');
  }
  renderProblems();

  window.logout = function () {
    localStorage.removeItem('loggedStaff');
    window.location.href = 'staff.html';
  };
})();