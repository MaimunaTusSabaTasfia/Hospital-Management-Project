document.addEventListener("DOMContentLoaded", () => {
  // ---------- Doctor Login ----------
  const loginForm = document.getElementById("doctorLoginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();

      let username = document.getElementById("doctorUsername").value.trim();
      let password = document.getElementById("doctorPassword").value.trim();

      let doctors = JSON.parse(localStorage.getItem("doctors")) || [];
      let doctor = doctors.find(
        (d) => d.username === username && d.password === password
      );

      if (doctor) {
        localStorage.setItem("loggedDoctor", JSON.stringify(doctor));
        window.location.href = "doctorDashboard.html";
      } else {
        document.getElementById("loginError").style.display = "block";
      }
    });
  }

  // ---------- Doctor Dashboard ----------
  if (window.location.pathname.includes("doctorDashboard.html")) {
    let doctor = JSON.parse(localStorage.getItem("loggedDoctor"));
    if (!doctor) {
      alert("Please login first");
      window.location.href = "doctor.html";
      return;
    }

    // Show profile
    document.getElementById("doctorProfile").innerHTML = `
      <p><b>Name:</b> ${doctor.name}</p>
      <p><b>Speciality:</b> ${doctor.speciality}</p>
      <p><b>Qualification:</b> ${doctor.qualification}</p>
      <p><b>Working Days:</b> ${doctor.workingDays}</p>
    `;

    // Logout
    document.getElementById("logoutBtn").addEventListener("click", () => {
      localStorage.removeItem("loggedDoctor");
      window.location.href = "index.html";
    });

    // Patients list
    let patients = JSON.parse(localStorage.getItem("patients")) || [];
    let appointments = JSON.parse(localStorage.getItem("appointments")) || [];

    let myAppointments = appointments.filter(
      (a) => a.doctorUsername === doctor.username
    );

    let table = document.getElementById("doctorPatientsTable");
    myAppointments.forEach((a) => {
      let patient = patients.find((p) => p.username === a.patientUsername);
      if (patient) {
        let row = table.insertRow();
        row.insertCell(0).innerText = patient.name;
        row.insertCell(1).innerText = patient.age;
        row.insertCell(2).innerText = patient.problem;
        row.insertCell(3).innerText = patient.reports || "None";
        row.insertCell(4).innerText = patient.prescription || "None";
      }
    });

    // Upload Report & Prescription
    document
      .getElementById("uploadForm")
      .addEventListener("submit", function (e) {
        e.preventDefault();
        let patientUser = document.getElementById("patientUser").value;
        let prescription = document.getElementById("prescription").value;
        let file = document.getElementById("reportFile").files[0];

        let patients = JSON.parse(localStorage.getItem("patients")) || [];
        let pIndex = patients.findIndex((p) => p.username === patientUser);
        if (pIndex !== -1) {
          patients[pIndex].prescription = prescription;
          if (file) {
            patients[pIndex].reports = file.name;
          }
          localStorage.setItem("patients", JSON.stringify(patients));
          alert("Updated successfully!");
          window.location.reload();
        } else {
          alert("Patient not found!");
        }
      });

    // Operation Requests
    let operations = JSON.parse(localStorage.getItem("operations")) || [];
    let myOps = operations.filter((op) => op.doctorUsername === doctor.username);

    let opTable = document.getElementById("operationTable");
    myOps.forEach((op, idx) => {
      let row = opTable.insertRow();
      row.insertCell(0).innerText = op.patientUsername;
      row.insertCell(1).innerText = op.details;
      row.insertCell(2).innerText = op.status || "Pending";

      let actionCell = row.insertCell(3);
      if (!op.status || op.status === "Pending") {
        let acceptBtn = document.createElement("button");
        acceptBtn.innerText = "Accept";
        acceptBtn.onclick = () => {
          myOps[idx].status = "Accepted";
          localStorage.setItem("operations", JSON.stringify(operations));
          alert("Operation Accepted");
          window.location.reload();
        };

        let rejectBtn = document.createElement("button");
        rejectBtn.innerText = "Reject";
        rejectBtn.onclick = () => {
          myOps[idx].status = "Rejected";
          localStorage.setItem("operations", JSON.stringify(operations));
          alert("Operation Rejected");
          window.location.reload();
        };

        actionCell.appendChild(acceptBtn);
        actionCell.appendChild(rejectBtn);
      }
    });

    // Achievements Graph
    let ctx = document.getElementById("achievementChart");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Patients", "Operations", "Reports"],
        datasets: [
          {
            label: "Doctor Stats",
            data: [
              myAppointments.length,
              myOps.length,
              patients.filter((p) => p.prescription || p.reports).length,
            ],
            backgroundColor: ["blue", "green", "orange"],
          },
        ],
      },
    });
  }
});