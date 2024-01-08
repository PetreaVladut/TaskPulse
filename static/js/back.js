document.addEventListener("DOMContentLoaded", function () {
  // Select all the project columns as drag-and-drop containers
  var containers = Array.from(document.querySelectorAll(".project-column"));

  // Initialize Dragula with these containers
  var drake = dragula(containers);

  drake.on("drop", function (el, target, source, sibling) {
    // el: the element being dragged
    // target: the target container the element was dropped into
    // source: the original container the element was dragged from
    // sibling: the element next to the dragged element after dropping

    // Example: Update task status on server using AJAX (fetch)
    let taskId = el.getAttribute("data-task-id");
    let newStatus = target.getAttribute("data-status"); // Ensure your columns have 'data-status' attribute

    fetch("/update-task-status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ task_id: taskId, new_status: newStatus }),
    })
      .then((response) => response.json())
      .then((data) => console.log(data));
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const addTaskButtons = document.querySelectorAll(".add-task-button");

  // Function to handle button click
  function handleAddTaskClick() {
    // You can add your logic here
   // alert("Add Task button clicked!");
  }

  // Add click event listener to each button
  addTaskButtons.forEach(function (button) {
    button.addEventListener("click", handleAddTaskClick);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Example: Alert when form is submitted
  document.querySelector("form").onsubmit = function () {
    //alert("Task is being added!");
  };
});
function updateTags() {
  var input = document.getElementById("tags");
  var container = document.getElementById("tags-container");
  container.innerHTML = ""; // Clear existing tags

  // Split the input value by commas and filter out empty values
  var tags = input.value.split(",").filter(function (tag) {
    return tag.trim() !== "";
  });

  // Create a span element for each tag
  tags.forEach(function (tag) {
    var span = document.createElement("span");
    span.textContent = tag.trim();
    span.style.backgroundColor = "#50b3a2"; // Tag background color
    span.style.color = "white"; // Tag text color
    span.style.padding = "5px 10px";
    span.style.marginRight = "5px";
    span.style.borderRadius = "5px";
    container.appendChild(span);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".assign-button").forEach((button) => {
    button.addEventListener("click", function () {
      let taskId = this.dataset.taskId;
      let newUserId = prompt("Enter new user ID for task " + taskId); // Simple prompt, replace with your own UI

      if (newUserId) {
        fetch("/update-assignee", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ task_id: taskId, new_user_id: newUserId }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              //alert("Assignee updated successfully");
              // Update the UI here if necessary
            } else {
             // alert("Error updating assignee");
            }
          });
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners to all option buttons
  document.querySelectorAll(".task__options").forEach(function (button) {
    button.addEventListener("click", function (event) {
      // Prevent the click from propagating
      event.stopPropagation();
      // Close all other dropdowns
      closeAllDropdowns();
      // Toggle the current dropdown
      this.nextElementSibling.style.display =
        this.nextElementSibling.style.display === "block" ? "none" : "block";
    });
  });

  // Clicking outside of the dropdown closes any open dropdowns
  document.addEventListener("click", function () {
    closeAllDropdowns();
  });
});

function closeAllDropdowns() {
  document.querySelectorAll(".dropdown-menu").forEach(function (dropdown) {
    dropdown.style.display = "none";
  });
}

function editTask() {
  // Implement task editing logic
 // alert("Edit task clicked");
}

function deleteTask() {
  // Implement task deletion logic
 // alert("Delete task clicked");
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".add-member").forEach((button) => {
    button.addEventListener("click", function () {
      // Example: Prompt for user ID and team ID
      let userId = prompt("Enter User ID:");
      let teamId = this.getAttribute("data-team-id");

      if (userId && teamId) {
        fetch("/add-member-to-team", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_id: userId, team_id: teamId }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              window.location.reload();
             // alert("Member added to team successfully");
              // Update the UI here if necessary
            } else {
             // alert("Error adding member to team");
            }
          });
      }
    });
  });
});


document.querySelector(".task__options").addEventListener("click", function () {
  document.querySelector(".dropdown-content").classList.toggle("show");
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".delete_member").forEach((button) => {
    button.addEventListener("click", function () {
      let userId = this.getAttribute("data-user-id");
      let teamId = this.getAttribute("data-team-id");

      fetch(`/delete_member/${userId}/${teamId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: userId, team_id: teamId }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            window.location.reload();
           // alert("Member removed successfully");
            // Optionally, update the UI here to reflect the change
          } else {
          //  alert("Error removing member");
          }
        });
    });
  });
});
function editTask(task_id) {
  // Implement task editing logic
  let taskId = task_id;

  fetch(`/task/edit/${taskId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task_id: taskId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        //alert("Member removed successfully");
        // Optionally, update the UI here to reflect the change
      } else {
       // alert("Error removing member");
      }
    });
 // alert("Edit task clicked");
}

function deleteTask() {
  // Implement task deletion logic
 // alert("Delete task clicked");
}

/* function changeTeamClick(event) {
  // Get the team ID from the data attribute
  let teamId = event.target.getAttribute('data-team-id');

  // Call the route with the team ID (modify the URL as needed)
  fetch(`/change_team/${teamId}`, {
      method: 'POST', // You can use 'POST' if needed
      headers: {
          'Content-Type': 'application/json'
      },
      // Add any request body data if needed
      body: JSON.stringify({ teamId: teamId })
  })
  .then(response => {
      if (response.ok) {
          // Handle a successful response here
          console.log('Team changed successfully.');
      } else {
          // Handle errors or other responses here
          console.error('Error changing team.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });

}
document.addEventListener("DOMContentLoaded", function() {
    // Your JavaScript code here

// Assign the click event to elements with class 'change-team'
const changeTeamButtons = document.querySelectorAll('.change-team');
changeTeamButtons.forEach(button => {
  button.addEventListener('click', changeTeamClick);
});
}); */