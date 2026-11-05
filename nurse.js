(function () {
  'use strict';

  const qs = (s) => document.querySelector(s);
  const load = (k) => {
    try { return JSON.parse(localStorage.getItem(k) || '[]'); }
    catch (e) { console.error('load error', e); return []; }
  };
  const save = (k, v) => localStorage.setItem(k, JSON.stringify(v));

  let nurses = load('nurses');

  const registerForm = qs('#registerForm');
  const loginForm = qs('#loginForm');
  const btnShowRegister = qs('#btnShowRegister');
  const btnShowLogin = qs('#btnShowLogin');

  btnShowRegister.onclick = () => {
    registerForm.style.display = 'block';
    loginForm.style.display = 'none';
  };
  btnShowLogin.onclick = () => {
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
  };

  // Registration - apply
  registerForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = qs('#n_name').value.trim();
    const qualification = qs('#n_qualification').value.trim();
    const experience = qs('#n_experience').value.trim();
    const workingDays = qs('#n_workingDays').value.trim();

    if (!name || !qualification) return alert('Please fill required fields.');

    const application = {
      name,
      qualification,
      experience,
      workingDays,
      status: 'Pending',
      username: null,
      password: null,
      achievements: [0,0,0],
      problems: []
    };

    nurses.push(application);
    save('nurses', nurses);
    registerForm.reset();
    alert('Application submitted. Wait for admin approval.');
  });

  // Login - only approved accounts
  loginForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const uname = qs('#login_username').value.trim();
    const pass = qs('#login_password').value.trim();
    const acct = nurses.find(n => n.username === uname && n.password === pass && n.status === 'Approved');
    if (acct) {
      localStorage.setItem('loggedNurse', uname);
      window.location.href = 'nursedashboard.html';
    } else {
      alert('Invalid credentials or not approved yet.');
    }
  });

})();