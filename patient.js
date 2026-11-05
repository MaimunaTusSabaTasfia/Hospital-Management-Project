// ---------- Patient Dashboard ----------
document.addEventListener("DOMContentLoaded", () => {
  // Check if on dashboard page
  if (window.location.pathname.includes("patientDashboard.html")) {
    let patient = JSON.parse(localStorage.getItem("loggedPatient"));
    if (!patient) {
      alert("Please login first");
      window.location.href = "patient.html";
      return;
    }

    // Show profile
    document.getElementById("patientProfile").innerHTML = `
      <p><b>Name:</b> ${patient.name}</p>
      <p><b>Age:</b> ${patient.age}</p>
      <p><b>Problem:</b> ${patient.problem}</p>
    `;

    // Logout
    document.getElementById("logoutBtn").addEventListener("click", () => {
      localStorage.removeItem("loggedPatient");
      window.location.href = "index.html";
    });

    // Doctors List
    let doctors = JSON.parse(localStorage.getItem("doctors")) || [];
    let appointments = JSON.parse(localStorage.getItem("appointments")) || [];
    let table = document.getElementById("doctorsTable");

    if (table) {
      doctors.forEach((doc) => {
        let row = table.insertRow();
        row.insertCell(0).innerText = doc.name;
        row.insertCell(1).innerText = doc.speciality;
        row.insertCell(2).innerText = doc.qualification;
        row.insertCell(3).innerText = doc.workingDays;

        let actionCell = row.insertCell(4);
        let appointBtn = document.createElement("button");
        appointBtn.innerText = "Book Appointment";
        appointBtn.style.padding = "8px 12px";
        appointBtn.style.background = "#2c9cd4";
        appointBtn.style.color = "white";
        appointBtn.style.border = "none";
        appointBtn.style.borderRadius = "8px";
        appointBtn.style.cursor = "pointer";
        appointBtn.onclick = () => {
          appointments.push({
            doctorUsername: doc.username,
            patientUsername: patient.username,
          });
          localStorage.setItem("appointments", JSON.stringify(appointments));
          alert("Appointment Booked!");
          window.location.reload();
        };
        actionCell.appendChild(appointBtn);
      });
    }

    // Reports & Prescriptions
    let reportsDiv = document.getElementById("myReports");
    let prescriptionDiv = document.getElementById("myPrescription");
    if (reportsDiv) reportsDiv.innerText = "Report: " + (patient.reports || "None");
    if (prescriptionDiv) prescriptionDiv.innerText = "Prescription: " + (patient.prescription || "None");

    // Billing
    let billDiv = document.getElementById("myBill");
    if (billDiv) {
      let billAmount = patient.bill || 0;
      billDiv.innerText = "Bill: $" + billAmount + " (Status: " + (patient.billStatus || "Unpaid") + ")";
    }

    let payBtn = document.getElementById("payBillBtn");
    if (payBtn) {
      payBtn.onclick = () => {
        let method = document.getElementById("paymentMethod").value;
        let patients = JSON.parse(localStorage.getItem("patients")) || [];
        let idx = patients.findIndex((p) => p.username === patient.username);
        if (idx !== -1) {
          patients[idx].billStatus = "Paid via " + method;
          localStorage.setItem("patients", JSON.stringify(patients));
          alert("Bill Paid Successfully!");
          window.location.reload();
        }
      };
    }

    // Operation Requests
    let opForm = document.getElementById("operationForm");
    if (opForm) {
      opForm.addEventListener("submit", (e) => {
        e.preventDefault();
        let doctorUser = document.getElementById("operationDoctor").value;
        let details = document.getElementById("operationDetails").value;
        let operations = JSON.parse(localStorage.getItem("operations")) || [];
        operations.push({
          doctorUsername: doctorUser,
          patientUsername: patient.username,
          details: details,
          status: "Pending",
        });
        localStorage.setItem("operations", JSON.stringify(operations));
        alert("Operation Requested!");
        window.location.reload();
      });
    }

    let operations = JSON.parse(localStorage.getItem("operations")) || [];
    let myOps = operations.filter((op) => op.patientUsername === patient.username);
    let opTable = document.getElementById("operationTable");
    if (opTable) {
      myOps.forEach((op) => {
        let row = opTable.insertRow();
        row.insertCell(0).innerText = op.doctorUsername;
        row.insertCell(1).innerText = op.details;
        row.insertCell(2).innerText = op.status;
      });
    }

    // Medicines
    let medicines = JSON.parse(localStorage.getItem("medicines")) || [
      { name: "Paracetamol", price: 50 },
      { name: "Antibiotic", price: 100 },
    ];
    let medTable = document.getElementById("medicineTable");
    let purchases = patient.medicines || [];
    
    if (medTable) {
      medicines.forEach((m) => {
        let row = medTable.insertRow();
        row.insertCell(0).innerText = m.name;
        row.insertCell(1).innerText = "$" + m.price;

        let buyBtn = document.createElement("button");
        buyBtn.innerText = "Buy";
        buyBtn.style.padding = "8px 12px";
        buyBtn.style.background = "#2c9cd4";
        buyBtn.style.color = "white";
        buyBtn.style.border = "none";
        buyBtn.style.borderRadius = "8px";
        buyBtn.style.cursor = "pointer";
        buyBtn.onclick = () => {
          purchases.push(m);
          patient.medicines = purchases;
          let patients = JSON.parse(localStorage.getItem("patients")) || [];
          let idx = patients.findIndex((p) => p.username === patient.username);
          if (idx !== -1) {
            patients[idx] = patient;
            localStorage.setItem("patients", JSON.stringify(patients));
          }
          alert("Medicine Purchased!");
          window.location.reload();
        };
        row.insertCell(2).appendChild(buyBtn);
      });
    }

    let myMedList = document.getElementById("myMedicines");
    if (myMedList) {
      purchases.forEach((m) => {
        let li = document.createElement("li");
        li.innerText = m.name + " - $" + m.price;
        myMedList.appendChild(li);
      });
    }

    // Chart
    let ctx = document.getElementById("patientChart");
    if (ctx) {
      new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Appointments", "Operations", "Medicines"],
          datasets: [{
            data: [
              appointments.filter((a) => a.patientUsername === patient.username).length,
              myOps.length,
              purchases.length,
            ],
            backgroundColor: ["#42a5f5", "#66bb6a", "#ffa726"],
          }],
        },
      });
    }
  }
});