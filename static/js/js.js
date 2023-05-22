function validateForm() {
    var experienceField = document.getElementById("experience");
    var experienceValue = experienceField.value;
    if (experienceValue < 0) {
        alert("Experience cannot be negative.");
        return false;
    }

    var salaryField = document.getElementById("salary");
    var salaryValue = salaryField.value;
    if (salaryValue < 0) {
        alert("Salary cannot be negative.");
        return false;
    }

    return true;
}
