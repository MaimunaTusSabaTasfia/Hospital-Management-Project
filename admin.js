// admin.js — fixed, full version
(function () {
  'use strict';

  
  /* ---------- Helpers ---------- */
  const qs = (sel) => document.querySelector(sel);
  const load = (key) => { try { return JSON.parse(localStorage.getItem(key)) || []; } catch (err) { console.error('load error', key, err); return []; } };
  const save = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (err) { console.error('save error', key, err); } };
  const escapeHtml = (input) => { if (input === null || input === undefined) return ''; return String(input).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;'); };

  /* ---------- Data ---------- */
  let doctors = load('doctors');
  let patients = load('patients');
  let staff = load('staff');
  let nurses = load('nurses');
  let medicines = load('medicines');
  let appointments = load('appointments');
  let operations = load('operations');
  let contacts = load('contacts'); // new for contact messages

  const persistAll = () => {
    save('doctors', doctors);
    save('patients', patients);
    save('staff', staff);
    save('nurses', nurses);
    save('medicines', medicines);
    save('appointments', appointments);
    save('operations', operations);
    save('contacts', contacts);
  };

  const usernameExists = (u) => {
    if (!u) return false;
    return [...doctors, ...patients, ...staff, ...nurses].some((x) => x.username === u);
  };

  /* ---------- DOM Refs ---------- */
  const refs = {
    doctorsTbody: qs('#doctorsTable tbody'),
    patientsTbody: qs('#patientsTable tbody'),
    staffAppsTbody: qs('#staffAppsTable tbody'),
    nurseAppsTbody: qs('#nurseAppsTable tbody'),
    medsTbody: qs('#medicinesTable tbody'),
    apptTbody: qs('#appointmentsTable tbody'),
    opsTbody: qs('#operationsTable tbody'),
    billsTbody: qs('#billsTable tbody'),
    contactsTbody: qs('#contactsTable tbody'),
    addDoctorForm: qs('#addDoctorForm'),
    addPatientForm: qs('#addPatientForm'),
    addMedicineForm: qs('#addMedicineForm'),
    btnRefresh: qs('#btnRefresh'),
    btnExport: qs('#btnExport'),
    btnLogout: qs('#btnLogout'),
    btnClearData: qs('#btnClearData'),
    countDoctors: qs('#countDoctors'),
    countPatients: qs('#countPatients'),
    countStaff: qs('#countStaff'),
    countNurses: qs('#countNurses'),
    countMedicines: qs('#countMedicines')
  };

  /* ---------- Forms ---------- */
  if (refs.addDoctorForm) {
    refs.addDoctorForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = (qs('#d_name')?.value || '').trim();
      const username = (qs('#d_username')?.value || '').trim();
      const password = (qs('#d_password')?.value || '').trim();
      if (!name || !username || !password) return alert('Name, username, and password required.');
      if (usernameExists(username)) return alert('Username already exists.');
      doctors.push({
        name,
        username,
        password,
        qualification: (qs('#d_qualification')?.value || '').trim(),
        speciality: (qs('#d_speciality')?.value || '').trim(),
        workingDays: (qs('#d_workingDays')?.value || '').trim(),
        picture: (qs('#d_picture')?.value || '').trim(),
        availability: 'Available',
        achievements: [0, 0, 0]
      });
      persistAll();
      refs.addDoctorForm.reset();
      renderAll();
      alert('Doctor added.');
    });
  }

  if (refs.addPatientForm) {
    refs.addPatientForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = (qs('#p_name')?.value || '').trim();
      const username = (qs('#p_username')?.value || '').trim();
      const password = (qs('#p_password')?.value || '').trim();
      if (!name || !username || !password) return alert('Name, username, and password required.');
      if (usernameExists(username)) return alert('Username already exists.');
      patients.push({
        name,
        username,
        password,
        age: (qs('#p_age')?.value || '').trim(),
        problem: (qs('#p_problem')?.value || '').trim(),
        picture: (qs('#p_picture')?.value || '').trim(),
        history: '',
        report: '',
        prescription: '',
        bill: 0,
        billStatus: 'Pending',
        paymentMethod: null,
        doctorUsername: null
      });
      persistAll();
      refs.addPatientForm.reset();
      renderAll();
      alert('Patient added.');
    });
  }

  if (refs.addMedicineForm) {
    refs.addMedicineForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = (qs('#m_name')?.value || '').trim();
      const price = parseFloat(qs('#m_price')?.value || 0) || 0;
      const qty = parseInt(qs('#m_qty')?.value || 0, 10) || 0;
      if (!name || qty <= 0) return alert('Name and positive quantity required.');
      const existing = medicines.find((m) => m.name.toLowerCase() === name.toLowerCase());
      if (existing) {
        existing.quantity += qty;
        existing.price = price || existing.price;
      } else {
        medicines.push({ name, price, quantity: qty });
      }
      persistAll();
      refs.addMedicineForm.reset();
      renderAll();
      alert('Medicine added/updated.');
    });
  }

  /* ---------- Delegated click handler ---------- */
  document.addEventListener('click', (ev) => {
    const btn = ev.target.closest('button[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    const index = btn.dataset.index ? parseInt(btn.dataset.index, 10) : null;
    const status = btn.dataset.status || null;
    switch (action) {
      case 'edit-doctor': editDoctor(index); break;
      case 'delete-doctor': deleteDoctor(index); break;
      case 'edit-patient': editPatient(index); break;
      case 'delete-patient': deletePatient(index); break;
      case 'approve-staff': approveStaff(index); break;
      case 'reject-staff': rejectStaff(index); break;
      case 'approve-nurse': approveNurse(index); break;
      case 'reject-nurse': rejectNurse(index); break;
      case 'edit-medicine': editMedicine(index); break;
      case 'delete-medicine': deleteMedicine(index); break;
      case 'op-status': setOperationStatus(index, status); break;
      case 'mark-paid': markPaid(index); break;
      default: console.warn('Unknown action', action);
    }
  });

  /* ---------- Actions ---------- */
  function editDoctor(i) { if (!Number.isInteger(i) || i < 0 || i >= doctors.length) return; const d = doctors[i]; const name = prompt('Name', d.name); if (name === null) return; d.name = name.trim() || d.name; d.qualification = (prompt('Qualification', d.qualification) || d.qualification).trim(); d.speciality = (prompt('Speciality', d.speciality) || d.speciality).trim(); d.workingDays = (prompt('Working days', d.workingDays) || d.workingDays).trim(); d.picture = (prompt('Picture URL', d.picture) || d.picture).trim(); persistAll(); renderAll(); }
  function deleteDoctor(i) { if (!Number.isInteger(i) || i < 0 || i >= doctors.length) return; if (confirm('Delete doctor?')) { doctors.splice(i, 1); persistAll(); renderAll(); } }
  function editPatient(i) { if (!Number.isInteger(i) || i < 0 || i >= patients.length) return; const p = patients[i]; const name = prompt('Name', p.name); if (!name) return; p.name = name.trim(); p.age = prompt('Age', p.age) || p.age; p.problem = prompt('Problem', p.problem) || p.problem; persistAll(); renderAll(); }
  function deletePatient(i) { if (!Number.isInteger(i) || i < 0 || i >= patients.length) return; if (confirm('Delete patient?')) { patients.splice(i, 1); persistAll(); renderAll(); } }
  function approveStaff(i) { if (!Number.isInteger(i) || i < 0 || i >= staff.length) return; const s = staff[i]; const defaultUsername = s.username || `staff_${Date.now()}`; const u = prompt('Username', defaultUsername); if (!u) return alert('Invalid username'); const uname = u.trim(); if (usernameExists(uname)) return alert('Username already exists'); s.username = uname; s.password = prompt('Password', 'password123') || 'password123'; s.status = 'Approved'; persistAll(); renderAll(); }
  function rejectStaff(i) { if (!Number.isInteger(i) || i < 0 || i >= staff.length) return; staff[i].status = 'Rejected'; persistAll(); renderAll(); }
  function approveNurse(i) { if (!Number.isInteger(i) || i < 0 || i >= nurses.length) return; const n = nurses[i]; const defaultUsername = n.username || `nurse_${Date.now()}`; const u = prompt('Username', defaultUsername); if (!u) return alert('Invalid username'); const uname = u.trim(); if (usernameExists(uname)) return alert('Username already exists'); n.username = uname; n.password = prompt('Password', 'password123') || 'password123'; n.status = 'Approved'; persistAll(); renderAll(); }
  function rejectNurse(i) { if (!Number.isInteger(i) || i < 0 || i >= nurses.length) return; nurses[i].status = 'Rejected'; persistAll(); renderAll(); }
  function editMedicine(i) { if (!Number.isInteger(i) || i < 0 || i >= medicines.length) return; const m = medicines[i]; const price = parseFloat(prompt('Price', m.price) || m.price); const qty = parseInt(prompt('Quantity', m.quantity) || m.quantity, 10); m.price = price; m.quantity = qty; persistAll(); renderAll(); }
  function deleteMedicine(i) { if (!Number.isInteger(i) || i < 0 || i >= medicines.length) return; if (confirm('Delete medicine?')) { medicines.splice(i, 1); persistAll(); renderAll(); } }
  function setOperationStatus(i, s) { if (!Number.isInteger(i) || i < 0 || i >= operations.length || !s) return; operations[i].status = s; persistAll(); renderAll(); }
  function markPaid(i) { if (!Number.isInteger(i) || i < 0 || i >= patients.length) return; patients[i].billStatus = 'Paid'; if (!patients[i].paymentMethod) patients[i].paymentMethod = 'Cash'; persistAll(); renderAll(); }

  /* ---------- Render ---------- */
  function renderDoctors() {
    if (!refs.doctorsTbody) return;
    refs.doctorsTbody.innerHTML = doctors.map((d, i) => `
      <tr>
        <td>${escapeHtml(d.name)}</td>
        <td>${escapeHtml(d.username)}</td>
        <td>${escapeHtml(d.qualification)}</td>
        <td>${escapeHtml(d.speciality)}</td>
        <td>${escapeHtml(d.workingDays)}</td>
        <td>${escapeHtml(d.availability)}</td>
        <td>
          <button data-action="edit-doctor" data-index="${i}">Edit</button>
          <button data-action="delete-doctor" data-index="${i}">Delete</button>
        </td>
      </tr>`).join('');
  }

  function renderPatients() {
    if (!refs.patientsTbody) return;
    refs.patientsTbody.innerHTML = patients.map((p, i) => `
      <tr>
        <td>${escapeHtml(p.name)}</td>
        <td>${escapeHtml(p.username)}</td>
        <td>${escapeHtml(p.age)}</td>
        <td>${escapeHtml(p.problem)}</td>
        <td>${escapeHtml(p.bill)}</td>
        <td>${escapeHtml(p.billStatus)}</td>
        <td>
          <button data-action="edit-patient" data-index="${i}">Edit</button>
          <button data-action="delete-patient" data-index="${i}">Delete</button>
        </td>
      </tr>`).join('');
  }

  function renderStaffApps() {
    if (!refs.staffAppsTbody) return;
    refs.staffAppsTbody.innerHTML = staff.map((s, i) => `
      <tr>
        <td>${escapeHtml(s.name)}</td>
        <td>${escapeHtml(s.qualification)}</td>
        <td>${escapeHtml(s.workPart)}</td>
        <td>${escapeHtml(s.workingDays)}</td>
        <td>${escapeHtml(s.status)}</td>
        <td>${s.status === 'Pending' ? `<button data-action="approve-staff" data-index="${i}">Approve</button> <button data-action="reject-staff" data-index="${i}">Reject</button>` : '<span>Processed</span>'}</td>
      </tr>`).join('');
  }

  function renderNurseApps() {
    if (!refs.nurseAppsTbody) return;
    refs.nurseAppsTbody.innerHTML = nurses.map((n, i) => `
      <tr>
        <td>${escapeHtml(n.name)}</td>
        <td>${escapeHtml(n.qualification)}</td>
        <td>${escapeHtml(n.experience)}</td>
        <td>${escapeHtml(n.workingDays)}</td>
        <td>${escapeHtml(n.status)}</td>
        <td>${n.status === 'Pending' ? `<button data-action="approve-nurse" data-index="${i}">Approve</button> <button data-action="reject-nurse" data-index="${i}">Reject</button>` : '<span>Processed</span>'}</td>
      </tr>`).join('');
  }

  function renderMedicines() {
    if (!refs.medsTbody) return;
    refs.medsTbody.innerHTML = medicines.map((m, i) => `
      <tr>
        <td>${escapeHtml(m.name)}</td>
        <td>${escapeHtml(m.price)}</td>
        <td>${escapeHtml(m.quantity)}</td>
        <td>
          <button data-action="edit-medicine" data-index="${i}">Edit</button>
          <button data-action="delete-medicine" data-index="${i}">Delete</button>
        </td>
      </tr>`).join('');
  }

  function renderAppointments() {
    if (!refs.apptTbody) return;
    refs.apptTbody.innerHTML = appointments.map((a, i) => `
      <tr>
        <td>${escapeHtml(a.patientName)}</td>
        <td>${escapeHtml(a.doctorName)}</td>
        <td>${escapeHtml(a.dateTime)}</td>
        <td>${escapeHtml(a.notes)}</td>
      </tr>`).join('');
  }

  function renderOperations() {
    if (!refs.opsTbody) return;
    refs.opsTbody.innerHTML = operations.map((op, i) => `
      <tr>
        <td>${escapeHtml(op.patientName)}</td>
        <td>${escapeHtml(op.doctorName)}</td>
        <td>${escapeHtml(op.status)}</td>
        <td>
          <button data-action="op-status" data-index="${i}" data-status="Scheduled">Scheduled</button>
          <button data-action="op-status" data-index="${i}" data-status="Done">Done</button>
        </td>
      </tr>`).join('');
  }

  function renderContacts() {
    if (!refs.contactsTbody) return;
    refs.contactsTbody.innerHTML = contacts.map((c, i) => `
      <tr>
        <td>${escapeHtml(c.name)}</td>
        <td>${escapeHtml(c.email)}</td>
        <td>${escapeHtml(c.message)}</td>
      </tr>`).join('');
  }

  function updateQuickCounts() {
    if (refs.countDoctors) refs.countDoctors.textContent = `Doctors: ${doctors.length}`;
    if (refs.countPatients) refs.countPatients.textContent = `Patients: ${patients.length}`;
    if (refs.countStaff) refs.countStaff.textContent = `Staff: ${staff.filter(s => s.status === 'Approved').length}`;
    if (refs.countNurses) refs.countNurses.textContent = `Nurses: ${nurses.filter(n => n.status === 'Approved').length}`;
    if (refs.countMedicines) refs.countMedicines.textContent = `Medicines: ${medicines.length}`;
  }

  function renderAll() {
    doctors = load('doctors');
    patients = load('patients');
    staff = load('staff');
    nurses = load('nurses');
    medicines = load('medicines');
    appointments = load('appointments');
    operations = load('operations');
    contacts = load('contacts');
    persistAll();
    renderDoctors();
    renderPatients();
    renderStaffApps();
    renderNurseApps();
    renderMedicines();
    renderAppointments();
    renderOperations();
    renderContacts();
    updateQuickCounts();
  }

  /* ---------- Buttons ---------- */
  if (refs.btnRefresh) refs.btnRefresh.addEventListener('click', renderAll);
  if (refs.btnExport) refs.btnExport.addEventListener('click', () => {
    const dump = { doctors, patients, staff, nurses, medicines, appointments, operations, contacts };
    const a = document.createElement('a');
    a.href = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(dump, null, 2));
    a.download = 'madicare-data.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
  });
  if (refs.btnClearData) refs.btnClearData.addEventListener('click', () => {
    if (!confirm('Clear all data?')) return;
    localStorage.clear();
    doctors = patients = staff = nurses = medicines = appointments = operations = contacts = [];
    renderAll();
  });
  if (refs.btnLogout) refs.btnLogout.addEventListener('click', () => {
    if (confirm('Logout?')) { localStorage.removeItem('adminLoggedIn'); window.location.href = 'index.html'; }
  });

  // Initial render
  renderAll();

})();