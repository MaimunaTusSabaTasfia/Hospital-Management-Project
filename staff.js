(function () {
  'use strict';

  const qs = (s) => document.querySelector(s);
  const load = (k) => JSON.parse(localStorage.getItem(k) || '[]');
  const save = (k, v) => localStorage.setItem(k, JSON.stringify(v));

  let staff = load('staff');

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

  // Staff Registration
  registerForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const newStaff = {
      name: qs('#s_name').value.trim(),
      qualification: qs('#s_qualification').value.trim(),
      workPart: qs('#s_workPart').value.trim(),
      workingDays: qs('#s_workingDays').value.trim(),
      status: 'Pending',
      username: null,
      password: null,
      achievements: [0, 0, 0],
      problems: []
    };
    staff.push(newStaff);
    save('staff', staff);
    registerForm.reset();
    alert('Application submitted successfully! Wait for admin approval.');
  });

  // Staff Login
  loginForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const uname = qs('#login_username').value.trim();
    const pass = qs('#login_password').value.trim();
    const found = staff.find((s) => s.username === uname && s.password === pass && s.status === 'Approved');
    if (found) {
      localStorage.setItem('loggedStaff', uname);
      window.location.href = 'staffdashboard.html';
    } else {
      alert('Invalid login or not approved yet.');
    }
  });
})();