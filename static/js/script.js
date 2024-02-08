document.addEventListener('DOMContentLoaded', function () {
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
        console.log('Page is reloaded');
        fetch('/reset-data', {method: 'POST'})
        .then(response => {
            if (response.ok) {
                console.log('Session data reset successfully');
            }
        });
    } else {
        console.log('Page is not reloaded');
    }
});

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
