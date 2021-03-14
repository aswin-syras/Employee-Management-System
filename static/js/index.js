var loadFile = function(event) {
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
    }
};
// ************************** THE PAGE REFRESH ********************** //
window.addEventListener('DOMContentLoaded', (event) => {
    // Call the settingDefault when the page is refresh
    if (typeof settingDefault  === "function") {
        settingDefault();
    }
 })

function settingDefault () {
    var el = document.getElementById("salary_complete_details");
    if ( document.getElementById("select-employment_type") ) {
        var emp_type = parseInt(document.getElementById("select-employment_type").value);
        var hourly_details = document.getElementById("hourly_pay_details");
        if ( emp_type == 1000 ) {
                el.style.display = 'block'
                hourly_details.style.display = 'none'
        } else {
            el.style.display = 'none'
            hourly_details.style.display = 'block'
        }
    }
}

function  employee_type_function() {
    var el = document.getElementById("salary_complete_details");
    if ( document.getElementById("select-employment_type") ) {
        var emp_type = parseInt(document.getElementById("select-employment_type").value);
        var hourly_details = document.getElementById("hourly_pay_details");
        if ( emp_type == 1000 ) {
                el.style.display = 'block'
                hourly_details.style.display = 'none'
                document.getElementById("hourlyRateId").value = ''
                document.getElementById("salaryId").value = ''
        } else {
            el.style.display = 'none'
            hourly_details.style.display = 'block'
            document.getElementById("salaryId").value = ''
            document.getElementById("hourlyRateId").value = ''
        }
    }
}

function newEmployeeValidation () {

    if (document.getElementById("select-employment_type") ) {
        console.log("SALERt: ", document.getElementById("salaryId"));
        console.log("SALERt: ", document.getElementById("bonusId"));
        console.log("SALERt: ", document.getElementById("basicAllowanceId"));
        console.log("SALERt: ", document.getElementById("medicalAllowanceId"));
        console.log("SALERt: ", document.getElementById("pfId"));
        console.log("SALERt: ", document.getElementById("taxId"));
        console.log("SALERt: ", document.getElementById("hourlyRateId"));
    }
}

// Scroll to the top
window.onscroll = function(ev) {
    if ((window.scrollY) > 100 ) {
        document.getElementById("back-to-top").style.display = "block";
    } else {
        document.getElementById("back-to-top").style.display = "none";
    }
};

function roleChange ( role) {
    console.log("1312321: ", role);
}

