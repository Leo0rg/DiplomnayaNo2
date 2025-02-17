document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    });

    // Time input validation
    var startTimeInput = document.getElementById('start_time');
    var endTimeInput = document.getElementById('end_time');
    
    if (startTimeInput && endTimeInput) {
        endTimeInput.addEventListener('change', function() {
            if (startTimeInput.value && endTimeInput.value) {
                if (endTimeInput.value <= startTimeInput.value) {
                    alert('Час закінчення повинен бути пізніше часу початку');
                    endTimeInput.value = '';
                }
            }
        });
    }
}); 