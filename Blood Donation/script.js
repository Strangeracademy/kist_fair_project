// Array to store donor data
let donors = [
    { name: "John Doe", bloodType: "O+", location: "Kathmandu" },
    { name: "Jane Smith", bloodType: "A+", location: "Pokhara" },
    { name: "Ravi Kumar", bloodType: "B+", location: "Chitwan" },
    { name: "Anita Rai", bloodType: "O-", location: "Lalitpur" }
];

// Function to display available donors
function displayDonors() {
    const donorListDiv = document.getElementById("donorList");
    donorListDiv.innerHTML = ""; // Clear previous list

    donors.forEach(donor => {
        const donorDiv = document.createElement("div");
        donorDiv.classList.add("donor");

        donorDiv.innerHTML = `
            <p>Name: ${donor.name}</p>
            <p>Blood Type: ${donor.bloodType}</p>
            <p>Location: ${donor.location}</p>
        `;

        donorListDiv.appendChild(donorDiv);
    });
}

// Function to handle blood donation request
document.getElementById("donationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const bloodType = document.getElementById("bloodType").value;
    const location = document.getElementById("location").value;

    // Add the request to the donor list (or database in the real app)
    donors.push({ name, bloodType, location });

    // Clear form and show confirmation
    document.getElementById("donationForm").reset();
    alert("Your blood donation request has been added!");

    // Update donor list after the new request
    displayDonors();
});

// Initial call to display donors
displayDonors();
