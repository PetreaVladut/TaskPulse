document.addEventListener('DOMContentLoaded', function () {
    // Select all the project columns as drag-and-drop containers
    var containers = Array.from(document.querySelectorAll('.project-column'));

    // Initialize Dragula with these containers
    var drake = dragula(containers);

    drake.on('drop', function (el, target, source, sibling) {
        // el: the element being dragged
        // target: the target container the element was dropped into
        // source: the original container the element was dragged from
        // sibling: the element next to the dragged element after dropping

        // Example: Update task status on server using AJAX (fetch)
        let taskId = el.getAttribute('data-task-id');
        let newStatus = target.getAttribute('data-status');  // Ensure your columns have 'data-status' attribute

        fetch('/update-task-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task_id: taskId, new_status: newStatus }),
        })
        .then(response => response.json())
        .then(data => console.log(data));
    });
});

  document.addEventListener("DOMContentLoaded", function () {
    const addTaskButtons = document.querySelectorAll(".add-task-button");
  
    // Function to handle button click
    function handleAddTaskClick() {
      // You can add your logic here
      alert("Add Task button clicked!");
    }
  
    // Add click event listener to each button
    addTaskButtons.forEach(function (button) {
      button.addEventListener("click", handleAddTaskClick);
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    // Example: Alert when form is submitted
    document.querySelector('form').onsubmit = function() {
        alert('Task is being added!');
    };
});
function updateTags() {
  var input = document.getElementById('tags');
  var container = document.getElementById('tags-container');
  container.innerHTML = '';  // Clear existing tags

  // Split the input value by commas and filter out empty values
  var tags = input.value.split(',').filter(function(tag) {
      return tag.trim() !== '';
  });

  // Create a span element for each tag
  tags.forEach(function(tag) {
      var span = document.createElement('span');
      span.textContent = tag.trim();
      span.style.backgroundColor = '#50b3a2';  // Tag background color
      span.style.color = 'white';              // Tag text color
      span.style.padding = '5px 10px';
      span.style.marginRight = '5px';
      span.style.borderRadius = '5px';
      container.appendChild(span);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.assign-button').forEach(button => {
      button.addEventListener('click', function() {
          let taskId = this.dataset.taskId;
          let newUserId = prompt("Enter new user ID for task " + taskId); // Simple prompt, replace with your own UI

          if(newUserId) {
              fetch('/update-assignee', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ task_id: taskId, new_user_id: newUserId }),
              })
              .then(response => response.json())
              .then(data => {
                  if(data.status === 'success') {
                      alert('Assignee updated successfully');
                      // Update the UI here if necessary
                  } else {
                      alert('Error updating assignee');
                  }
              });
          }
      });
  });
});

function editFunction() {
    console.log("Edit button clicked");
    // Add your edit logic here
}

function deleteFunction() {
    console.log("Delete button clicked");
    // Add your delete logic here
}

// Optional: close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

document.querySelector('.dropdown').addEventListener('click', function() {
    document.querySelector('.dropdown-content').classList.toggle('show');
});