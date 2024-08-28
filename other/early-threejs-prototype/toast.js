 // Function to show a toast message
 function showToast(message) {
    const container = document.getElementById('toast-container');
    
    // Create a new toast message element
    const toast = document.createElement('div');
    toast.classList.add('toast-message');
    toast.textContent = message;

    // Show the toast by adding the 'active' class
    toast.classList.add('active');

    // Add event listener to close button
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.addEventListener('click', () => {
        hideToast(toast);
    });
    toast.appendChild(closeButton);

    // Add the toast to the container
    container.appendChild(toast);

    // Automatically hide the toast after a few seconds (e.g., 5 seconds)
    setTimeout(() => {
        hideToast(toast);
    }, 2000);
}

// Function to hide a toast message
function hideToast(toast) {
    toast.classList.remove('active');
    
    // Remove the toast from the container after the fade-out animation
    toast.addEventListener('transitionend', () => {
        toast.remove();
    });
}