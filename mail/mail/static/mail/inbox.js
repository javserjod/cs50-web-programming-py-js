document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send email when submitting the form
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    event.preventDefault();
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // 
      load_mailbox('sent');
    });

  })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails from the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Loop through each email and create a list item
    emails.forEach(email => {
      const emailElement = document.createElement('div');
      emailElement.className = 'email-item';
      emailElement.innerHTML = `
      <div>
        <strong>${email.sender}</strong> - ${email.subject} 
      </div>
      <div>
        <span class="date">${email.timestamp}</span>
      </div>
      `;
      // Style the email item
      emailElement.style.display = 'flex';
      emailElement.style.justifyContent = 'space-between';
      emailElement.style.cursor = 'pointer';
      emailElement.style.padding = '10px';
      emailElement.style.border = '1px solid #ccc';

      // Unread emails have grey background
      if (!email.read) {
        emailElement.style.backgroundColor = '#e3e3e3'; 
      }
      
      // Add click event to view the email
      emailElement.addEventListener('click', () => {
        view_email(email.id);
      });

      // Append the email item to the emails view
      document.querySelector('#emails-view').appendChild(emailElement);
    });
  });
  
    
}


function view_email(email_id) {
  // Fetch the email details
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Show the email details
    document.querySelector('#emails-view').innerHTML = `
      <p><strong>From:</strong> ${email.sender}</p>
      <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
      <p><strong>Subject:</strong> ${email.subject}</p>
      <p><strong>Timestamp:</strong> ${email.timestamp}</p>
      <div id="email-actions">
        <button id="reply-button">Reply</button>
        <button id="archive-button">${email.archived ? 'Unarchive' : 'Archive'}</button>
      </div>
      <hr>
      <p>${email.body}</p>
    `;

    document.querySelector('#email-actions').style.display = 'flex';
    document.querySelector('#email-actions').style.justifyContent = 'space-between';

    // Mark the email as read
    if (!email.read) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    }

    document.querySelector('#archive-button').addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(() => {
        // Reload the mailbox after archiving/unarchiving
        load_mailbox('inbox');
      })
    })

  })

}