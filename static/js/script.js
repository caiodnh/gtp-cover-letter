// document.addEventListener('DOMContentLoaded', function () {
//     var navigationEntries = performance.getEntriesByType("navigation");
//     if (navigationEntries.length > 0 && navigationEntries[0].type === 'reload') {
//         console.log('Page is reloaded');
//         fetch('/reset-data', {method: 'POST'})
//         .then(response => {
//             if (response.ok) {
//                 console.log('Session data reset successfully');
//             }
//         });
//     } else {
//         console.log('Page is not reloaded');
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    var plainTextFormContainer = document.getElementById('plainTextFormContainer');
    if (plainTextFormContainer.style.display === 'block') {
        plainTextFormContainer.scrollIntoView({ behavior: 'smooth' });
    }
});

function copyLetterToClipboard() {
    const hiringManager = document.querySelector('input[name="hiring_manager"]').value;
    const bodyContent = document.querySelector('textarea[name="body"]').value;
    const closingExpression = document.querySelector('input[name="closing_expression"]').value;
    const candidateName = document.querySelector('input[name="candidate_name"]').value;
    
    const letterContent = `Dear ${hiringManager},\n\n${bodyContent}\n\n${closingExpression},\n\n${candidateName}`;
    
    navigator.clipboard.writeText(letterContent).then(function() {
        console.log('Letter content copied to clipboard');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

function placeholderFunction() {
    console.log("PDF functionality will be implemented here.");
    // Future implementation
}

function submitPdfForm() {
    // Show the PDF form container when the PDF File button is clicked
    var pdfFormContainer = document.getElementById('pdfFormContainer');
    pdfFormContainer.style.display = 'block'; // Make the PDF form visible

    // Optional: Scroll the PDF form into view
    pdfFormContainer.scrollIntoView({ behavior: 'smooth' });
    
    // You might not need to submit a form here directly if you're just displaying the PDF form
    // Remove or comment out the form submission logic if it's not needed here
    // var actionInput = document.getElementById('actionInput');
    // actionInput.value = 'generate_pdf';
    // var form = document.getElementById('plainTextForm');
    // form.submit();
}

// function submitPdfForm() {
//     var actionInput = document.getElementById('actionInput');
//     actionInput.value = 'generate_pdf';
//     var form = document.getElementById('plainTextForm'); // Ensure your form has this ID
//     form.submit(); // Submit the form with the action to generate the PDF
// }