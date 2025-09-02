$(document).ready(function() {
    $('#loginForm').on('submit', function(e) {
        let username = $('#username').val();
        let password = $('#password').val();
        
        if (username === '' || password === '') {
            alert('Please fill in all fields');
            e.preventDefault();
        }
    });
});

$(document).ready(function() {
    $('#feedbackForm').on('submit', function(e) {
        let feedback = $('#feedback').val();
        let email = $('#email').val();
        
        if (feedback === '' || email === '') {
            alert('Please fill in all fields');
            e.preventDefault();  // Prevent form submission
        }
    });
});
