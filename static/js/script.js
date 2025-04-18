$(document).ready(function() {
    // Edit todo button click handler
    $('.edit-btn').click(function() {
        const todoId = $(this).data('id');
        
        // Fetch todo data
        $.get(`/get_todo/${todoId}`, function(data) {
            // Populate form fields
            $('#editText').val(data.text);
            $('#editDueDate').val(data.due_date);
            $('#editDueTime').val(data.due_time);
            
            // Set form action
            $('#editTodoForm').attr('action', `/update_todo/${todoId}`);
            
            // Show modal
            new bootstrap.Modal(document.getElementById('editTodoModal')).show();
        });
    });
    
    // Confirm delete
    $('.delete-form').submit(function(e) {
        if (!confirm('Are you sure you want to delete this task?')) {
            e.preventDefault();
        }
    });
});
